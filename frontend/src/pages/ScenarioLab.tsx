import PhotoBanner from '../components/PhotoBanner';
import { useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Accessibility, Activity, AlertTriangle, ArrowRight, ArrowUpRight, BusFront, Check,
  CheckCircle2, CircleAlert, FileJson, FlaskConical, Info, Play, RotateCcw, ShieldCheck,
  UploadCloud, Users, XCircle
} from 'lucide-react';
import { useDemo } from '../app/demoContext';
import type { Scenario, ValidAiEvent } from '../app/demoTypes';
import { formatTime } from '../app/demoData';
import { validateAiEvent } from '../integrations/eventValidator';
import DigitalTwin from '../components/DigitalTwin';
import ScenarioVisual from '../components/ScenarioVisual';
import { DemoBadge, Empty, Panel, Tag } from '../components/UI';

type ScenarioInfo = {id: Scenario; label: string; description: string; tone: string; icon: typeof BusFront; group: string};
const scenarios: ScenarioInfo[] = [
  {id:'NORMAL', label:'Normal conditions', description:'A clear curbside zone and an accessible bus arrival.', tone:'green',icon:ShieldCheck,group:'BASELINE'},
  {id:'CAR_BLOCKING',label:'Car blocking the zone',description:'See how a parked car creates a potential ramp-access risk.',tone:'red',icon:AlertTriangle,group:'OBSTRUCTION'},
  {id:'MOTORCYCLE_BLOCKING',label:'Motorcycle obstruction',description:'Explore an obstructed boarding area and driver advisory.',tone:'amber',icon:AlertTriangle,group:'OBSTRUCTION'},
  {id:'ASSISTANCE',label:'Assistance requested',description:'A passenger signals the need for wheelchair ramp support.',tone:'blue',icon:Accessibility,group:'PASSENGER'},
  {id:'ACKNOWLEDGED',label:'Driver acknowledged',description:"The driver accepts a passenger's assistance request.",tone:'teal',icon:CheckCircle2,group:'DRIVER'},
  {id:'BOARDING_COMPLETED',label:'Boarding completed',description:'Follow the journey to a recorded successful boarding.',tone:'green',icon:BusFront,group:'OUTCOME'},
  {id:'BOARDING_FAILED',label:'Unable to board',description:'An uncleared obstruction leads to an unsuccessful boarding.',tone:'red',icon:CircleAlert,group:'OUTCOME'}
];

type StepInfo = { title: string; description: string; action: string; link: string; linkText: string; role: string };
function guidedSteps(outcome: 'success' | 'failure'): StepInfo[] {
  return [
    {title:'A blocked boarding zone',description:'A car is detected near the bus stop, creating a potential obstruction advisory.',action:'Show obstruction alert',link:'/experience',linkText:'Explore the street view',role:'STREET VIEW'},
    {title:'A passenger needs support',description:'The passenger requests wheelchair ramp assistance at Cyberjaya City Centre.',action:'Send assistance request',link:'/passenger/status',linkText:'View passenger status',role:'PASSENGER'},
    {title:'The driver sees both alerts',description:'The request and the potential obstruction are visible together on the driver dashboard.',action:'Continue to acknowledgment',link:'/driver',linkText:'Open driver dashboard',role:'DRIVER'},
    {title:'The driver acknowledges',description:'The driver confirms the request. The passenger can now see that help has been acknowledged.',action:'Acknowledge request',link:'/passenger/status',linkText:'See passenger update',role:'DRIVER'},
    {title:'The operator has visibility',description:'The command center can follow the passenger request and the boarding-zone advisory.',action:'Continue to zone check',link:'/operator',linkText:'Open command center',role:'OPERATOR'},
    outcome==='success'
      ? {title:'The boarding zone is cleared',description:'In this successful scenario, the obstruction is marked cleared. The driver still checks conditions on site.',action:'Clear simulated obstruction',link:'/experience',linkText:'See updated street view',role:'STREET VIEW'}
      : {title:'The obstruction remains',description:'For this unsuccessful scenario, the boarding zone stays obstructed. No clearance is recorded.',action:'Continue with active alert',link:'/experience',linkText:'See active obstruction',role:'STREET VIEW'},
    outcome==='success'
      ? {title:'The passenger boards safely',description:'The boarding attempt concludes with a recorded successful outcome.',action:'Record successful boarding',link:'/passenger/status',linkText:'View boarding result',role:'PASSENGER'}
      : {title:'Boarding cannot proceed',description:'The obstruction prevents ramp deployment. The unsuccessful outcome and reason are recorded.',action:'Record unsuccessful boarding',link:'/passenger/status',linkText:'View boarding result',role:'PASSENGER'},
    {title:'The operator closes the loop',description:'The operator reviews the recorded journey and its outcome for follow-up.',action:'Record operator review',link:'/operator',linkText:'Review recorded outcome',role:'OPERATOR'}
  ];
}

