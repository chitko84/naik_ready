"""AI-generated scene assets with explicitly manual, scoreless overlays.
These hand-positioned polygons are presentation annotations, not YOLO results.
"""
from pathlib import Path
import cv2
import numpy as np
ROOT=Path(__file__).resolve().parent/'assets/photoreal'
SCENES={
 'Normal / Clear':('clear',[[.415,.96],[.545,.38],[.626,.38],[.855,.96]],None),
 'Car Blocking':('car',[[.26,.97],[.49,.4],[.657,.4],[.77,.97]],[.38,.38,.68,.76]),
 'Motorcycle Blocking':('motorcycle',[[.31,.93],[.51,.34],[.62,.34],[.80,.93]],[.465,.41,.585,.81]),
 'Obstruction Cleared':('cleared',[[.355,.94],[.505,.27],[.59,.27],[.86,.94]],None)
}

def render_photo(selection,zone=True,boxes=True):
    name,polygon,box=SCENES[selection]
    img=cv2.imread(str(ROOT/(name+'.png')))
    if img is None:raise FileNotFoundError(name+'.png')
    h,w=img.shape[:2];blocked=box is not None
    color=(70,64,221) if blocked else (114,155,21)
    if zone:
        points=np.array([[int(x*w),int(y*h)] for x,y in polygon],np.int32)
        overlay=img.copy();cv2.fillPoly(overlay,[points],color)
        img=cv2.addWeighted(img,.85,overlay,.15,0)
        for a,b in zip(points,np.roll(points,-1,axis=0)):
            length=np.linalg.norm(b-a)
            for start in range(0,int(length),25):
                aa=(a+(b-a)*start/max(1,length)).astype(int);bb=(a+(b-a)*min(start+14,length)/max(1,length)).astype(int)
                cv2.line(img,tuple(aa),tuple(bb),color,3,cv2.LINE_AA)
    if boxes and box:
        x1,y1,x2,y2=[int(v*s) for v,s in zip(box,[w,h,w,h])]
        cv2.rectangle(img,(x1,y1),(x2,y2),color,3)
        label=('car' if name=='car' else 'motorcycle')+' | MANUAL SIMULATION'
        tw=cv2.getTextSize(label,cv2.FONT_HERSHEY_SIMPLEX,.7,2)[0][0]
        cv2.rectangle(img,(x1,y1-38),(min(w,x1+tw+16),y1),color,-1)
        cv2.putText(img,label,(x1+8,y1-12),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),2,cv2.LINE_AA)
    # Persistent provenance remains visible in exported screenshots too.
    cv2.rectangle(img,(0,0),(w,43),(36,25,7),-1)
    cv2.putText(img,'AI-GENERATED SCENE  |  MANUAL SIMULATION  |  NO MODEL SCORE',(18,29),cv2.FONT_HERSHEY_SIMPLEX,.65,(255,255,255),1,cv2.LINE_AA)
    return img
