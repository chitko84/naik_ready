"""Deterministic zone / dwell logic. No model or UI dependencies."""
from dataclasses import dataclass
from math import hypot
import uuid

@dataclass
class Detection:
    label: str
    bbox: list  # normalized x1,y1,x2,y2
    confidence: float | None
    track_id: int | None = None


def inside(point, polygon):
    """Ray casting; boundary counts as inside."""
    x, y = point
    hit = False
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        cross = (x-a[0])*(b[1]-a[1])-(y-a[1])*(b[0]-a[0])
        if abs(cross) < 1e-9 and min(a[0],b[0])-1e-9 <= x <= max(a[0],b[0])+1e-9 and min(a[1],b[1])-1e-9 <= y <= max(a[1],b[1])+1e-9:
            return True
        if (a[1]>y) != (b[1]>y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
            hit = not hit
    return hit


def iou(a,b):
    w=max(0,min(a[2],b[2])-max(a[0],b[0])); h=max(0,min(a[3],b[3])-max(a[1],b[1]))
    inter=w*h
    return inter/max(1e-9,(a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-inter)


class ZoneMonitor:
    def __init__(self, config, source, simulated=False):
        self.cfg=config; self.source=source; self.simulated=simulated
        self.tracks={}; self.next_id=1; self.episode=None; self.clear_since=None
        self.last_time=-1
        self.run_id=uuid.uuid4().hex[:12]

    def update(self, detections, t):
        if t < self.last_time:
            raise ValueError('Video time must be monotonic; create a fresh monitor after seek/replay.')
        self.last_time=t
        for k in list(self.tracks):
            if t-self.tracks[k]['seen'] > self.cfg['track_timeout_seconds']:
                del self.tracks[k]
        # Greedy one-to-one IoU matching; suitable only for this fixed-camera prototype.
        pairs=[]
        for idx,d in enumerate(detections):
            for k,tr in self.tracks.items():
                score=iou(d.bbox,tr['bbox']) if d.label==tr['label'] else 0
                if score >= self.cfg['match_iou']:
                    pairs.append((score,idx,k))
        assigned={}; used=set()
        for _,idx,k in sorted(pairs,reverse=True):
            if idx not in assigned and k not in used:
                assigned[idx]=k; used.add(k)
        rows=[]; blockers=[]
        for idx,d in enumerate(detections):
            k=assigned.get(idx)
            anchor=((d.bbox[0]+d.bbox[2])/2,d.bbox[3])
            if k is None:
                k=self.next_id; self.next_id+=1
                self.tracks[k]={'label':d.label,'since':None,'reference':anchor}
            tr=self.tracks[k]; d.track_id=k
            in_zone=inside(anchor,self.cfg['zone'])
            eligible=in_zone and d.label in self.cfg['blocking_classes']
            if eligible:
                if tr['since'] is None or hypot(anchor[0]-tr['reference'][0],anchor[1]-tr['reference'][1]) > self.cfg['stationary_tolerance']:
                    tr['since']=t; tr['reference']=anchor
            else:
                tr['since']=None; tr['reference']=anchor
            dwell=0 if tr['since'] is None else t-tr['since']
            tr.update(bbox=d.bbox,seen=t)
            row={'track_id':k,'vehicle_type':d.label,'confidence':d.confidence,'bbox_normalized':d.bbox,'in_zone':in_zone,'stationary_seconds':round(dwell,2),'potential_obstruction':eligible and dwell>=self.cfg['dwell_seconds']}
            rows.append(row)
            if row['potential_obstruction']: blockers.append(row)
        events=[]
        if blockers:
            self.clear_since=None
            if self.episode is None:
                self.episode=f'{self.run_id}-{uuid.uuid4().hex[:8]}'
                events.append(self.event('obstruction_started',t,blockers))
            status='BLOCKED'
        elif self.episode:
            if self.clear_since is None: self.clear_since=t
            if t-self.clear_since >= self.cfg['clear_seconds']:
                events.append(self.event('obstruction_cleared',t,[]))
                self.episode=None; self.clear_since=None
                status='CLEAR'
            else: status='CLEARING'
        else:
            status='OBSERVING' if any(r['in_zone'] and r['vehicle_type'] in self.cfg['blocking_classes'] for r in rows) else 'CLEAR'
        return {'video_time_seconds':round(t,3),'status':status,'detections':rows,'events':events,'simulated':self.simulated}

    def event(self, kind,t,vehicles):
        return {'schema_version':'1.0','event_id':uuid.uuid4().hex,'episode_id':self.episode,'run_id':self.run_id,'event_type':kind,'stop_id':self.cfg['stop_id'],'zone_id':self.cfg['zone_id'],'video_time_seconds':round(t,3),'source':self.source,'simulated':self.simulated,'inference_mode':'scripted_simulation' if self.simulated else 'yolo_recorded_video','status':'BLOCKED' if vehicles else 'CLEAR','message':'Boarding Area Blocked' if vehicles else 'Obstruction cleared','vehicles':vehicles,'zone_normalized':self.cfg['zone'],'dwell_threshold_seconds':self.cfg['dwell_seconds'],'requires_human_review':True,'network':{'transport':'local_file','real_5g':False}}