const journeyRoles = [
  {label:'Street', icon:AlertTriangle}, {label:'Passenger', icon:Accessibility},
  {label:'Driver', icon:BusFront}, {label:'Operator', icon:Users}
];

export default function ScenarioLab() {
  const [previewOpen,setPreviewOpen]=useState(false);
  const {state,dispatch,notify} = useDemo();
  const [error,setError] = useState('');
  const [success,setSuccess] = useState('');
  const [busy,setBusy] = useState(false);
  const [showAdvanced,setShowAdvanced] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const steps = guidedSteps(state.guidedOutcome);
  const guideActive = state.guidedStep >= 0;
  const guideComplete = state.guidedStep >= steps.length;
  const nextStep = state.guidedStep >= 0 && !guideComplete ? steps[state.guidedStep] : null;
  const activeIncident = state.incidents.find(i=>i.detectionStatus==='POTENTIAL');
  const request = state.requests[0];
  const scenario = scenarios.find(x=>x.id===state.activeScenario) ?? scenarios[0];
  const progress = guideComplete ? 100 : Math.max(0, Math.round(state.guidedStep / steps.length * 100));

  const preset = (selected: Scenario) => {
    dispatch({type:'PRESET',scenario:selected});
    notify(`${scenarios.find(x=>x.id===selected)?.label} scenario loaded.`);
  };
  const reset = () => {
    if (window.confirm('Reset all passenger requests, incidents and demonstration events? This cannot be undone.')) {
      dispatch({type:'RESET'});
      setSuccess(''); setError('');
      notify('Experience reset. Ready for a new journey.');
    }
  };
  const importFile = async (file?: File) => {
    if (!file) return;
    setError(''); setSuccess(''); setBusy(true);
    try {
      if (file.size > 250000) throw new Error('JSON file must be under 250 KB.');
      const obj: unknown = JSON.parse(await file.text());
      const items=Array.isArray(obj)?obj:[obj];
      if(!items.length||items.length>200)throw new Error('Choose 1–200 sensor events.');
      const events:ValidAiEvent[]=items.map(item=>{const valid=validateAiEvent(item);if(!valid.ok)throw new Error(valid.error);return valid.event});
      const seen=new Set(state.importedEventIds);let added=0;
      for(const event of events){
        if(seen.has(event.event_id))continue;
        seen.add(event.event_id);added++;
        if(event.event_type==='OBSTRUCTION_DETECTED')dispatch({type:'OBSTRUCT',objectClass:event.object!.class,stopId:event.stop_id,imported:event});
        else dispatch({type:'IMPORT_CLEAR',event});
      }
      if(!added)throw new Error('These events have already been imported.');
      setSuccess(`${added} sensor event${added===1?'':'s'} applied in file order.`);
      notify('Event applied to the connected demonstration.');
    } catch(err) {
      setError(err instanceof SyntaxError ? 'Invalid JSON file. Select a valid event file.' : err instanceof Error ? err.message : 'Unable to import this file.');
    } finally { setBusy(false); if(inputRef.current) inputRef.current.value=''; }
  };
  const startGuided = (outcome: 'success'|'failure') => {
    dispatch({type:'GUIDE_START',outcome});
    notify(`${outcome==='success'?'Successful':'Unsuccessful'} boarding walkthrough ready.`);
  };
  const advance = () => {
    dispatch({type:'GUIDE_NEXT'});
    notify(`Journey moment ${state.guidedStep+1} recorded.`);
  };

  return <main className="page-container demo-page">
    <div className="page-titlebar">
      <div><span className="overline">EXPLORE THE SOLUTION</span><h1>Scenario <span className="teal">Lab</span></h1><p>Explore the moments that determine whether someone can board.</p></div>
      <div className="titlebar-end"><DemoBadge/><button className="btn btn-outline" onClick={reset}><RotateCcw size={17}/> Reset all</button></div>
    </div>

    <div className="demo-grid">
      <div className="demo-side">
        <section className="guided-panel" id="guided-demo" aria-labelledby="guided-heading">
          <div className="guided-top"><div><span className="overline">THE STORY IN EIGHT MOMENTS</span><h2 id="guided-heading">Guided walkthrough</h2><p>Watch how one boarding journey unfolds from start to finish.</p></div><span className="guided-icon"><Play size={24}/></span></div>
          <div className="journey-role-strip">{journeyRoles.map((role,index)=><div key={role.label}><role.icon size={16}/><span>{role.label}</span>{index<3&&<ArrowRight size={12} className="journey-role-arrow"/>}</div>)}</div>
          <div className="guided-mode" role="group" aria-label="Choose boarding outcome"><button aria-pressed={state.guidedOutcome==='success'} className={state.guidedOutcome==='success'?'guided-selected':''} onClick={()=>startGuided('success')}><CheckCircle2 size={15}/> Successful boarding</button><button aria-pressed={state.guidedOutcome==='failure'} className={state.guidedOutcome==='failure'?'guided-selected':''} onClick={()=>startGuided('failure')}><XCircle size={15}/> Unable to board</button></div>
          {!guideActive ? <div className="guide-start"><div className="guide-preview">{steps.map((s,i)=><span key={i}>{String(i+1).padStart(2,'0')}</span>)}</div><p>Choose an outcome, then advance through each moment of the journey.</p><button className="btn btn-white btn-lg btn-full" onClick={()=>startGuided(state.guidedOutcome)}><Play size={18}/> Start guided journey</button></div>
            : guideComplete ? <div className="guide-finished"><CheckCircle2 size={45}/><h3>Journey complete</h3><p>{state.guidedOutcome==='success'?'The passenger boarded and the operator has a clear record of the outcome.':'The boarding obstacle and unsuccessful outcome are recorded for operator review.'}</p><div className="guided-finished-links"><Link to="/passenger/status" className="guided-role-link">Passenger result <ArrowUpRight size={15}/></Link><Link to="/operator" className="guided-role-link">Operator record <ArrowUpRight size={15}/></Link></div><button className="btn btn-white btn-full" onClick={()=>startGuided(state.guidedOutcome)}>Replay this journey <ArrowRight size={17}/></button></div>
            : <div className="guided-step" key={`${state.guidedOutcome}-${state.guidedStep}`}><div className="guided-progress"><span>MOMENT {state.guidedStep+1} / 8</span><span>{progress}% complete</span></div><div className="progress-track" role="progressbar" aria-valuemin={0} aria-valuemax={8} aria-valuenow={state.guidedStep} aria-label="Guided journey progress"><div style={{width:`${progress}%`}}/></div><div className="guide-moment-line"><span className="step-index">{String(state.guidedStep+1).padStart(2,'0')}</span><span className="guide-role-pill">{nextStep?.role}</span></div><h3>{nextStep?.title}</h3><p>{nextStep?.description}</p><div className="guide-peek"><span className="guide-peek-label">WHERE TO SEE IT</span><Link to={nextStep!.link} className="guided-role-link">{nextStep!.linkText} <ArrowUpRight size={17}/></Link></div><button className="btn btn-white btn-lg btn-full" onClick={advance}>{nextStep?.action} <ArrowRight size={18}/></button><p className="guide-button-hint">This advances the demonstration. Open the linked screen to see the updated state.</p></div>}
        </section>
        <details className="simple-disclosure" onToggle={e=>setPreviewOpen(e.currentTarget.open)}><summary>Street preview and scene controls</summary><div className="disclosure-body">        <Panel title="Live street preview" aside={<Link to="/experience" className="inline-link">Expand <ArrowRight size={15}/></Link>}>{previewOpen&&<DigitalTwin/>}</Panel></div></details>
      </div>

      <div>
        <details className="simple-disclosure"><summary>Explore individual scenarios</summary><div className="disclosure-body">        <Panel title="Choose a situation" aside={<Tag tone="teal">7 scenarios</Tag>}>
          <p className="scenario-section-lead">Select any scene to explore how NaikReady responds.</p>
          <div className="scenario-grid">
            {scenarios.map(item=><button key={item.id} type="button" aria-pressed={state.activeScenario===item.id} className={`scenario-card scenario-card-${item.tone} ${state.activeScenario===item.id?'scenario-selected':''}`} onClick={()=>preset(item.id)}>
              <ScenarioVisual scenario={item.id}/>
              <span className="scenario-info-row"><span className={`scenario-icon scenario-${item.tone}`}><item.icon size={19}/></span><span className="scenario-card-copy"><span className="scenario-eyebrow">{item.group}</span><strong>{item.label}</strong><span className="scenario-description">{item.description}</span></span><span className="scenario-arrow">{state.activeScenario===item.id?<Check size={18}/>:<ArrowUpRight size={18}/>}</span></span>
              {state.activeScenario===item.id && <span className="scenario-active-tag"><Check size={12}/> Selected scene</span>}
            </button>)}
          </div>
        </Panel>
</div></details>
        <div className="scene-status-panel" aria-live="polite">
          <div className="scene-status-header"><div><span className="overline">CURRENT SCENE</span><h3>{scenario.label}</h3></div><span className={`scene-status-dot ${activeIncident?'scene-is-alert':''}`}/></div>
          <div className="scene-status-details">
            <div><span>Boarding zone</span><strong className={activeIncident?'text-alert':'text-positive'}>{activeIncident?'Possible obstruction':'No active advisory'}</strong></div>
            <div><span>Passenger request</span><strong>{request ? request.status.replaceAll('_',' ').toLowerCase() : 'None yet'}</strong></div>
          </div>
          <Link to="/experience" className="inline-link">Explore full street visualization <ArrowRight size={15}/></Link>
        </div>
        <div className="event-import-wrap"><button className="advanced-event-toggle" aria-expanded={showAdvanced} onClick={()=>setShowAdvanced(!showAdvanced)}><span><FileJson size={17}/> Recorded AI event import <small>Optional showcase feature</small></span><span>{showAdvanced?'Hide details':'Show details'} <ArrowRight size={15}/></span></button>
          {showAdvanced && <div className="event-import-body"><p>Import a recorded detection event to show a potential obstruction warning across the passenger, driver and operator views.</p><input ref={inputRef} type="file" accept=".json,application/json" className="sr-only" id="event-file" onChange={e=>void importFile(e.target.files?.[0])}/><div className="event-import-actions"><button className="btn btn-primary" disabled={busy} onClick={()=>inputRef.current?.click()}><UploadCloud size={17}/>{busy?'Importing...':'Choose event JSON'}</button><a href="/demo-assets/sample-obstruction-event.json" download className="inline-link">Sample event <ArrowRight size={14}/></a></div>{error&&<div className="notice notice-red" role="alert"><CircleAlert size={18}/>{error}</div>}{success&&<div className="notice notice-green" role="status"><CheckCircle2 size={18}/>{success}</div>}</div>}
        </div>
      </div>

    </div>

    <PhotoBanner photo="bus" eyebrow="STREETS. PEOPLE. POSSIBILITIES." title="Explore the moments that shape a journey." description="Follow a boarding situation from the roadside to a coordinated response." compact/>
    <div className="demo-intro">
      <div className="demo-intro-icon"><FlaskConical size={26}/></div>
      <div><strong>One stop. Four perspectives. One connected journey.</strong><p>Explore the obstruction, passenger request, driver response and boarding outcome.</p></div>
      <a className="btn btn-white btn-sm" href="#guided-demo">Take the guided tour <ArrowRight size={16}/></a>
    </div>

    <details className="simple-disclosure"><summary>Journey activity</summary><div className="disclosure-body">    <Panel title="Journey activity" aside={<span className="tiny muted">Most recent first</span>} className="demo-log"><div className="log-table">{state.activityLog.length?state.activityLog.slice(0,25).map(l=><div className="log-entry" key={l.id}><span className="log-icon"><Activity size={17}/></span><span><strong>{l.message}</strong><small>{l.type.replaceAll('_',' ')} {l.detail?`· ${l.detail}`:''}</small></span><time>{formatTime(l.at)}</time></div>):<Empty icon={<Activity size={25}/>} heading="Your journey begins here" text="Choose a scenario or begin the guided demonstration to see activity appear."/>}</div></Panel>
</div></details>
    <div className="demo-disclaimer"><Info size={18}/> Interactive concept demonstration using illustrative data. Drivers verify boarding conditions on site.</div>
  </main>;
}
