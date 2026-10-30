import { initialState } from './demoData';
import type { AssistanceRequest, DemoAction, DemoState, FailureReason, ObstructionIncident, Scenario, StopId, ValidAiEvent } from './demoTypes';
const now = () => new Date().toISOString();
const newId = (prefix: string) => `${prefix}-${(Date.now().toString(36) + Math.random().toString(36).slice(2,7)).toUpperCase()}`;
const record = (s: DemoState, type: string, message: string, detail?: string): DemoState => ({ ...s, activityLog:[{id:newId('LOG'),at:now(),type,message,detail},...s.activityLog].slice(0,120) });
function makeRequest(s: DemoState, stopId:StopId, type:AssistanceRequest['type'], note = ''): DemoState {
  const req: AssistanceRequest = {id:newId('NR'),stopId,routeId:'DEMO-R01',type,note,status:'REQUESTED',createdAt:now(),relatedIncidentIds:s.incidents.filter(i => i.stopId === stopId && i.detectionStatus==='POTENTIAL').map(i=>i.id)};
  return record({...s, selectedStopId:stopId,requests:[req,...s.requests],activeScenario:'ASSISTANCE'}, 'ASSISTANCE_REQUESTED', `New ${type.toLowerCase()} request`, req.id);
}
function updateRequest(s:DemoState, id:string, from:AssistanceRequest['status'][], status:AssistanceRequest['status'], event:string, detail?:string): DemoState {
  const request = s.requests.find(r=>r.id===id && from.includes(r.status));
  if (!request) return s;
  if ((status==='BOARDING_ATTEMPT'||status==='COMPLETED') && (s.incidents.some(i=>i.stopId===request.stopId&&i.detectionStatus==='POTENTIAL') || !request.safeVerifiedAt)) return s;
  const timestamp=now();
  const updated:AssistanceRequest = {...request,status,
    ...(status==='DRIVER_ACKNOWLEDGED'? {acknowledgedAt:timestamp} : {}),
    ...(status==='BOARDING_ATTEMPT'? {boardingStartedAt:timestamp} : {}),
    ...(status==='COMPLETED' || status==='UNABLE_TO_BOARD'? {completedAt:timestamp} : {}),
    ...(status==='CANCELLED'? {cancelledAt:timestamp} : {}),
    ...(status==='UNABLE_TO_BOARD' && detail ? {failureReason:detail as FailureReason} : {})};
  const next = {...s,requests:s.requests.map(r=>r.id===id?updated:r), activeScenario: (status==='COMPLETED'?'BOARDING_COMPLETED':status==='UNABLE_TO_BOARD'?'BOARDING_FAILED':status==='DRIVER_ACKNOWLEDGED'?'ACKNOWLEDGED':s.activeScenario) as Scenario};
  return record(next,event,`${status==='COMPLETED'?'Boarding confirmed': status==='UNABLE_TO_BOARD'?'Unable to board':status==='DRIVER_ACKNOWLEDGED'?'Driver acknowledged':status==='BOARDING_ATTEMPT'?'Boarding attempt started':'Request cancelled'} · ${id}`,detail);
}
function obstruct(s: DemoState, objectClass:'car'|'motorcycle'|'truck', stopId:StopId, imported?:ValidAiEvent):DemoState {
  if (imported && s.importedEventIds.includes(imported.event_id)) return s;
  const incident: ObstructionIncident = {
    id:imported?.event_id ?? newId('INC'), eventId:imported?.event_id,episodeId:imported?.episode_id,stopId,routeId:'DEMO-R01',objectClass,
    confidence:imported?.object?.confidence, sourceMode:imported?.source_mode ?? 'manual_simulation',
    detectedAt:imported?.timestamp ?? now(),detectionStatus:'POTENTIAL',driverAcknowledged:false,
    reviewStatus:imported?.review_status ?? 'PENDING_OPERATOR_REVIEW',operatorNotes:'',
    dwellSeconds:imported?.zone?.dwell_seconds,overlapRatio:imported?.zone?.overlap_ratio};
  const next:DemoState = {...s,activeScenario:objectClass==='car'?'CAR_BLOCKING':'MOTORCYCLE_BLOCKING',incidents:[incident,...s.incidents],requests:s.requests.map(r=>r.stopId===stopId?{...r,safeVerifiedAt:undefined,relatedIncidentIds:[...r.relatedIncidentIds,incident.id]}:r),
    importedEventIds:imported?[...s.importedEventIds,imported.event_id]:s.importedEventIds};
  return record(next,'OBSTRUCTION_DETECTED',`Potential ${objectClass} obstruction — verify on arrival`,incident.id);
}
function clearObstruction(s:DemoState, id?:string):DemoState {
  if (id && !s.incidents.some(i=>i.id===id && i.detectionStatus==='POTENTIAL')) return s;
  if (!id && !s.incidents.some(i=>i.stopId===s.selectedStopId&&i.detectionStatus==='POTENTIAL')) return s;
  const incidents = s.incidents.map(i => (i.detectionStatus==='POTENTIAL' && (id?i.id===id:i.stopId===s.selectedStopId))?{...i,detectionStatus:'CLEARED' as const,clearedAt:now()}:i);
  return record({...s,incidents,activeScenario:'NORMAL'},'OBSTRUCTION_CLEARED','Potential obstruction marked cleared in simulation');
}
function ensureReq(s:DemoState):{ s:DemoState; id:string }{
  const current=s.requests.find(r=>r.stopId===s.selectedStopId&&!['COMPLETED','UNABLE_TO_BOARD','CANCELLED'].includes(r.status));
  if(current) return {s,id:current.id};
  const next=makeRequest(s,s.selectedStopId,'Wheelchair / Ramp');
  return {s:next,id:next.requests[0].id};
}
function applyPreset(s:DemoState,scenario:Scenario):DemoState {
  if(scenario==='NORMAL')return record({...clearObstruction(s),activeScenario:'NORMAL'},'SCENARIO','Normal simulation selected');
  if(scenario==='CAR_BLOCKING'||scenario==='MOTORCYCLE_BLOCKING')return obstruct(s,scenario==='CAR_BLOCKING'?'car':'motorcycle',s.selectedStopId);
  // Establish the selected scene before creating a passenger request, so related alerts remain linked.
  if(scenario==='BOARDING_FAILED' && !s.incidents.some(i=>i.stopId===s.selectedStopId && i.detectionStatus==='POTENTIAL')) s=obstruct(s,'car',s.selectedStopId);
  if(scenario==='BOARDING_COMPLETED' && s.incidents.some(i=>i.detectionStatus==='POTENTIAL')) s=clearObstruction(s);
  let {s:next,id}=ensureReq(s);
  if(scenario==='ASSISTANCE')return next;
  const req=next.requests.find(r=>r.id===id);
  if(req?.status==='REQUESTED')next=updateRequest(next,id,['REQUESTED'],'DRIVER_ACKNOWLEDGED','DRIVER_ACKNOWLEDGED');
  if(scenario==='ACKNOWLEDGED')return next;
  if(scenario==='BOARDING_COMPLETED')next={...next,requests:next.requests.map(r=>r.id===id?{...r,safeVerifiedAt:now()}:r)};
  if(scenario==='BOARDING_FAILED')return updateRequest(next,id,['DRIVER_ACKNOWLEDGED','BOARDING_ATTEMPT'],'UNABLE_TO_BOARD','BOARDING_FAILED','Blocked Boarding Zone');
  if(next.requests.find(r=>r.id===id)?.status==='DRIVER_ACKNOWLEDGED')next=updateRequest(next,id,['DRIVER_ACKNOWLEDGED'],'BOARDING_ATTEMPT','BOARDING_ATTEMPT');
  return scenario==='BOARDING_COMPLETED'
    ? updateRequest(next,id,['BOARDING_ATTEMPT'],'COMPLETED','BOARDING_COMPLETED')
    : updateRequest(next,id,['BOARDING_ATTEMPT'],'UNABLE_TO_BOARD','BOARDING_FAILED','Blocked Boarding Zone');
}
function reduceAction(s:DemoState, action:DemoAction):DemoState {
  switch(action.type){
    case 'SELECT_TWIN_MODE': {
      const selected=s.sceneSelection;
      if(selected?.stopId===s.selectedStopId&&selected.mode===action.mode)return s;
      let next=s;
      if(action.mode==='normal')next=clearObstruction(s);
      if(action.mode==='blocked'&&!s.incidents.some(i=>i.stopId===s.selectedStopId&&i.detectionStatus==='POTENTIAL'))next=obstruct(s,'car',s.selectedStopId);
      if(action.mode==='assistance'){
        if(!s.incidents.some(i=>i.stopId===s.selectedStopId&&i.detectionStatus==='POTENTIAL'))next=obstruct(s,'car',s.selectedStopId);
        next=ensureReq(next).s;
      }
      if(action.mode==='resolved')next=applyPreset(s,'BOARDING_COMPLETED');
      return record({...next,sceneSelection:{stopId:s.selectedStopId,mode:action.mode}},'SCENE_SELECTED',`Boarding scene: ${action.mode}`);
    }
    case 'SELECT_STOP': return {...s,selectedStopId:action.stopId};
    case 'REQUEST': return makeRequest(s,action.stopId,action.assistanceType,action.note.slice(0,140));
    case 'ACKNOWLEDGE': return updateRequest(s,action.id,['REQUESTED'],'DRIVER_ACKNOWLEDGED','DRIVER_ACKNOWLEDGED');
    case 'RESTORE': return action.state;
    case 'VERIFY_BOARDING': {
      const r=s.requests.find(r=>r.id===action.id&&r.status==='DRIVER_ACKNOWLEDGED');
      if(!r||s.incidents.some(i=>i.stopId===r.stopId&&i.detectionStatus==='POTENTIAL'))return s;
      return record({...s,requests:s.requests.map(x=>x.id===r.id?{...x,safeVerifiedAt:now()}:x)},'ZONE_VERIFIED','Driver verified alignment and ramp readiness while stationary',r.id);
    }
    case 'COORDINATE': {
      if(!action.assignee.trim()||!s.incidents.some(i=>i.id===action.id&&i.detectionStatus==='POTENTIAL'))return s;
      return record({...s,incidents:s.incidents.map(i=>i.id===action.id?{...i,assignedTo:action.assignee.trim().slice(0,80),coordinatedAt:now(),reviewStatus:'REVIEWED'}:i)},'RESPONSE_ASSIGNED',`Response assigned to ${action.assignee.trim().slice(0,80)}`,action.id);
    }
    case 'BEGIN_BOARDING': return updateRequest(s,action.id,['DRIVER_ACKNOWLEDGED'],'BOARDING_ATTEMPT','BOARDING_ATTEMPT');
    case 'COMPLETE': return updateRequest(s,action.id,['BOARDING_ATTEMPT'],'COMPLETED','BOARDING_COMPLETED');
    case 'FAIL': return updateRequest(s,action.id,['DRIVER_ACKNOWLEDGED','BOARDING_ATTEMPT'],'UNABLE_TO_BOARD','BOARDING_FAILED',action.reason);
    case 'CANCEL': return updateRequest(s,action.id,['REQUESTED'],'CANCELLED','CANCELLED');
    case 'OBSTRUCT': return obstruct(s,action.objectClass,action.stopId,action.imported);
    case 'CLEAR_OBSTRUCTION': return clearObstruction(s,action.id);
    case 'IMPORT_CLEAR': {
      if(s.importedEventIds.includes(action.event.event_id)) return s;
      const targets=s.incidents.filter(i=>i.stopId===action.event.stop_id && i.detectionStatus==='POTENTIAL' && i.sourceMode===action.event.source_mode && (action.event.episode_id?i.episodeId===action.event.episode_id:i.eventId!==undefined) && Date.parse(i.detectedAt)<=Date.parse(action.event.timestamp));
      const updated=targets.length?targets.reduce((acc,i)=>clearObstruction(acc,i.id),s):record(s,'OBSTRUCTION_CLEARED','Clear event recorded; no matching active sensor episode');
      return {...updated,importedEventIds:[...updated.importedEventIds,action.event.event_id]};
    }
    case 'ACK_WARNING': {
      if(!s.incidents.some(i=>i.id===action.id && !i.driverAcknowledged))return s;
      return record({...s,incidents:s.incidents.map(i=>i.id===action.id?{...i,driverAcknowledged:true}:i)},'WARNING_ACKNOWLEDGED','Driver reviewed potential obstruction',action.id);
    }
    case 'REVIEW_INCIDENT': {
      if(!s.incidents.some(i=>i.id===action.id))return s;
      return record({...s,incidents:s.incidents.map(i=>i.id===action.id?{...i,reviewStatus:'REVIEWED' as const,operatorNotes:action.note===undefined?i.operatorNotes:action.note.slice(0,500)}:i)},'OPERATOR_REVIEWED','Operator reviewed incident',action.id);
    }
    case 'REVIEW_REQUEST': {
      if(!s.requests.some(r=>r.id===action.id))return s;
      return record({...s,requests:s.requests.map(r=>r.id===action.id?{...r,operatorReviewed:r.status==='UNABLE_TO_BOARD'?true:r.operatorReviewed,operatorNotes:action.note===undefined?r.operatorNotes:action.note.slice(0,500)}:r)},'OPERATOR_REVIEWED','Operator saved assistance case notes',action.id);
    }
    case 'PRESET':return applyPreset(s,action.scenario);
    case 'GUIDE_START':return {...initialState, guidedStep:0,guidedOutcome:action.outcome};
    case 'GUIDE_NEXT': {
      if(s.guidedStep<0||s.guidedStep>=8)return s;
      const step=s.guidedStep;
      let next=s;
      if(step===0)next=obstruct(next,'car','CYB-DEMO-01');
      if(step===1)next=makeRequest(next,'CYB-DEMO-01','Wheelchair / Ramp','Please prepare ramp assistance.');
      if(step===3){ const req=next.requests[0]; if(req)next=updateRequest(next,req.id,['REQUESTED'],'DRIVER_ACKNOWLEDGED','DRIVER_ACKNOWLEDGED'); }
      if(step===4&&next.incidents[0])next=demoReducer(next,{type:'COORDINATE',id:next.incidents[0].id,assignee:'Station attendant'});
      if(step===5 && s.guidedOutcome==='success')next=clearObstruction(next);
      if(step===6){const req=next.requests[0];if(req){if(s.guidedOutcome==='success')next=demoReducer(next,{type:'VERIFY_BOARDING',id:req.id});next=updateRequest(next,req.id,['DRIVER_ACKNOWLEDGED'],'BOARDING_ATTEMPT','BOARDING_ATTEMPT');next=updateRequest(next,req.id,['DRIVER_ACKNOWLEDGED','BOARDING_ATTEMPT'],s.guidedOutcome==='success'?'COMPLETED':'UNABLE_TO_BOARD',s.guidedOutcome==='success'?'BOARDING_COMPLETED':'BOARDING_FAILED',s.guidedOutcome==='success'?undefined:'Blocked Boarding Zone');}}
      if(step===7){
        const incident=next.incidents[0]; const failed=next.requests.find(r=>r.status==='UNABLE_TO_BOARD');
        next=record({...next,incidents:next.incidents.map(i=>i.id===incident?.id?{...i,reviewStatus:'REVIEWED' as const,operatorNotes:'Reviewed in guided demo.'}:i), requests:next.requests.map(r=>r.id===failed?.id?{...r,operatorReviewed:true,operatorNotes:'Reviewed in guided demo.'}:r)},'OPERATOR_REVIEWED','Operator reviewed scenario outcome');
      }
      return {...next,guidedStep:step+1};
    }
    case 'RESET':return {...initialState,activityLog:[{id:newId('LOG'),at:now(),type:'DEMO_RESET',message:'Demo reset to a clear baseline'}]};
    default:return s;
  }
}
export function sceneForState(s:DemoState):Scenario {
  if(s.sceneSelection?.stopId===s.selectedStopId)return ({normal:'NORMAL',blocked:'CAR_BLOCKING',assistance:'ASSISTANCE',resolved:'BOARDING_COMPLETED'} as const)[s.sceneSelection.mode];
  const blocker=s.incidents.find(i=>i.stopId===s.selectedStopId&&i.detectionStatus==='POTENTIAL');
  const active=s.requests.find(r=>r.stopId===s.selectedStopId&&['REQUESTED','DRIVER_ACKNOWLEDGED','BOARDING_ATTEMPT'].includes(r.status));
  if(active)return active.status==='REQUESTED'?'ASSISTANCE':'ACKNOWLEDGED';
  if(blocker)return blocker.objectClass==='motorcycle'?'MOTORCYCLE_BLOCKING':'CAR_BLOCKING';
  const last=s.requests.find(r=>r.stopId===s.selectedStopId);
  return last?.status==='COMPLETED'?'BOARDING_COMPLETED':last?.status==='UNABLE_TO_BOARD'?'BOARDING_FAILED':'NORMAL';
}
export function demoReducer(s:DemoState,action:DemoAction):DemoState {
  let next=reduceAction(s,action);
  const operational=['REQUEST','ACKNOWLEDGE','VERIFY_BOARDING','BEGIN_BOARDING','COMPLETE','FAIL','CANCEL','OBSTRUCT','CLEAR_OBSTRUCTION','IMPORT_CLEAR','PRESET','GUIDE_START','GUIDE_NEXT','RESET'];
  if(next!==s&&operational.includes(action.type))next={...next,sceneSelection:undefined};
  return next===s?s:{...next,activeScenario:sceneForState(next)};
}
export function validStoredState(value:unknown):value is DemoState {
  if(!value||typeof value!=='object')return false;
  const s=value as DemoState;
  const stop=(v:unknown)=>['CYB-DEMO-01','CYB-DEMO-02'].includes(String(v));
  const date=(v:unknown)=>typeof v==='string'&&Number.isFinite(Date.parse(v));
  return (!s.sceneSelection||(stop(s.sceneSelection.stopId)&&['normal','blocked','assistance','resolved'].includes(s.sceneSelection.mode)))&&s.version===1&&stop(s.selectedStopId)&&Number.isInteger(s.guidedStep)&&s.guidedStep>=-1&&s.guidedStep<=8&&['success','failure'].includes(s.guidedOutcome)&&
    Array.isArray(s.requests)&&s.requests.every(r=>r&&typeof r.id==='string'&&stop(r.stopId)&&typeof r.type==='string'&&typeof r.note==='string'&&['REQUESTED','DRIVER_ACKNOWLEDGED','BOARDING_ATTEMPT','COMPLETED','UNABLE_TO_BOARD','CANCELLED'].includes(r.status)&&date(r.createdAt)&&Array.isArray(r.relatedIncidentIds))&&
    Array.isArray(s.incidents)&&s.incidents.every(i=>i&&typeof i.id==='string'&&stop(i.stopId)&&['car','motorcycle','truck'].includes(i.objectClass)&&['POTENTIAL','CLEARED'].includes(i.detectionStatus)&&date(i.detectedAt)&&typeof i.operatorNotes==='string')&&
    Array.isArray(s.activityLog)&&s.activityLog.every(l=>l&&typeof l.id==='string'&&typeof l.message==='string'&&typeof l.type==='string'&&date(l.at))&&
    Array.isArray(s.importedEventIds)&&s.importedEventIds.every(id=>typeof id==='string');
}
export function safeHydrate(): DemoState {
  try{
    const raw=localStorage.getItem('naikready-demo-v1');
    if(!raw)return initialState;
    const parsed:unknown=JSON.parse(raw);
    return validStoredState(parsed)?{...parsed,activeScenario:sceneForState(parsed)}:initialState;
  } catch {return initialState;}
}
