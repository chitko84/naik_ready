import json
import sys
import time
from pathlib import Path
import cv2
from fastapi.testclient import TestClient
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from backend.main import app
client=TestClient(app)

def wait(job_id):
    for _ in range(240):
        r=client.get('/api/jobs/'+job_id)
        assert r.status_code==200
        data=r.json()
        if data['status'] in ('failed','complete'):
            assert data['status']=='complete',data
            return data
        time.sleep(.25)
    raise AssertionError('Analysis did not finish in 60 seconds')

def test_health_and_replays():
    assert client.get('/api/health').json()['weights_present']
    scripted=client.get('/api/replay/simulation').json()
    assert len(scripted['events'])==4
    assert scripted['events'][0]['object']['confidence'] is None
    assert scripted['events'][0]['stop_id']=='CYB-DEMO-01'
    actual=client.get('/api/replay/recorded').json()
    assert actual['events']==[]
    assert actual['summary']['simulated'] is False

def test_invalid_requests():
    assert client.get('/api/jobs/not-a-job').status_code==404
    assert client.post('/api/analyze',data={'media_type':'audio'},files={'file':('bad.jpg',b'abc','image/jpeg')}).status_code==422
    assert client.post('/api/analyze',data={'media_type':'image','zone':'[[0,0],[1,1]]'},files={'file':('bad.jpg',b'abc','image/jpeg')}).status_code==422
    assert client.post('/api/analyze',data={'media_type':'image','stop_id':'BAD'},files={'file':('bad.jpg',b'abc','image/jpeg')}).status_code==422
    assert client.get('/api/replay/unknown').status_code==404

def test_actual_image_inference():
    data=(ROOT/'ai-cctv/outputs/runs/da3235ed66/observing.jpg').read_bytes()
    r=client.post('/api/analyze',data={'media_type':'image','stop_id':'CYB-DEMO-02'},files={'file':('evidence.jpg',data,'image/jpeg')})
    assert r.status_code==202,r.text
    result=wait(r.json()['job_id'])
    assert result['mode']=='real_yolo_inference' and result['simulated'] is False
    assert result['frames_processed']==1 and result['events']==[]
    assert result['stop_id']=='CYB-DEMO-02'
    assert client.get(result['evidence_url']).headers['content-type']=='image/jpeg'
    print('ACTUAL_IMAGE_RESULT',json.dumps(result))

def test_actual_video_inference(tmp_path):
    # Controlled fixture exercises actual decoding and model calls, not field accuracy.
    frame=cv2.imread(str(ROOT/'ai-cctv/outputs/runs/da3235ed66/observing.jpg'))
    frame=cv2.resize(frame,(640,360))
    path=tmp_path/'clip.mp4'
    writer=cv2.VideoWriter(str(path),cv2.VideoWriter_fourcc(*'mp4v'),5,(640,360))
    assert writer.isOpened()
    for _ in range(15):writer.write(frame)
    writer.release()
    r=client.post('/api/analyze',data={'media_type':'video','dwell_seconds':2},files={'file':('clip.mp4',path.read_bytes(),'video/mp4')})
    assert r.status_code==202,r.text
    result=wait(r.json()['job_id'])
    assert result['frames_processed']==15
    assert result['media_type']=='video' and result['simulated'] is False
    print('ACTUAL_VIDEO_RESULT',json.dumps(result))

def test_bad_media_fails_honestly():
    r=client.post('/api/analyze',data={'media_type':'image'},files={'file':('bad.jpg',b'not an image','image/jpeg')})
    assert r.status_code==202
    job_id=r.json()['job_id']
    for _ in range(80):
        data=client.get('/api/jobs/'+job_id).json()
        if data['status']=='failed':
            assert 'decodable' in data['error'];break
        time.sleep(.1)
    else:raise AssertionError('Malformed image not rejected')

def test_built_routes_and_assets():
    for route in ['/','/passenger','/passenger/request','/passenger/status','/driver','/operator','/experience','/demo','/activity']:
        r=client.get(route);assert r.status_code==200 and '<html' in r.text.lower()
    for mode in ['normal','blocked','assistance','resolved']:
        r=client.get('/twin/'+mode+'.glb');assert r.status_code==200 and r.content[:4]==b'glTF'
