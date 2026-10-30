"""YOLO adapter and shared annotation. No simulated confidence scores."""
import cv2
import numpy as np
from core import Detection

class YoloDetector:
    def __init__(self,config):
        from ultralytics import YOLO
        self.cfg=config
        self.model=YOLO(config['model'])
        self.classes=[k for k,v in self.model.names.items() if v in ('car','motorcycle','bus','truck')]
        if not self.classes: raise ValueError('Model must expose COCO vehicle labels.')
    def predict(self,frame):
        r=self.model.predict(frame,conf=self.cfg['confidence'],imgsz=self.cfg['image_size'],classes=self.classes,device='cpu',verbose=False)[0]
        h,w=frame.shape[:2]; found=[]
        for b in r.boxes:
            x1,y1,x2,y2=b.xyxy[0].tolist()
            found.append(Detection(self.model.names[int(b.cls.item())],[x1/w,y1/h,x2/w,y2/h],float(b.conf.item())))
        return found

def annotate(frame,snapshot,config):
    out=frame.copy(); h,w=out.shape[:2]
    blocked=snapshot['status'] in ('BLOCKED','CLEARING')
    color=(75,90,245) if blocked else (180,210,30)
    poly=np.array([[int(x*w),int(y*h)] for x,y in config['zone']],dtype=np.int32)
    if config.get('show_zone',True):
        tint=out.copy(); cv2.fillPoly(tint,[poly],color); out=cv2.addWeighted(out,.87,tint,.13,0)
        for a,b in zip(poly,np.roll(poly,-1,axis=0)):
            length=float(np.linalg.norm(b-a))
            for start in range(0,int(length),18):
                end=min(start+10,length)
                cv2.line(out,tuple((a+(b-a)*start/max(length,1)).astype(int)),tuple((a+(b-a)*end/max(length,1)).astype(int)),color,2)
        cv2.putText(out,'VIRTUAL TEST ZONE' if config.get('source_context') else 'BOARDING ZONE',(poly[0][0],poly[0][1]-10),cv2.FONT_HERSHEY_SIMPLEX,.55,color,2)
    for d in snapshot['detections']:
        x1,y1,x2,y2=[int(v*s) for v,s in zip(d['bbox_normalized'],[w,h,w,h])]
        c=(75,90,245) if d['potential_obstruction'] else (235,210,60)
        cv2.rectangle(out,(x1,y1),(x2,y2),c,2)
        confidence='SCRIPTED' if d['confidence'] is None else f"{d['confidence']:.0%}"
        label=f"#{d['track_id']} {d['vehicle_type']} {confidence} / {d['stationary_seconds']:.1f}s"
        tw,th=cv2.getTextSize(label,cv2.FONT_HERSHEY_SIMPLEX,.43,1)[0]
        lx=max(0,min(x1,w-tw-12)); ly=max(83,y1)
        cv2.rectangle(out,(lx,ly-th-12),(lx+tw+10,ly),(26,32,39),-1)
        cv2.putText(out,label,(lx+5,ly-6),cv2.FONT_HERSHEY_SIMPLEX,.43,c,1)
    cv2.rectangle(out,(0,0),(w,62),(25,25,18),-1)
    title='Potential obstruction - review' if snapshot['status']=='BLOCKED' else snapshot['status'].replace('_',' ')
    mode='SIMULATION - scripted scene / detections' if snapshot['simulated'] else 'YOLO INFERENCE - recorded video'
    cv2.putText(out,title,(22,27),cv2.FONT_HERSHEY_SIMPLEX,.75,color,2)
    cv2.putText(out,f"{mode} | video t={snapshot['video_time_seconds']:.1f}s",(22,50),cv2.FONT_HERSHEY_SIMPLEX,.46,(225,225,225),1)
    if config.get('source_context'):
        cv2.rectangle(out,(0,h-32),(w,h),(25,25,18),-1)
        cv2.putText(out,config['source_context'],(14,h-11),cv2.FONT_HERSHEY_SIMPLEX,.43,(225,225,225),1)
    return out
