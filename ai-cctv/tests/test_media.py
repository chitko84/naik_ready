from pathlib import Path
import json
import cv2
ROOT=Path(__file__).resolve().parents[1]

def test_complete_delivered_videos():
    for folder,expected in [('simulation',288)]:
        cap=cv2.VideoCapture(str(ROOT/'outputs'/folder/'annotated.mp4'))
        assert cap.isOpened()
        count=0
        while True:
            ok,frame=cap.read()
            if not ok:break
            assert frame.size>0
            count+=1
        cap.release()
        assert count==expected

def test_scenario_transitions_and_real_provenance():
    events=json.loads((ROOT/'outputs/simulation/events.json').read_text())
    assert [e['video_time_seconds'] for e in events]==[7,12,16,21]
    assert all(e['simulated'] for e in events)
