import type { DemoState, Scenario } from '../app/demoTypes';
/** Integration contract for an externally supplied Digital Twin. No 3D package is required. */
export interface DigitalTwinSnapshot {
  scenarioId: Scenario;
  selectedStopId: DemoState['selectedStopId'];
  potentialObstructions: {id:string;stopId:string;objectClass:'car'|'motorcycle'|'truck'}[];
  assistanceMarkers: {requestId:string;stopId:string;status:string}[];
}
export function getDigitalTwinSnapshot(state: DemoState): DigitalTwinSnapshot {
  return {scenarioId:state.activeScenario,selectedStopId:state.selectedStopId,
    potentialObstructions:state.incidents.filter(i=>i.detectionStatus==='POTENTIAL').map(i=>({id:i.id,stopId:i.stopId,objectClass:i.objectClass})),
    assistanceMarkers:state.requests.filter(r=>!['CANCELLED'].includes(r.status)).map(r=>({requestId:r.id,stopId:r.stopId,status:r.status}))};
}
export type OnScenarioChange=(scenarioId: Scenario)=>void;
