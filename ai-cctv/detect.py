"""python detect.py --input path/to/clip.mp4 --output outputs/real_test"""
import argparse
import json
import math
import tempfile
from pathlib import Path
import cv2
from core import ZoneMonitor
from vision import YoloDetector,annotate

def load_config(path):
    cfg=json.loads(Path(path).read_text())
    zone=cfg['zone']
    if len(zone)<3 or any(len(p)!=2 or any(not 0<=v<=1 for v in p) for p in zone):
        raise ValueError('Zone requires at least three normalized [x,y] vertices in [0,1].')
    area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(zone,zone[1:]+zone[:1])))/2
    if area<0.0001: raise ValueError('Zone has zero or negligible area.')
    for key in ('dwell_seconds','clear_seconds','track_timeout_seconds','stationary_tolerance'):
        if not math.isfinite(cfg[key]) or cfg[key]<=0: raise ValueError(f'{key} must be positive and finite')
    if not 0<cfg['confidence']<=1 or not 0<cfg['match_iou']<=1: raise ValueError('Confidence and IoU must be in (0,1].')
    return cfg

def process_video(path, cfg, output, callback=None):
    out=Path(output); out.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(path))
    try:
        if not cap.isOpened(): raise ValueError('Cannot open video. Use a local MP4/AVI/MOV recording.')
        fps=cap.get(cv2.CAP_PROP_FPS)
        if not math.isfinite(fps) or fps<=0: raise ValueError('Video has no valid FPS metadata; re-encode it first.')
        w,h=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        detector=YoloDetector(cfg); monitor=ZoneMonitor(cfg,Path(path).name,False)
        video=out/'annotated.mp4'
        with tempfile.NamedTemporaryFile(suffix='.mp4',delete=False) as f:temp_video=Path(f.name)
        writer=cv2.VideoWriter(str(temp_video),cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h))
        if not writer.isOpened(): raise RuntimeError('MP4 video encoder unavailable.')
        events=[]; statuses={}; i=0; captures=set()
        with (out/'frames.jsonl').open('w') as log:
            try:
                while True:
                    ok,frame=cap.read()
                    if not ok: break
                    snap=monitor.update(detector.predict(frame),i/fps)
                    annotated=annotate(frame,snap,cfg); writer.write(annotated)
                    log.write(json.dumps(snap)+'\n'); events.extend(snap['events'])
                    statuses[snap['status']]=statuses.get(snap['status'],0)+1
                    if snap['status'] not in captures:
                        cv2.imwrite(str(out/f"{snap['status'].lower()}.jpg"),annotated); captures.add(snap['status'])
                    if callback and i%max(1,int(fps/3))==0: callback(annotated,snap)
                    i+=1
            finally:
                writer.release()
                if temp_video.exists():
                    video.write_bytes(temp_video.read_bytes())
                    temp_video.unlink()
        if i==0: raise ValueError('No decodable video frames.')
        (out/'events.json').write_text(json.dumps(events,indent=2))
        (out/'effective_config.json').write_text(json.dumps(cfg,indent=2))
        summary={'mode':'real_yolo_inference','source':Path(path).name,'frames_processed':i,'fps_source':fps,'duration_seconds':i/fps,'status_frame_counts':statuses,'event_count':len(events),'model':cfg['model'],'simulated':False,'config':cfg,'note':'Potential zone obstructions only; no accessibility or 5G validation.'}
        (out/'summary.json').write_text(json.dumps(summary,indent=2))
        return summary
    finally: cap.release()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True); p.add_argument('--config',default='config.json'); p.add_argument('--output',default='outputs/real_test')
    a=p.parse_args()
    try: print(json.dumps(process_video(a.input,load_config(a.config),a.output),indent=2))
    except Exception as exc: p.exit(1,f'Detection failed: {exc}\n')
if __name__=='__main__': main()
