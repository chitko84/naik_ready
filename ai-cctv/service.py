"""Private synchronous inference HTTP service; Streamlit remains available as app.py."""
import base64
import json
import os
import shutil
import tempfile
import threading
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

os.environ.setdefault('NAIKREADY_RUNTIME_DIR', str(Path(tempfile.gettempdir()) / 'naikready-vision'))
import local_api as vision

app = FastAPI(title='NaikReady private AI', docs_url=None, redoc_url=None, openapi_url=None)
capacity = threading.BoundedSemaphore(1)
MAX_UPLOAD_BYTES = 3_500_000


def run_analysis(job_id, path, media_type, cfg):
    # Model configuration and inference must run under the same lock.
    if not capacity.acquire(blocking=False):
        raise HTTPException(429, 'The detector is busy. Please retry shortly.')
    try:
        vision.process_job(job_id, path, media_type, cfg)
        folder = vision.JOBS / job_id
        result = json.loads((folder / 'result.json').read_text())
        if result['status'] != 'complete':
            raise HTTPException(422, result.get('error', 'The file could not be analyzed.'))
        import cv2
        frame = cv2.imread(str(folder / 'evidence.jpg'))
        if frame is None:
            raise HTTPException(500, 'Evidence rendering failed.')
        height, width = frame.shape[:2]
        scale = min(1, 960 / max(width, height))
        if scale < 1:
            frame = cv2.resize(frame, (max(1, round(width*scale)), max(1, round(height*scale))))
        ok, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if not ok or len(jpeg) > 1_000_000:
            raise HTTPException(500, 'Evidence could not be encoded within the response limit.')
        result.pop('evidence_url', None)
        result['evidence_data_url'] = 'data:image/jpeg;base64,' + base64.b64encode(jpeg).decode('ascii')
        result['delivery'] = 'inline'
        return result
    finally:
        capacity.release()


@app.get('/health')
def health():
    return vision.health()


@app.post('/analyze')
async def analyze(file: UploadFile = File(...), media_type: str = Form(...), stop_id: str = Form('CYB-DEMO-01'), zone: str = Form('[[0.25,0.45],[0.85,0.45],[0.85,0.82],[0.25,0.82]]'), dwell_seconds: float = Form(10)):
    folder = None
    try:
        if media_type not in ('image', 'video'):
            raise HTTPException(422, 'media_type must be image or video.')
        try:
            cfg = vision.config_for(zone, stop_id, dwell_seconds)
        except (ValueError, TypeError, KeyError) as exc:
            raise HTTPException(422, str(exc)) from exc
        suffix = Path(file.filename or '').suffix.lower()
        allowed = ('.jpg','.jpeg','.png','.webp') if media_type == 'image' else ('.mp4','.mov','.avi','.webm','.mkv')
        if suffix not in allowed:
            raise HTTPException(422, f'Choose a supported {media_type} file.')
        content = await file.read(MAX_UPLOAD_BYTES + 1)
        if len(content) > MAX_UPLOAD_BYTES:
            raise HTTPException(413, 'Hosted upload limit is 3.5 MB.')
        if not content:
            raise HTTPException(422, 'The file is empty.')
        if not health()['inference_available']:
            raise HTTPException(503, 'The detector dependencies or weights are unavailable.')
        job_id = uuid.uuid4().hex
        folder = vision.JOBS / job_id
        folder.mkdir()
        path = folder / ('input' + suffix)
        path.write_bytes(content)
        # Do not return an ephemeral job ID and rely on a later invocation finding its disk.
        return await run_in_threadpool(run_analysis, job_id, path, media_type, cfg)
    finally:
        await file.close()
        if folder is not None:
            shutil.rmtree(folder, ignore_errors=True)


@app.get('/replay/{mode}')
def replay(mode: str):
    return vision.replay(mode)
