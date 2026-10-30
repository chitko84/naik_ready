import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest
from core import Detection,ZoneMonitor,inside

@pytest.fixture
def cfg():
    config=json.loads((Path(__file__).resolve().parents[1]/'config.json').read_text())
    config['dwell_seconds']=3.0
    return config
def car(x=.39,label='car'):return Detection(label,[x,.47,x+.25,.73],.9)
def new(cfg):return ZoneMonitor(cfg,'test.mp4')
def feed(m,ds,start,end,step=.25):
    results=[]
    for i in range(round((end-start)/step)+1):results.append(m.update(ds,start+i*step))
    return results

def test_empty(cfg):assert new(cfg).update([],0)['status']=='CLEAR'
def test_dwell_threshold_and_single_start(cfg):
    m=new(cfg);r=feed(m,[car()],0,4)
    assert r[11]['status']=='OBSERVING'
    assert r[12]['status']=='BLOCKED'
    assert sum(len(s['events']) for s in r)==1
    assert len({s['detections'][0]['track_id'] for s in r})==1

def test_clear_debounce_same_episode(cfg):
    m=new(cfg);r=feed(m,[car()],0,3);episode=r[-1]['events'][0]['episode_id']
    assert m.update([],3.25)['status']=='CLEARING'
    r=feed(m,[],3.5,4.25)
    assert r[-1]['status']=='CLEAR'
    assert r[-1]['events'][0]['episode_id']==episode
    assert m.update([],4.5)['events']==[]
def test_motion_resets_dwell(cfg):
    m=new(cfg)
    for i in range(20):r=m.update([car(.3+i*.008)],i*.25)
    assert r['status']=='OBSERVING'
    assert not r['events']
def test_zone_exit_resets(cfg):
    m=new(cfg);feed(m,[car(.6)],0,2.75)
    m.update([car(.75)],3)  # overlapping box, same matched track, anchor exits zone
    assert m.update([car(.6)],3.25)['status']=='OBSERVING'
def test_timeout_not_counted_as_dwell(cfg):
    m=new(cfg);m.update([car()],0)
    r=m.update([car()],4)
    assert r['status']=='OBSERVING'
    assert r['detections'][0]['stationary_seconds']==0

def test_brief_dropout_does_not_emit_duplicate(cfg):
    m=new(cfg);feed(m,[car()],0,3)
    assert m.update([],3.25)['status']=='CLEARING'
    r=m.update([car()],3.5)
    assert r['status']=='BLOCKED' and not r['events']
def test_two_vehicles_not_merged(cfg):
    m=new(cfg);r=m.update([car(.26),car(.6)],0)
    assert len({d['track_id'] for d in r['detections']})==2

def test_motorcycle_blocks_bus_exempt(cfg):
    m=new(cfg);r=feed(m,[car(label='motorcycle')],0,3)
    assert r[-1]['status']=='BLOCKED'
    m=new(cfg);r=feed(m,[car(label='bus')],0,4)
    assert r[-1]['status']=='CLEAR'
    assert r[-1]['detections'][0]['vehicle_type']=='bus'
def test_zone_boundary():
    poly=[[0,0],[1,0],[1,1],[0,1]]
    assert inside((0,.5),poly)
    assert not inside((1.1,.5),poly)
def test_simulation_provenance(cfg):
    m=ZoneMonitor(cfg,'illustration',True);r=feed(m,[Detection('car',[.3,.4,.6,.7],None)],0,3)
    e=r[-1]['events'][0]
    assert e['simulated'] and e['inference_mode']=='scripted_simulation'
    assert e['vehicles'][0]['confidence'] is None
    assert not e['network']['real_5g']
def test_rewind_rejected(cfg):
    m=new(cfg);m.update([],1)
    with pytest.raises(ValueError):m.update([],0)
def test_different_vehicles_cannot_accumulate_dwell(cfg):
    m=new(cfg)
    for i in range(16):
        r=m.update([car(label='car' if i%2 else 'motorcycle')],i*.5)
    assert r['status']=='OBSERVING'
