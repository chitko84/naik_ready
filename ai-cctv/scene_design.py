"""Illustrated bus-stop artwork for the existing four simulation scenarios.
All detection inputs and timings intentionally match the original demonstration.
This is a drawing, not CCTV footage and not an AI inference result.
"""
import cv2
import numpy as np
from core import Detection
W,H=1120,630


def color(hex_value):
    s=hex_value.lstrip('#')
    return tuple(int(s[i:i+2],16) for i in (4,2,0))


def poly(im,points,fill,stroke=None):
    pts=np.array(points,np.int32)
    cv2.fillPoly(im,[pts],color(fill),lineType=cv2.LINE_AA)
    if stroke:cv2.polylines(im,[pts],True,color(stroke),1,cv2.LINE_AA)


def text(im,value,xy,size=.45,tone='#929fb8',weight=1):
    cv2.putText(im,value,xy,cv2.FONT_HERSHEY_SIMPLEX,size,color(tone),weight,cv2.LINE_AA)


def line(im,a,b,tone='#596279',width=1):
    cv2.line(im,a,b,color(tone),width,cv2.LINE_AA)


def base_scene():
    im=np.zeros((H,W,3),np.uint8)
    # A restrained dusk palette; deterministic asphalt grain is drawn artwork.
    rng=np.random.default_rng(17)
    for y in range(H):
        v=y/H
        im[y,:]=np.array([31+7*v,25+4*v,23+3*v],dtype=np.uint8)
    grain=rng.integers(-2,3,(H,W,1),dtype=np.int16)
    im=np.clip(im.astype(np.int16)+grain,0,255).astype(np.uint8)
    # Background facades and pavement, deliberately diagrammatic.
    cv2.rectangle(im,(0,65),(W,213),color('#181d2a'),-1)
    for x in range(700,1100,56):
        cv2.rectangle(im,(x,76+(x%3)*8),(x+36,208),color('#1d2432'),-1)
        for yy in (96,120,144,168):
            for xx in (x+7,x+21):cv2.rectangle(im,(xx,yy),(xx+5,yy+7),color('#35384d'),-1)
    poly(im,[(0,214),(1120,214),(1120,268),(0,268)],'#282e3a')
    for x in range(-100,1200,95):line(im,(x,214),(x+56,267),'#353a46')
    line(im,(0,269),(1120,269),'#757386',3)
    line(im,(0,275),(1120,275),'#10151f',3)
    # Transparent shelter panels with vertical mullions and a lit roof edge.
    poly(im,[(95,127),(505,127),(505,247),(95,247)],'#242b3a','#4a5068')
    for x in (115,244,373,494):
        line(im,(x,135),(x,248),'#8990a4',4)
        line(im,(x+4,135),(x+4,248),'#40465a')
    for x in (130,260,390):
        line(im,(x,150),(x+65,215),'#343d52')
        line(im,(x+8,150),(x+73,215),'#2e374b')
    poly(im,[(70,110),(496,110),(535,128),(104,128)],'#555d75','#8388a0')
    line(im,(105,130),(531,130),'#b3a9de',2)
    poly(im,[(70,110),(104,128),(104,137),(70,119)],'#3b4259')
    cv2.rectangle(im,(168,207),(435,215),color('#444a61'),-1)
    for x in (190,406):line(im,(x,216),(x,246),'#575d74',3)
    cv2.rectangle(im,(145,142),(333,185),color('#151b26'),-1)
    cv2.rectangle(im,(145,142),(148,185),color('#a79bdd'),-1)
    text(im,'NaikReady 5G',(159,164),.58,'#e0dbf1')
    text(im,'ACCESSIBLE JOURNEYS',(159,179),.29,'#9298b0')
    # Assistance pedestal, explicitly a concept prop in this illustrated scene.
    poly(im,[(585,129),(615,129),(625,140),(625,246),(585,246)],'#3c4257','#77758e')
    cv2.circle(im,(603,156),9,color('#536e71'),-1,cv2.LINE_AA)
    cv2.circle(im,(603,156),4,color('#9be0c9'),-1,cv2.LINE_AA)
    text(im,'HELP',(591,182),.27,'#c7cce0')
    line(im,(592,194),(615,194),'#6b6c88')
    # Tactile strip; no claim of a physically installed accessible stop.
    cv2.rectangle(im,(696,250),(1080,259),color('#74664c'),-1)
    for x in range(700,1080,9):line(im,(x,251),(x,257),'#b69c64')
    text(im,'CYBERJAYA / CONCEPT STOP',(748,192),.43,'#b6b7cc')
    text(im,'Illustration - not a real CCTV recording',(748,213),.34,'#7b879f')
    # Road furniture and lane direction.
    for x in (52,674,1060):
        cv2.ellipse(im,(x+2,264),(12,3),0,0,360,color('#111823'),-1)
        line(im,(x,247),(x,265),'#777a8b',5)
        line(im,(x-2,245),(x+2,245),'#c5c2c8',2)
    for x in range(0,W,145):
        poly(im,[(x,545),(x+75,545),(x+74,549),(x,549)],'#686e80')
    line(im,(956,426),(1035,426),'#42495e',3)
    poly(im,[(1035,426),(1016,417),(1016,435)],'#42495e')
    text(im,'BOARDING APPROACH',(876,458),.33,'#68738d')
    return im

BASE=base_scene()


