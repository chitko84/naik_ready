"""Translate sensor events to Min's v1.0 import array; no invented overlap or score."""
from datetime import datetime,timezone
import csv,io

def export_events(events):
    result=[]
    for e in events:
        cleared=e['event_type'] in ('obstruction_cleared','OBSTRUCTION_CLEARED')
        vehicle=next(iter(e.get('vehicles',[])),None)
        label=vehicle['vehicle_type'] if vehicle else None
        out={'schema_version':'1.0','event_id':e['event_id'],'episode_id':e['episode_id'],
             'event_type':'OBSTRUCTION_CLEARED' if cleared else 'OBSTRUCTION_DETECTED',
             'scenario_id':'NORMAL' if cleared else {'car':'CAR_BLOCKING','motorcycle':'MOTORCYCLE_BLOCKING'}.get(label,'VEHICLE_BLOCKING'),
             'stop_id':{'CYBERJAYA-DEMO-01':'CYB-DEMO-01','CYBERJAYA-DEMO-02':'CYB-DEMO-02'}.get(e.get('stop_id'),e.get('stop_id','CYB-DEMO-01')),'route_id':'DEMO-R01','timestamp':e.get('timestamp',datetime.now(timezone.utc).isoformat()),
             'video_time_seconds':e['video_time_seconds'],'source_mode':'manual_simulation' if e['simulated'] else 'recorded_video_model_inference',
             'timestamp_kind':'event_export_time','deployment_status':'prototype','zone':{'id':e.get('zone_id','boarding-zone-01'),'dwell_seconds':vehicle['stationary_seconds'] if vehicle else 0,'position_rule':'bottom_center_in_polygon'},
             'review_status':'PENDING_OPERATOR_REVIEW' if not cleared else 'SENSOR_CONDITION_CLEARED','is_demo':True}
        if vehicle and not cleared:
            out['object']={'class':label,'confidence':vehicle.get('confidence')}
        # Frontend normalizes null scripted confidence to an absent metric.
        result.append(out)
    return result

def history_rows(events):
    return [{'Clip time (s)':e['video_time_seconds'],'Event':e['event_type'],'Object':e.get('object',{}).get('class','—'),'Confidence':e.get('object',{}).get('confidence'),'Dwell (s)':e['zone']['dwell_seconds'],'Provenance':e['source_mode'],'Review':e['review_status']} for e in events]

def csv_bytes(events):
    rows=history_rows(events)
    if not rows:return b'Clip time (s),Event,Object,Confidence,Dwell (s),Provenance,Review\r\n'
    f=io.StringIO();w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    return f.getvalue().encode('utf-8-sig')
