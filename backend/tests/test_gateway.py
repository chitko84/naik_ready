import io
import json
from pathlib import Path
import sys

import httpx
import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from backend.gateway import create_app, MAX_UPLOAD_BYTES, service_url


def test_binding_is_runtime_only_and_keeps_base_path(monkeypatch):
    monkeypatch.delenv('AI_CCTV_URL', raising=False)
    client = TestClient(create_app())
    assert client.get('/api/health').status_code == 503
    monkeypatch.setenv('AI_CCTV_URL', 'http://bound-ai.internal/base/')
    assert service_url('health') == 'http://bound-ai.internal/base/health'
    assert service_url('/analyze') == 'http://bound-ai.internal/base/analyze'


def test_public_gateway_preserves_paths_and_routes_only_known_endpoints(monkeypatch):
    monkeypatch.setenv('AI_CCTV_URL', 'http://ai.internal/')
    calls = []
    def handler(request):
        calls.append((request.method, request.url.path))
        return httpx.Response(200, json={'status':'ok','inference_available':True,'weights_present':True})
    client = TestClient(create_app(httpx.MockTransport(handler)))
    data = client.get('/api/health').json()
    assert data['max_upload_bytes'] == MAX_UPLOAD_BYTES
    assert data['analysis_delivery'] == 'inline'
    assert client.get('/api/replay/simulation').status_code == 200
    assert client.get('/api/replay/not-a-mode').status_code == 404
    assert client.get('/api/jobs/old-id').status_code == 410
    assert client.get('/api/jobs/old-id/evidence').status_code == 410
    assert client.get('/api/not-real').status_code == 404
    assert client.get('/').status_code == 404
    assert calls == [('GET','/health'),('GET','/replay/simulation')]


def test_upload_is_forwarded_as_multipart_and_returns_inline_evidence(monkeypatch):
    monkeypatch.setenv('AI_CCTV_URL', 'http://ai.internal/binding')
    def handler(request):
        assert request.url.path == '/binding/analyze'
        assert b'file-bytes' in request.content and b'CYB-DEMO-02' in request.content
        assert b'name="dwell_seconds"' in request.content
        return httpx.Response(200,json={'status':'complete','mode':'real_yolo_inference','simulated':False,'events':[],'evidence_data_url':'data:image/jpeg;base64,YWJj'})
    client = TestClient(create_app(httpx.MockTransport(handler)))
    r=client.post('/api/analyze',data={'media_type':'image','stop_id':'CYB-DEMO-02'},files={'file':('test.jpg',b'file-bytes','image/jpeg')})
    assert r.status_code == 200 and r.json()['status'] == 'complete'
    assert 'ai.internal' not in r.text


def test_oversize_empty_and_wrong_media_rejected_before_forward(monkeypatch):
    monkeypatch.setenv('AI_CCTV_URL', 'http://ai.internal')
    def handler(request):
        raise AssertionError('Rejected uploads must not reach AI service')
    client=TestClient(create_app(httpx.MockTransport(handler)))
    assert client.post('/api/analyze',data={'media_type':'image'},files={'file':('x.jpg',b'x'*(MAX_UPLOAD_BYTES+1))}).status_code == 413
    assert client.post('/api/analyze',data={'media_type':'image'},files={'file':('x.jpg',b'')}).status_code == 422
    assert client.post('/api/analyze',data={'media_type':'audio'},files={'file':('x.jpg',b'x')}).status_code == 422


@pytest.mark.parametrize('failure,status', [('timeout',504),('network',503),('bad-json',502),('invalid-shape',502),('unavailable',503)])
def test_upstream_failures_are_honest(monkeypatch,failure,status):
    monkeypatch.setenv('AI_CCTV_URL','http://ai.internal')
    def handler(request):
        if failure=='timeout':raise httpx.ReadTimeout('test')
        if failure=='network':raise httpx.ConnectError('test')
        if failure=='bad-json':return httpx.Response(200,text='<html>not JSON</html>')
        if failure=='invalid-shape':return httpx.Response(200,json=[])
        return httpx.Response(503,json={'detail':'Detector unavailable'})
    client=TestClient(create_app(httpx.MockTransport(handler)))
    assert client.post('/api/analyze',data={'media_type':'image'},files={'file':('x.jpg',b'x')}).status_code==status


def test_service_routing_and_binding_contract():
    config=json.loads((ROOT/'vercel.json').read_text())
    assert set(config['services'])=={'ai-cctv','backend','frontend'}
    assert config['services']['backend']['bindings']==[{'type':'service','service':'ai-cctv','format':'url','env':'AI_CCTV_URL'}]
    assert 'bindings' not in config['services']['frontend']
    assert [x['destination']['service'] for x in config['rewrites']]==['backend','backend','frontend']
    assert all(x['destination']['service']!='ai-cctv' for x in config['rewrites'])
    assert config['rewrites'][-1]['source']=='/(.*)'
    assert not set(config).intersection({'functions','framework','installCommand','buildCommand','devCommand','outputDirectory','ignoreCommand'})


def test_vercel_entrypoint_does_not_import_local_inference_modules():
    import os
    import subprocess
    environment = {**os.environ, 'VERCEL': '1'}
    environment.pop('AI_CCTV_URL', None)
    code = '''
import sys
from fastapi.testclient import TestClient
from backend.main import app
client = TestClient(app)
assert client.get('/api/health').status_code == 503
assert client.get('/api/unknown').status_code == 404
assert not {'torch', 'cv2', 'ultralytics', 'local_api', 'naikready_local_api'}.intersection(sys.modules)
'''
    completed = subprocess.run([sys.executable, '-c', code], cwd=ROOT, env=environment,
                               capture_output=True, text=True, timeout=30)
    assert completed.returncode == 0, completed.stderr