def car(im,box):
    x1,y1,x2,y2=[int(v*s) for v,s in zip(box,[W,H,W,H])]
    cv2.ellipse(im,((x1+x2)//2,y2-5),((x2-x1)//2,13),0,0,360,color('#10141c'),-1,cv2.LINE_AA)
    pts=[(x1+4,y1+74),(x1+45,y1+57),(x1+87,y1+17),(x1+202,y1+17),(x1+244,y1+57),(x2-12,y1+70),(x2-2,y2-30),(x1+1,y2-30)]
    poly(im,pts,'#8c8caa','#c0b8d3')
    poly(im,[(x1+63,y1+57),(x1+98,y1+25),(x1+191,y1+25),(x1+224,y1+57)],'#242b3e','#666b87')
    line(im,(x1+148,y1+26),(x1+148,y1+57),'#b2acc9',4)
    line(im,(x1+151,y1+63),(x1+151,y2-38),'#5e647f')
    line(im,(x1+77,y1+64),(x1+77,y2-37),'#636881')
    line(im,(x1+174,y1+74),(x1+190,y1+74),'#cbc4d8',2)
    line(im,(x1+99,y1+74),(x1+115,y1+74),'#cbc4d8',2)
    line(im,(x1+23,y2-38),(x2-25,y2-38),'#b1a9c7',2)
    for x in (x1+60,x2-59):
        cv2.circle(im,(x,y2-26),25,color('#121721'),-1,cv2.LINE_AA)
        cv2.circle(im,(x,y2-26),16,color('#697188'),-1,cv2.LINE_AA)
        cv2.circle(im,(x,y2-26),11,color('#2b3345'),-1,cv2.LINE_AA)
        for a,b in [((x-8,y2-26),(x+8,y2-26)),((x,y2-34),(x,y2-18))]:line(im,a,b,'#a6a7b9')
    line(im,(x1+5,y1+83),(x1+20,y1+83),'#e98e9e',4)
    line(im,(x2-20,y1+84),(x2-5,y1+84),'#e8dfbb',4)
    line(im,(x1+235,y1+55),(x1+248,y1+51),'#b6aec8',3)


def motorcycle(im,box):
    x1,y1,x2,y2=[int(v*s) for v,s in zip(box,[W,H,W,H])]
    cy=y2-21;back=x1+29;front=x2-27
    cv2.ellipse(im,((x1+x2)//2,y2+1),((x2-x1)//2,7),0,0,360,color('#11151d'),-1)
    for x in (back,front):
        cv2.circle(im,(x,cy),21,color('#10151e'),-1,cv2.LINE_AA)
        cv2.circle(im,(x,cy),14,color('#737a90'),2,cv2.LINE_AA)
        cv2.circle(im,(x,cy),5,color('#9096a8'),-1,cv2.LINE_AA)
    poly(im,[(x1+31,y1+65),(x1+80,y1+70),(x1+91,y1+89),(x1+46,y1+91)],'#aa7892','#d4a4b6')
    poly(im,[(x1+78,y1+50),(x1+111,y1+53),(x1+126,y1+67),(x1+113,y1+80),(x1+83,y1+73)],'#a095cd','#c5b6eb')
    poly(im,[(x1+69,y1+84),(x1+104,y1+84),(x1+115,y1+111),(x1+77,y1+111)],'#62697e','#9299ad')
    for yy in range(y1+88,y1+109,5):line(im,(x1+77,yy),(x1+103,yy),'#aab0bd')
    line(im,(back,cy),(x1+65,y1+80),'#a6a5b5',3)
    line(im,(front,cy),(x1+122,y1+39),'#b9b6c6',4)
    line(im,(x1+124,y1+40),(x1+143,y1+38),'#a7a1b7',3)
    line(im,(x1+128,y1+37),(x1+122,y1+21),'#9095ac',2)
    cv2.ellipse(im,(x1+120,y1+19),(8,4),0,0,360,color('#b0a8c9'),-1,cv2.LINE_AA)
    line(im,(x1+42,y1+59),(x1+78,y1+61),'#252a3d',7)
    line(im,(x1+92,y1+113),(x1+138,y1+115),'#9399ad',5)
    cv2.circle(im,(x1+135,y1+49),5,color('#e0d8bc'),-1,cv2.LINE_AA)
    cv2.ellipse(im,(front,cy-20),(22,4),0,180,360,color('#b8abd8'),2,cv2.LINE_AA)


def scene(t):
    im=BASE.copy();ds=[]
    if 4<=t<11:
        box=[.39,.47,.68,.73];ds=[Detection('car',box,None)];car(im,box)
    elif 13<=t<20:
        box=[.48,.52,.64,.74];ds=[Detection('motorcycle',box,None)];motorcycle(im,box)
    scenario='01 / CLEAR BUS STOP' if t<4 else '02 / CAR BLOCKING' if t<11 else '04 / OBSTRUCTION CLEARED' if t<13 else '03 / MOTORCYCLE BLOCKING' if t<20 else '04 / OBSTRUCTION CLEARED'
    text(im,scenario,(25,590),.65,'#ded9ed')
    text(im,'SIMULATED INPUT  /  Same zone and dwell engine as recorded-video mode',(25,614),.41,'#8e97b1')
    text(im,'NAIKREADY / SCENARIO LAB',(817,590),.35,'#82769f')
    return im,ds
