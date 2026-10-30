"""NaikReady API: Aung's actual YOLO + zone/dwell monitor, with explicit replay provenance."""
from pathlib import Path
import base64
import json
import math
import sys
import tempfile
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

ROOT = Path(__file__).resolve().parents[1]
AI = ROOT / 'ai-cctv'
sys.path.insert(0, str(AI))
app = FastAPI(title='NaikReady Vision API', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'], allow_methods=['GET', 'POST'], allow_headers=['*'])
JOBS = ROOT / 'backend' / 'runtime'
JOBS.mkdir(exist_ok=True)
pool = ThreadPoolExecutor(max_workers=1)
lock = threading.Lock()
model_lock = threading.Lock()
models = {}
for previous in JOBS.glob('*/result.json'):
    try:
        data=json.loads(previous.read_text())
        if data.get('status') in ('queued','processing'):
            previous.write_text(json.dumps({'status':'failed','error':'The analysis service restarted. Please submit the file again.','mode':data.get('mode','real_yolo_inference')}))
    except (OSError,ValueError):
        pass


def config_for(zone, stop, dwell):
    from detect import load_config
    cfg = load_config(AI / 'config.json')
    if stop not in ('CYB-DEMO-01', 'CYB-DEMO-02'):
        raise ValueError('Unknown bus stop.')
    points = json.loads(zone) if isinstance(zone, str) else zone
    if not isinstance(points, list) or not 3 <= len(points) <= 12:
        raise ValueError('Use 3–12 normalized polygon vertices.')
    if any(not isinstance(p, list) or len(p) != 2 or any(type(v) not in (float, int) or not math.isfinite(v) or not 0 <= v <= 1 for v in p) for p in points):
        raise ValueError('Each zone vertex must contain two numbers between 0 and 1.')
    area = abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(points,points[1:]+points[:1]))) / 2
    if area < .0001:
        raise ValueError('The zone must have a nonzero area.')
    if not math.isfinite(dwell) or not 1 <= dwell <= 30:
        raise ValueError('Dwell threshold must be between 1 and 30 seconds.')
    cfg.update(zone=points, stop_id=stop, dwell_seconds=dwell, model=str(AI / 'yolov8n.pt'))
    return cfg


def get_detector(cfg):
    from vision import YoloDetector
    # Only one worker uses inference. Models are loaded lazily; opening the UI never loads torch.
    with model_lock:
        key = cfg['model']
        if key not in models:
            models[key] = YoloDetector(cfg)
        models[key].cfg = cfg
        return models[key]


def write_job(job_id, value):
    path = JOBS / job_id / 'result.json'
    with lock:
        tmp = path.with_suffix('.tmp')
        tmp.write_text(json.dumps(value, allow_nan=False))
        tmp.replace(path)


def process_job(job_id, path, media_type, cfg):
    cap = None
    try:
        import cv2
        from core import ZoneMonitor
        from vision import annotate
        from event_export import export_events
        write_job(job_id, {'status': 'processing', 'progress': 0, 'phase':'loading_model', 'mode': 'real_yolo_inference'})
        detector = get_detector(cfg)
        write_job(job_id, {'status':'processing','progress':0,'phase':'analyzing_frames','mode':'real_yolo_inference'})
        monitor = ZoneMonitor(cfg, path.name, False)
        events, snapshots = [], []
        last_frame = None
        if media_type == 'image':
            frame = cv2.imread(str(path))
            if frame is None:
                raise ValueError('The file is not a decodable image.')
            if frame.size > 60_000_000:
                raise ValueError('Image is too large. Resize to less than 20 megapixels.')
            last_frame = frame
            snap = monitor.update(detector.predict(frame), 0)
            snapshots.append(snap)
        else:
            cap = cv2.VideoCapture(str(path))
            fps = cap.get(cv2.CAP_PROP_FPS)
            count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            if not cap.isOpened() or not math.isfinite(fps) or fps <= 0 or count <= 0:
                raise ValueError('Video needs decodable frames and valid duration metadata.')
            duration = count / fps
            if duration > 60 or count > 12000:
                raise ValueError('Use a video of 60 seconds or less (maximum 12,000 frames).')
            stride = max(1, round(fps / 5))
            index = 0
            with (JOBS / job_id / 'frames.jsonl').open('w') as log:
                while True:
                    ok, frame = cap.read()
                    if not ok:
                        break
                    if index % stride == 0:
                        snap = monitor.update(detector.predict(frame), index / fps)
                        log.write(json.dumps(snap) + '\n')
                        snapshots.append(snap)
                        events.extend(snap['events'])
                        last_frame = frame
                        if len(snapshots) % 5 == 0:
                            write_job(job_id, {'status':'processing', 'progress':min(99, round(index/count*100)), 'mode':'real_yolo_inference'})
                    index += 1
            if not snapshots:
                raise ValueError('No frames could be decoded.')
        last = snapshots[-1]
        cv2.imwrite(str(JOBS / job_id / 'evidence.jpg'), annotate(last_frame, last, cfg))
        exported = export_events(events)
        result = {'status':'complete', 'progress':100, 'job_id':job_id, 'mode':'real_yolo_inference', 'simulated':False,
                  'media_type':media_type, 'stop_id':cfg['stop_id'], 'zone':cfg['zone'], 'dwell_seconds':cfg['dwell_seconds'],
                  'frames_processed':len(snapshots), 'observations':last['detections'], 'zone_status':last['status'],
                  'events':exported, 'evidence_url':f'/api/jobs/{job_id}/evidence',
                  'note':'Single-frame occupancy only; no stationary dwell or obstruction event can be inferred from an image.' if media_type=='image' else 'YOLO detections + stationary bottom-center-in-polygon dwell. Potential obstruction requires human verification.',
                  'at':datetime.now(timezone.utc).isoformat()}
        write_job(job_id, result)
    except Exception as exc:
        write_job(job_id, {'status':'failed', 'error':str(exc), 'mode':'real_yolo_inference'})
    finally:
        if cap is not None:
            cap.release()
        path.unlink(missing_ok=True)


