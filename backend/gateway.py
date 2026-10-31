"""Small public gateway: the binding is read only at request time, never during build."""
import os
from urllib.parse import urlsplit

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

MAX_UPLOAD_BYTES = 3_500_000  # Leaves room for multipart framing under Vercel's 4.5 MB ceiling.
ANALYSIS_TIMEOUT_SECONDS = 230


def service_url(path):
    base = os.environ.get('AI_CCTV_URL', '')
    parts = urlsplit(base)
    if parts.scheme not in ('http', 'https') or not parts.netloc or parts.query or parts.fragment:
        raise HTTPException(503, 'The private AI service binding is unavailable.')
    # Append to the bound base path instead of replacing it with a leading slash.
    return base.rstrip('/') + '/' + path.lstrip('/')


def create_app(transport=None):
    app = FastAPI(title='NaikReady public API', docs_url=None, redoc_url=None, openapi_url=None)

    async def call(method, path, **kwargs):
        url = service_url(path)
        try:
            async with httpx.AsyncClient(transport=transport, timeout=httpx.Timeout(ANALYSIS_TIMEOUT_SECONDS, connect=10), follow_redirects=False, trust_env=False) as client:
                response = await client.request(method, url, **kwargs)
        except httpx.TimeoutException as exc:
            raise HTTPException(504, 'The AI analysis timed out. Try a shorter video or smaller image.') from exc
        except httpx.RequestError as exc:
            raise HTTPException(503, 'The private AI service is temporarily unavailable.') from exc
        try:
            value = response.json()
        except ValueError as exc:
            raise HTTPException(502, 'The AI service returned an invalid response.') from exc
        if not isinstance(value, dict):
            raise HTTPException(502, 'The AI service returned an invalid response.')
        if response.is_error:
            detail = value.get('detail', 'AI analysis could not complete.')
            raise HTTPException(response.status_code if response.status_code in (413, 422, 429, 503, 504) else 502, detail)
        return value

    @app.get('/api/health')
    async def health():
        try:
            data = await call('GET', 'health')
            return {**data, 'max_upload_bytes': MAX_UPLOAD_BYTES, 'analysis_delivery': 'inline', 'network': 'Internal service HTTP; no measured 5G connection'}
        except HTTPException:
            return JSONResponse(status_code=503, content={'status': 'unavailable', 'inference_available': False, 'max_upload_bytes': MAX_UPLOAD_BYTES, 'analysis_delivery': 'inline'})

    @app.post('/api/analyze')
    async def analyze(file: UploadFile = File(...), media_type: str = Form(...), stop_id: str = Form('CYB-DEMO-01'), zone: str = Form('[[0.25,0.45],[0.85,0.45],[0.85,0.82],[0.25,0.82]]'), dwell_seconds: float = Form(10)):
        try:
            if media_type not in ('image', 'video'):
                raise HTTPException(422, 'media_type must be image or video.')
            content = await file.read(MAX_UPLOAD_BYTES + 1)
            if len(content) > MAX_UPLOAD_BYTES:
                raise HTTPException(413, 'Hosted upload limit is 3.5 MB. Use a smaller file or run local inference for files up to 40 MiB.')
            if not content:
                raise HTTPException(422, 'The file is empty.')
            return await call('POST', 'analyze', data={'media_type':media_type, 'stop_id':stop_id, 'zone':zone, 'dwell_seconds':str(dwell_seconds)}, files={'file':(file.filename or 'upload', content, file.content_type or 'application/octet-stream')})
        finally:
            await file.close()

    @app.get('/api/replay/{mode}')
    async def replay(mode: str):
        if mode not in ('simulation', 'recorded'):
            raise HTTPException(404, 'Choose simulation or recorded.')
        return await call('GET', f'replay/{mode}')

    @app.get('/api/jobs/{job_id}')
    @app.get('/api/jobs/{job_id}/evidence')
    async def old_job(job_id: str):
        raise HTTPException(410, 'Hosted analysis returns evidence directly. Submit the file again; local queued jobs are not available on this deployment.')

    return app
