import type {DemoState,TwinMode} from '../app/demoTypes';
/** Explicit scene selection has priority over historical outcomes, until a new operational action. */
export function getTwinMode(s:DemoState):TwinMode {
 if(s.sceneSelection?.stopId===s.selectedStopId)return s.sceneSelection.mode;
 const blocker=s.incidents.some(i=>i.stopId===s.selectedStopId&&i.detectionStatus==='POTENTIAL');
 const request=s.requests.find(r=>r.stopId===s.selectedStopId&&['REQUESTED','DRIVER_ACKNOWLEDGED','BOARDING_ATTEMPT'].includes(r.status));
 if(blocker)return request?'assistance':'blocked';
 if(request)return request.safeVerifiedAt?'resolved':'normal';
 return s.requests.find(r=>r.stopId===s.selectedStopId)?.status==='COMPLETED'?'resolved':'normal';
}