@app.get('/api/health')
def health():
    import importlib.util
    available = bool(importlib.util.find_spec('ultralytics') and importlib.util.find_spec('cv2') and (AI/'yolov8n.pt').exists())
    return {'status':'ok', 'inference_available':available, 'weights_present':(AI/'yolov8n.pt').exists(), 'network':'local HTTP; no measured 5G service'}


@app.post('/api/analyze', status_code=202)
async def analyze(file: UploadFile = File(...), media_type: str = Form(...), stop_id: str = Form('CYB-DEMO-01'),
                  zone: str = Form('[[0.25,0.45],[0.85,0.45],[0.85,0.82],[0.25,0.82]]'), dwell_seconds: float = Form(10)):
    if media_type not in ('image', 'video'):
        raise HTTPException(422, 'media_type must be image or video.')
    try:
        cfg = config_for(zone, stop_id, dwell_seconds)
    except (ValueError, TypeError, KeyError) as exc:
        raise HTTPException(422, str(exc)) from exc
    if not health()['inference_available']:
        raise HTTPException(503, 'Inference dependencies are unavailable. Install backend/requirements.txt or use the labeled recorded replay.')
    with lock:
        active = sum(1 for p in JOBS.glob('*/result.json') if json.loads(p.read_text()).get('status') in ('queued','processing'))
    if active >= 2:
        raise HTTPException(429, 'Two analyses are already queued. Wait for completion.')
    suffix = Path(file.filename or '').suffix.lower()
    allowed = ('.jpg','.jpeg','.png','.webp') if media_type=='image' else ('.mp4','.mov','.avi','.webm','.mkv')
    if suffix not in allowed:
        raise HTTPException(422, f'Choose a supported {media_type} file.')
    job_id = uuid.uuid4().hex
    folder = JOBS / job_id
    folder.mkdir()
    path = folder / ('input' + suffix)
    size = 0
    try:
        with path.open('wb') as out:
            while data := await file.read(1024 * 1024):
                size += len(data)
                if size > 40 * 1024 * 1024:
                    raise HTTPException(413, 'Upload limit is 40 MiB.')
                out.write(data)
        if not size:
            raise HTTPException(422, 'The file is empty.')
        write_job(job_id, {'status':'queued', 'progress':0, 'mode':'real_yolo_inference'})
        pool.submit(process_job, job_id, path, media_type, cfg)
    except Exception:
        path.unlink(missing_ok=True)
        raise
    finally:
        await file.close()
    return {'job_id':job_id, 'status':'queued'}


def job_path(job_id):
    if len(job_id)!=32 or any(c not in '0123456789abcdef' for c in job_id):
        raise HTTPException(404, 'Unknown analysis.')
    folder = JOBS / job_id
    if not (folder/'result.json').exists():
        raise HTTPException(404, 'Unknown analysis.')
    return folder


@app.get('/api/jobs/{job_id}')
def job(job_id: str):
    folder = job_path(job_id)
    with lock:
        return json.loads((folder/'result.json').read_text())


@app.get('/api/jobs/{job_id}/evidence')
def evidence(job_id: str):
    path = job_path(job_id) / 'evidence.jpg'
    if not path.exists():
        raise HTTPException(404, 'Evidence is not available yet.')
    return FileResponse(path, media_type='image/jpeg')


@app.get('/api/replay/{mode}')
def replay(mode: str):
    if mode not in ('simulation', 'recorded'):
        raise HTTPException(404, 'Choose simulation or recorded.')
    folder = AI / ('outputs/simulation' if mode=='simulation' else 'outputs/runs/da3235ed66')
    from event_export import export_events
    return {'mode':'scripted_simulation' if mode=='simulation' else 'recorded_video_model_inference',
            'summary':json.loads((folder/'summary.json').read_text()),
            'events':export_events(json.loads((folder/'events.json').read_text()))}

# After `npm run build`, the API can serve the complete app from one localhost origin.
@app.get('/{requested_path:path}', include_in_schema=False)
def frontend(requested_path: str):
    dist = ROOT / 'frontend' / 'dist'
    candidate = (dist / requested_path).resolve()
    if not candidate.is_relative_to(dist.resolve()) or requested_path.startswith('api/'):
        raise HTTPException(404, 'Not found.')
    if candidate.is_file():
        return FileResponse(candidate)
    if (dist/'index.html').exists():
        return FileResponse(dist/'index.html')
    raise HTTPException(404, 'Build the frontend first, or run npm run dev.')
