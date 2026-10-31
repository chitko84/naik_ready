"""Exercise the hosted response path with the actual bundled CPU detector."""
import base64
from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'ai-cctv'))
import service


@pytest.mark.skipif(not service.health()['inference_available'], reason='Install local detector dependencies to run actual inference.')
def test_actual_detector_returns_inline_evidence_and_removes_temporary_files(monkeypatch, tmp_path):
    monkeypatch.setattr(service.vision, 'JOBS', tmp_path)
    image = ROOT / 'ai-cctv' / 'outputs' / 'runs' / 'da3235ed66' / 'observing.jpg'
    with TestClient(service.app) as client:
        response = client.post('/analyze', data={'media_type': 'image', 'stop_id': 'CYB-DEMO-02'},
                               files={'file': ('evidence.jpg', image.read_bytes(), 'image/jpeg')})
    assert response.status_code == 200, response.text
    result = response.json()
    assert result['mode'] == 'real_yolo_inference' and result['simulated'] is False
    assert result['delivery'] == 'inline' and result['frames_processed'] == 1
    assert result['stop_id'] == 'CYB-DEMO-02' and result['events'] == []
    assert 'evidence_url' not in result
    assert base64.b64decode(result['evidence_data_url'].split(',', 1)[1]).startswith(b'\xff\xd8')
    assert not list(tmp_path.iterdir())
