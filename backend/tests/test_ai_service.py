import base64
from pathlib import Path
import sys

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'ai-cctv'))
import service


@pytest.fixture
def client(monkeypatch,tmp_path):
    monkeypatch.setattr(service.vision,'JOBS',tmp_path)
    monkeypatch.setattr(service,'health',lambda:{'inference_available':True,'weights_present':True})
    class Detector:
        def predict(self,frame):return []
    monkeypatch.setattr(service.vision,'get_detector',lambda cfg:Detector())
    return TestClient(service.app)


def test_sync_image_pipeline_returns_inline_jpeg_and_cleans_job_files(client,tmp_path):
    ok,jpeg=cv2.imencode('.jpg',np.zeros((120,200,3),np.uint8));assert ok
    response=client.post('/analyze',data={'media_type':'image'},files={'file':('x.jpg',jpeg.tobytes(),'image/jpeg')})
    assert response.status_code==200,response.text
    result=response.json()
    assert result['status']=='complete' and result['delivery']=='inline'
    assert result['mode']=='real_yolo_inference' and result['simulated'] is False
    assert result['frames_processed']==1 and result['events']==[]
    assert 'evidence_url' not in result
    assert result['evidence_data_url'].startswith('data:image/jpeg;base64,')
    assert base64.b64decode(result['evidence_data_url'].split(',',1)[1])[:2]==b'\xff\xd8'
    assert not list(tmp_path.iterdir())


def test_decode_failure_cleans_files_and_is_not_simulated(client,tmp_path):
    response=client.post('/analyze',data={'media_type':'image'},files={'file':('bad.jpg',b'not an image')})
    assert response.status_code==422 and 'decodable' in response.json()['detail']
    assert not list(tmp_path.iterdir())


def test_service_rejects_invalid_configuration_and_size(client,tmp_path):
    for fields in [{'media_type':'audio'},{'media_type':'image','stop_id':'invalid'},{'media_type':'image','zone':'[[0,0],[0,0],[0,0]]'}]:
        assert client.post('/analyze',data=fields,files={'file':('x.jpg',b'x')}).status_code==422
    assert client.post('/analyze',data={'media_type':'image'},files={'file':('x.jpg',b'x'*(service.MAX_UPLOAD_BYTES+1))}).status_code==413
    assert not list(tmp_path.iterdir())


def test_busy_detector_does_not_queue_transient_job(client,tmp_path):
    service.capacity.acquire()
    try:
        response=client.post('/analyze',data={'media_type':'image'},files={'file':('x.jpg',b'x')})
        assert response.status_code==429
        assert not list(tmp_path.iterdir())
    finally:service.capacity.release()


def test_internal_api_has_no_background_job_polling(client):
    assert client.get('/api/jobs/'+'a'*32).status_code==404
    assert client.get('/docs').status_code==404
    response=client.get('/replay/recorded')
    assert response.status_code==200 and response.json()['mode']=='recorded_video_model_inference'
