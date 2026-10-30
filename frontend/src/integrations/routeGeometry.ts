import type {StopId} from '../app/demoTypes';
// Planning anchors in Cyberjaya; illustrative route geometry, never GPS telemetry.
export const STOP_POINTS:Record<StopId,[number,number]>={'CYB-DEMO-01':[2.9228,101.6553],'CYB-DEMO-02':[2.9277,101.6419]};
export const ROUTE_POINTS:[number,number][]=[[2.9277,101.6419],[2.9267,101.6429],[2.9255,101.6429],[2.9246,101.6438],[2.9246,101.6475],[2.9228,101.6490],[2.9228,101.6520],[2.9228,101.6553]];
export function routePosition(progress:number):[number,number]{const t=Math.max(0,Math.min(1,progress))*(ROUTE_POINTS.length-1);const i=Math.min(ROUTE_POINTS.length-2,Math.floor(t));const f=t-i;return [ROUTE_POINTS[i][0]+(ROUTE_POINTS[i+1][0]-ROUTE_POINTS[i][0])*f,ROUTE_POINTS[i][1]+(ROUTE_POINTS[i+1][1]-ROUTE_POINTS[i][1])*f]}
export function diagramView(zoom:number,stop?:StopId){const width=680/Math.max(1,zoom),height=425/Math.max(1,zoom);const [x,y]=stop?(stop==='CYB-DEMO-01'?[420,168]:[170,310]):[340,212.5];return `${x-width/2} ${y-height/2} ${width} ${height}`}
export function diagramBusPoint(progress:number):[number,number]{const p=Math.max(0,Math.min(1,progress));const t=p<=.5?p*2:(p-.5)*2;const points=p<=.5?[[170,310],[220,310],[228,254],[285,243]]:[[285,243],[340,233],[354,167],[420,168]];const value=(i:number)=>(1-t)**3*points[0][i]+3*(1-t)**2*t*points[1][i]+3*(1-t)*t*t*points[2][i]+t**3*points[3][i];return [value(0),value(1)]}
