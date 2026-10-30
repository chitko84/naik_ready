"""Create deterministic synthetic bus-stop media. Does NOT run YOLO."""
import json
import tempfile
from pathlib import Path
import cv2
import numpy as np
from core import Detection,ZoneMonitor
from vision import annotate

ROOT=Path(__file__).parent
FPS=12; SECONDS=24; W=1120; H=630

from scene_design import scene

def main():
    cfg=json.loads((ROOT/'config.json').read_text()); out=ROOT/'outputs'/'simulation';out.mkdir(parents=True,exist_ok=True)
    cfg['dwell_seconds']=3.0  # Existing short illustrated fixture, explicitly labelled in UI.
    # A bundled optional WebM preview must not outlive regenerated artwork.
    (out/'preview.webm').unlink(missing_ok=True)
    monitor=ZoneMonitor(cfg,'synthetic_bus_stop',True)
    with tempfile.NamedTemporaryFile(suffix='.mp4',delete=False) as f: temp_video=Path(f.name)
    writer=cv2.VideoWriter(str(temp_video),cv2.VideoWriter_fourcc(*'mp4v'),FPS,(W,H))
    if not writer.isOpened(): raise RuntimeError('Encoder unavailable')
    snapshots=[];events=[]
    marks={24:'01_clear_bus_stop',108:'02_car_blocking',144:'04_car_cleared',216:'03_motorcycle_blocking',270:'05_obstruction_cleared'}
    try:
        for i in range(FPS*SECONDS):
            t=i/FPS;frame,ds=scene(t);s=monitor.update(ds,t);frame=annotate(frame,s,cfg)
            writer.write(frame);snapshots.append(s);events.extend(s['events'])
            if i in marks: cv2.imwrite(str(out/(marks[i]+'.png')),frame)
    finally: writer.release()
    (out/'annotated.mp4').write_bytes(temp_video.read_bytes())
    temp_video.unlink()
    (out/'frames.jsonl').write_text(''.join(json.dumps(s)+'\n' for s in snapshots))
    (out/'events.json').write_text(json.dumps(events,indent=2))
    (ROOT/'outputs'/'sample_alert.json').write_text(json.dumps(events[0],indent=2))
    (out/'summary.json').write_text(json.dumps({'simulated':True,'model_executed':False,'frames':len(snapshots),'fps':FPS,'events':len(events),'description':'Illustrated scene and scripted boxes; real zone/dwell engine. Not AI accuracy evidence.'},indent=2))
    print(f'Created {len(snapshots)} simulated frames, {len(events)} transitions')
if __name__=='__main__':main()
