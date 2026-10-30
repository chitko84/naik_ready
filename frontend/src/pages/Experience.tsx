import TransitPhoto from '../components/TransitPhoto';
import { Link } from 'react-router-dom';
import { Activity, ArrowRight, BusFront, Camera, CheckCircle2, CircleAlert, FileJson, Layers3, Radio, ScanLine, ShieldCheck, Sparkles, Wifi } from 'lucide-react';
import { useDemo } from '../app/demoContext';
import VisionConsole from '../components/VisionConsole';
import DigitalTwin from '../components/DigitalTwin';
import { DemoBadge, Panel, Tag } from '../components/UI';
import { stopName, formatTime } from '../app/demoData';

export default function Experience(){
  const {state}=useDemo();
  const incident=state.incidents.find(i=>i.stopId===state.selectedStopId&&i.detectionStatus==='POTENTIAL');
  const active=incident?.detectionStatus==='POTENTIAL';
  return <main className="page-container experience-page">
    <div className="page-titlebar"><div><span className="overline">CONNECTED BOARDING AWARENESS</span><h1>Digital Twin <span className="teal">& Vision AI</span></h1><p>A closer look at how a potential obstruction can affect a passenger's journey.</p></div><DemoBadge/></div>
    <div className="experience-feature-grid">
      <div className="experience-main"><div className="experience-panel-header"><div><span><Layers3 size={19}/> BOARDING ZONE VIEW</span><h2>{stopName(state.selectedStopId)}</h2></div><Tag tone={active?'warning':'teal'}>{active?'Potential obstruction':'No active advisory'}</Tag></div>
        <DigitalTwin large/>
        <div className="experience-description"><div><strong>Watch the boarding zone</strong><p>Explore the original Blender environment in 3D. The scene follows boarding-zone alerts and assistance progress at the selected stop.</p></div><Link to="/demo" className="btn btn-primary">Explore scenarios <ArrowRight size={17}/></Link></div>
      </div>

    </div>
    <VisionConsole/>
    <details className="simple-disclosure"><summary>About connectivity and boarding verification</summary><div className="disclosure-body">      <div className="experience-insights"><TransitPhoto photo="skyline" title="Connected to everyday life." subtitle="Kuala Lumpur · Urban mobility"/>
        <div className="insight-card"><div className="insight-icon"><Wifi size={25}/></div><span className="overline">CONNECTED MOBILITY</span><h3>Earlier awareness for every arrival.</h3><p>The proposed 5G system connects roadside awareness with driver and operator notifications to support timely responses.</p><div className="insight-small"><Radio size={14}/> Connectivity concept · No live network link</div></div>
        <div className="insight-card"><div className="insight-icon light"><ShieldCheck size={25}/></div><span className="overline">ACCESSIBILITY FIRST</span><h3>Human judgment stays essential.</h3><p>A potential obstruction warning prompts a check on arrival. Only the driver can verify that the boarding area is safe.</p></div>
      </div></div></details>
    <div className="experience-next"><Link to="/driver" className="btn btn-outline"><BusFront size={17}/> Driver dashboard</Link><Link to="/operator" className="btn btn-primary"><Activity size={17}/> Coordinate a response</Link><Link to="/activity" className="btn btn-outline"><FileJson size={17}/> Activity history</Link></div>
  </main>;
}
