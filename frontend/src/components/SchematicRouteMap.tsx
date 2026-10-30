import { useDemo } from '../app/demoContext';
import type { StopId } from '../app/demoTypes';
import {diagramBusPoint} from '../integrations/routeGeometry';
import { stopName } from '../app/demoData';
import { BusFront, MapPin, Maximize2, Radio } from 'lucide-react';
export default function RouteMap({compact=false,interactive=true,showLegend=true,routeProgress=.5,viewBox='0 0 680 425'}:{routeProgress?:number;viewBox?:string;compact?:boolean;interactive?:boolean;showLegend?:boolean}){
  const {state,dispatch,notify}=useDemo();
  const selected=state.selectedStopId;const bus=diagramBusPoint(routeProgress);
  const incidents=state.incidents.filter(i=>i.detectionStatus==='POTENTIAL');
  const requests=state.requests.filter(r=>['REQUESTED','DRIVER_ACKNOWLEDGED','BOARDING_ATTEMPT'].includes(r.status));
  const locations:{id:StopId;x:number;y:number}[]=[{id:'CYB-DEMO-01',x:420,y:168},{id:'CYB-DEMO-02',x:170,y:310}];
  return <div className={'route-map '+(compact?'route-map-compact':'')}>
    <div className="map-canvas">
      <svg viewBox={viewBox} role="img" aria-label="Illustrative Cyberjaya Demo Shuttle schematic route with Cyberjaya City Centre and MMU Area stops" preserveAspectRatio="xMidYMid meet">
        <defs><pattern id="map-grid" width="60" height="60" patternUnits="userSpaceOnUse" patternTransform="rotate(-12)"><path d="M0 0H60M0 0V60" stroke="#e0e9ec" strokeWidth="9" fill="none"/></pattern><linearGradient id="water" x1="0" y1="0" x2="1" y2="1"><stop stopColor="#bde8f5"/><stop offset="1" stopColor="#d9f2fb"/></linearGradient><filter id="route-shadow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="5"/></filter></defs>
        <rect width="680" height="425" fill="#f4f8f8"/><rect width="680" height="425" fill="url(#map-grid)" opacity="0.65"/>
        <path d="M-30 72Q105 92 130 167T300 238Q396 245 412 365T720 420" stroke="url(#water)" strokeWidth="63" fill="none"/>
        <path d="M-20 77Q100 104 131 167T300 239Q388 246 408 363T710 424" stroke="#8fcbdc" strokeWidth="3" opacity=".6" fill="none"/>
        <path d="M-10 347L110 267L252 298L335 205L400 113L531 85L694 23" stroke="#d2dddf" strokeWidth="34" fill="none"/>
        <path d="M-10 347L110 267L252 298L335 205L400 113L531 85L694 23" stroke="#fff" strokeWidth="24" fill="none"/>
        <path d="M70-15L106 105L190 193L266 405M265-15L262 110L348 214L500 443M-20 184L170 199L298 160L681 220M481-15L420 112L510 265L720 350" stroke="#fff" strokeWidth="17" fill="none"/>
        <path d="M70-15L106 105L190 193L266 405M265-15L262 110L348 214L500 443M-20 184L170 199L298 160L681 220M481-15L420 112L510 265L720 350" stroke="#dce6e8" strokeWidth="1.5" fill="none"/>
        <path d="M70 20L113 24L125 75L82 82zM280 22L345 32L352 86L300 79zM500 288L620 285L642 374L551 390zM22 255L87 259L68 332L4 317zM523 120L615 126L628 195L535 186z" fill="#cae9d0" opacity=".88"/>
        <path d="M20 22L65 39L45 95L-5 83zM324 302L377 282L397 333L354 360zM452 25L483 31L471 95L436 72zM595 4L674 22L659 78L602 68z" fill="#d7eedb"/>
        <text x="480" y="143" className="map-location-label">CYBERJAYA</text><text x="480" y="162" className="map-sub-label">CITY CENTRE</text>
        <text x="91" y="348" className="map-location-label">MMU AREA</text><text x="91" y="367" className="map-sub-label">UNIVERSITY DISTRICT</text>
        <text x="273" y="73" className="map-sub-label">CYBERJAYA LAKE</text><text x="531" y="254" className="map-sub-label">SMART CITY DISTRICT</text>
        <path d="M170 310C220 310 228 254 285 243C340 233 354 167 420 168" stroke="#9bd3f8" strokeWidth="18" fill="none" filter="url(#route-shadow)"/>
        <path d="M170 310C220 310 228 254 285 243C340 233 354 167 420 168" stroke="#fff" strokeWidth="10" fill="none" strokeLinecap="round"/>
        <path d="M170 310C220 310 228 254 285 243C340 233 354 167 420 168" stroke="#1678df" strokeWidth="6" fill="none" strokeLinecap="round" strokeDasharray="1 0"/>
        <g transform={`translate(${bus[0]-285} ${bus[1]-243})`}><circle cx="285" cy="243" r="18" fill="#0e72d9" stroke="white" strokeWidth="5"/>
        <rect x="275" y="235" width="20" height="16" rx="4" fill="none" stroke="white" strokeWidth="2.5"/><path d="M279 252v4m13-4v4M279 241h12" stroke="white" strokeWidth="2"/></g>
        {locations.map(loc=>{const active=loc.id===selected;const danger=incidents.some(i=>i.stopId===loc.id);const requested=requests.some(r=>r.stopId===loc.id);return <g key={loc.id} role={interactive?'button':undefined} aria-label={`Select ${stopName(loc.id)} stop`} tabIndex={interactive?0:undefined} onClick={()=>interactive&&dispatch({type:'SELECT_STOP',stopId:loc.id})} onKeyDown={e=>{if(interactive&&(e.key==='Enter'||e.key===' ')){e.preventDefault();dispatch({type:'SELECT_STOP',stopId:loc.id});}}} className={interactive?'map-marker map-marker-clickable':'map-marker'}><circle cx={loc.x} cy={loc.y} r={active?20:17} fill="#fff" stroke={danger?'#DD4052':active?'#1769E0':'#009b83'} strokeWidth="4"/><circle cx={loc.x} cy={loc.y} r="7" fill={danger?'#DD4052':active?'#1769E0':'#009b83'}/>{(danger||requested)&&<><circle cx={loc.x+19} cy={loc.y-21} r="12" fill={danger?'#DD4052':'#1769E0'} stroke="white" strokeWidth="3"/><text x={loc.x+19} y={loc.y-16.5} textAnchor="middle" fontSize="14" fontWeight="bold" fill="white">{danger?'!':'+'}</text></>}</g>})}
        <rect x="23" y="15" width="142" height="30" rx="15" fill="#fff" opacity=".95"/><circle cx="39" cy="30" r="4" fill="#159B72"/><text x="50" y="34" className="map-pill-text">DEMO-R01 · ILLUSTRATIVE</text>
      </svg>
      {interactive&&<button className="map-focus" title="Select Cyberjaya City Centre" aria-label="Focus on Cyberjaya City Centre" onClick={()=>{dispatch({type:'SELECT_STOP',stopId:'CYB-DEMO-01'});notify('Map focused on Cyberjaya City Centre')}}><Maximize2 size={17}/></button>}
      <div className="map-selected"><div className="map-selected-icon"><MapPin size={18}/></div><div><strong>{stopName(selected)}</strong><small>Selected demonstration bus stop</small></div><span className="map-selected-check">✓</span></div>
    </div>
    {showLegend&&<div className="map-legend"><span><i className="dot dot-green"/>Stop</span><span><i className="dot dot-blue"/>Demo route</span><span><i className="dot dot-red"/>Potential obstruction</span><span className="muted tiny"><Radio size={12}/> Illustrative, not GPS</span></div>}
  </div>;
}
