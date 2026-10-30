import json
from pathlib import Path
from event_export import export_events,csv_bytes
ROOT=Path(__file__).resolve().parents[1]
def test_contract():
    out=export_events(json.loads((ROOT/'outputs/simulation/events.json').read_text()))
    assert len(out)==4
    assert out[0]['event_type']=='OBSTRUCTION_DETECTED'
    assert out[0]['source_mode']=='manual_simulation'
    assert out[0]['object']['confidence'] is None
    assert out[1]['event_type']=='OBSTRUCTION_CLEARED'
    assert out[1]['scenario_id']=='NORMAL'
    assert 'object' not in out[1]
    assert out[0]['stop_id']=='CYB-DEMO-01'
    assert csv_bytes(out)

def test_ten_second_default_obstruction():
    from core import ZoneMonitor,Detection
    cfg=json.loads((ROOT/'config.json').read_text())
    assert cfg['dwell_seconds']==10
    m=ZoneMonitor(cfg,'authorized_test.mp4')
    events=[]
    for i in range(45):
        s=m.update([Detection('car',[.4,.5,.6,.7],.8)],i*.25)
        events.extend(s['events'])
    assert len(events)==1
    out=export_events(events)
    assert out[0]['event_type']=='OBSTRUCTION_DETECTED'
    assert out[0]['object']['confidence']==.8
    assert out[0]['video_time_seconds']==10
