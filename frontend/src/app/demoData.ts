import type { AssistanceType, DemoState, StopId } from './demoTypes';
export const stops: { id: StopId; name: string; address: string; eta: number; short: string }[] = [
  { id:'CYB-DEMO-01', name:'Cyberjaya City Centre', address:'Cyberjaya, Selangor · Illustrative location', eta:6, short:'City Centre' },
  { id:'CYB-DEMO-02', name:'MMU Area', address:'Multimedia University Area · Illustrative location', eta:9, short:'MMU Area' }
];
export const assistanceTypes: { title: AssistanceType; description: string; icon: string }[] = [
  {title:'Wheelchair / Ramp',description:'Ramp access and boarding support',icon:'accessibility'},
  {title:'Extra Boarding Time',description:'A little more time to board',icon:'clock'},
  {title:'Low-Vision Guidance',description:'Verbal guidance and orientation',icon:'eye'},
  {title:'Stroller',description:'Help with boarding and storage',icon:'baby'},
  {title:'Luggage',description:'Support with bags and belongings',icon:'briefcase'},
  {title:'Other Assistance',description:'Tell the driver what you need',icon:'heart'}
];
export const initialState: DemoState = { version:1, activeScenario:'NORMAL', selectedStopId:'CYB-DEMO-01', requests:[], incidents:[], activityLog:[], importedEventIds:[], guidedStep:-1, guidedOutcome:'success' };
export const stopName = (id: StopId) => stops.find(stop => stop.id === id)?.name ?? id;
export const formatTime = (time: string) => new Date(time).toLocaleTimeString('en-MY', { hour: '2-digit', minute: '2-digit', hour12: true, timeZone: 'Asia/Kuala_Lumpur' });
export const requestLabels: Record<string,string> = { REQUESTED:'Awaiting driver', DRIVER_ACKNOWLEDGED:'Driver acknowledged', BOARDING_ATTEMPT:'Boarding in progress', COMPLETED:'Boarding completed', UNABLE_TO_BOARD:'Unable to board', CANCELLED:'Cancelled' };
