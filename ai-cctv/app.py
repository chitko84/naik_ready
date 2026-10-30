"""NaikReady Vision AI — local recorded-video review console."""
import json,tempfile,uuid
from pathlib import Path
from html import escape
from datetime import datetime,timezone
import cv2
import streamlit as st
from detect import load_config,process_video
from vision import annotate
from event_export import export_events,history_rows,csv_bytes
from photo_scenarios import render_photo

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='NaikReady Vision AI',page_icon='🚌',layout='wide')
SLIDER_CSS = """
/* Scenario playback control: styles are included in app.py. */
.st-key-scenario_control{padding:18px 22px 16px;margin-top:12px;border:1px solid #dce7f5;border-radius:16px;background:linear-gradient(135deg,#fff,#eef5ff);box-shadow:0 6px 20px #071c360d}
.scenario-heading{display:flex;align-items:center;justify-content:space-between;gap:12px;color:#11365a;font-size:11px;font-weight:750;letter-spacing:1.3px}
.scenario-heading span{color:#75869b;font-size:11px;font-weight:400;letter-spacing:0}
.st-key-scenario_control [data-testid="stSlider"] [data-orientation="horizontal"][style*="position: relative"]{height:8px!important;margin:30px 5px 12px!important;border-radius:999px!important;background:#dce7f5!important}
.st-key-scenario_control [data-testid="stSlider"] [data-orientation="horizontal"][style*="position: relative"]>div:first-child{height:100%!important;border-radius:999px!important;background:linear-gradient(90deg,#1769e0,#20c4ba)!important}
.st-key-scenario_control [data-testid="stSlider"] [data-rac][style*="position: absolute"]{width:22px!important;height:22px!important;box-sizing:border-box!important;border:4px solid white!important;border-radius:50%!important;background:#1769e0!important;box-shadow:0 0 0 1px #bed3ee,0 3px 10px #1769e04d;transition:box-shadow 180ms ease}
.st-key-scenario_control [data-testid="stSlider"] [data-rac][style*="position: absolute"]:hover{box-shadow:0 0 0 6px #1769e01f,0 3px 12px #1769e04d}
.st-key-scenario_control [data-testid="stSlider"] [data-rac][style*="position: absolute"]:focus-within{outline:2px solid #008f96;outline-offset:4px}
.st-key-scenario_control [data-testid="stSliderThumbValue"] p{color:#1769e0!important;font-size:12px!important;font-weight:650!important;white-space:nowrap}
.st-key-scenario_control [data-testid="stSliderTickBar"]{display:none!important}
.scenario-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:8px}
.scenario-step{display:flex;align-items:center;gap:7px;padding:10px 8px;border:1px solid #e2eaf1;border-radius:9px;background:#ffffffb3;color:#75869b;font-size:11px;transition:background-color 180ms ease,border-color 180ms ease,color 180ms ease}
.scenario-step b{color:#9aaabd;font-size:10px}
.scenario-step.active{border-color:#a8cafa;background:#e4efff;color:#1769e0;font-weight:650}
.scenario-step.active b{color:#1769e0}
@media(max-width:600px){.scenario-steps{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(prefers-reduced-motion:reduce){.st-key-scenario_control *{transition:none!important}}
"""
st.markdown('<style>'+(ROOT/'console.css').read_text()+SLIDER_CSS+'</style>',unsafe_allow_html=True)
def read(p):return json.loads(Path(p).read_text())
def frames(p):return [json.loads(s) for s in Path(p).read_text().splitlines() if s.strip()]
def exports(events,key):
    a,b=st.columns(2)
    a.download_button('Export JSON',json.dumps(events,indent=2),'naikready_events.json','application/json',key=key+'json',width='stretch')
    b.download_button('Export CSV',csv_bytes(events),'naikready_history.csv','text/csv',key=key+'csv',width='stretch')

def choose_scenario(label):
    st.session_state.scenario=label
    st.session_state.evidence_mode='Manual simulation'

cfg=load_config(ROOT/'config.json')
cfg.update(stop_id='CYB-DEMO-01',zone_id='boarding-zone-01',dwell_seconds=10.0)
if 'zone_settings' in st.session_state:cfg.update(st.session_state.zone_settings)
with st.sidebar:
    st.markdown('<div class="brand"><svg width=26 height=26 viewBox="0 0 26 26" style="vertical-align:middle;color:#438eff"><circle cx=13 cy=13 r=7 fill=none stroke=currentColor stroke-width=3 /><path d="M3 9 A11 11 0 0 1 23 9 M3 17 A11 11 0 0 0 23 17" fill=none stroke=currentColor stroke-width=2 /><circle cx=13 cy=13 r=3 fill=currentColor /></svg> NaikReady <span>5G</span></div><div class="subtitle">VISION AI / RECORDED VIDEO DEMO</div>',unsafe_allow_html=True)
    section=st.radio('Workspace',['Video Detection','Detection History','Test Scenarios','Zone Configuration','About Prototype'],label_visibility='collapsed')
    mode=st.selectbox('Evidence source',['Manual simulation','Recorded video · YOLO'],key='evidence_mode')
    source_badge='AI-GENERATED SIMULATION' if mode=='Manual simulation' else 'DEMO — RECORDED FOOTAGE'
    st.markdown(f'<div class="scope"><b>AI MODEL</b><br>YOLOv8n · pretrained<br>CPU inference<br><br><b>{source_badge}</b><br>No live CCTV connection.<br>No measured 5G connection.</div>',unsafe_allow_html=True)

sim=mode=='Manual simulation'
folder=ROOT/'outputs/simulation'
scenarios={'Normal / Clear':('01_clear_bus_stop',2.0),'Car Blocking':('02_car_blocking',9.0),'Motorcycle Blocking':('03_motorcycle_blocking',18.0),'Obstruction Cleared':('05_obstruction_cleared',22.5)}
selection=st.session_state.get('scenario','Normal / Clear')
allframes=frames(folder/'frames.jsonl') if sim else []
events=read(folder/'events.json') if sim else []
source='AI-generated photorealistic scene' if sim else 'No recording processed'
snapshot=min(allframes,key=lambda f:abs(f['video_time_seconds']-scenarios[selection][1])) if sim else {'status':'UNCERTAIN','detections':[],'video_time_seconds':0}
summary={}
if not sim and st.session_state.get('last_result'):
    result=Path(st.session_state.last_result);summary=read(result/'summary.json');allframes=frames(result/'frames.jsonl');events=read(result/'events.json');snapshot=allframes[-1];source=summary['source']
contract=export_events(events)
# Stable export timestamps describe event generation, never invented capture dates.
for e in contract:
    stamp_key='event_stamp_'+e['event_id']
    if stamp_key not in st.session_state:st.session_state[stamp_key]=e['timestamp']
    e['timestamp']=st.session_state[stamp_key]

st.title('AI CCTV Monitoring – Bus Stop Obstruction Detection')
st.caption('NaikReady Vision AI · See the blockage. Support the boarding.')
a,b,c=st.columns([2,2,1]);a.markdown('**Demo Stop: CYB-DEMO-01**');b.caption(source);c.markdown('<span class="badge">LOCAL PROTOTYPE</span>',unsafe_allow_html=True)
if sim:st.info('AI-GENERATED SCENES · Manual simulation, not CCTV footage. Boxes and observations are scripted; confidence is unavailable. Fixture dwell: 3s / actual analysis default: 10s.')
else:st.info('Recorded Video Analysis — NOT LIVE CCTV · Upload footage you are authorized to process. Confidence scores come from actual model inference.')

if section=='Zone Configuration':
    st.subheader('Boarding-area polygon')
    st.caption('Ordered normalized [x,y] points, each from 0 to 1. Bottom-center anchors determine zone membership.')
    raw=st.text_area('Polygon points',json.dumps(cfg['zone']),height=110)
    dwell=st.slider('Obstruction dwell (video seconds)',3,15,int(cfg['dwell_seconds']))
    conf=st.slider('Detection confidence threshold',.1,.9,float(cfg['confidence']),.05)
    show=st.checkbox('Show boarding zone',value=cfg.get('show_zone',True))
    try:
        poly=json.loads(raw);candidate=dict(cfg,zone=poly,dwell_seconds=dwell,confidence=conf,show_zone=show)
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json',delete=False) as f:json.dump(candidate,f);test=Path(f.name)
        try:load_config(test)
        finally:test.unlink(missing_ok=True)
        if st.button('Save zone settings',type='primary'):
            st.session_state.zone_settings={k:candidate[k] for k in ('zone','dwell_seconds','confidence','show_zone')};st.success('Settings saved for this session and the next analysis.')
        st.download_button('Download zone configuration',json.dumps(candidate,indent=2),'demo_zone.json','application/json')
        img=st.session_state.get('calibration_frame',cv2.imread(str(ROOT/'assets/photoreal/clear.png')))
        st.image(annotate(img,{'status':'CLEAR','simulated':'calibration_frame' not in st.session_state,'video_time_seconds':0,'detections':[]},candidate),channels='BGR',caption='Calibration preview only — model has not run. Background uses uploaded first frame when available, otherwise an AI-generated scene.')
    except Exception as exc:st.error(f'Invalid zone: {exc}')
    st.stop()

if section=='About Prototype':
    st.subheader('AI Smart CCTV — Boarding Zone Awareness')
    st.write('OpenCV decoding → pretrained YOLO vehicle recognition → bottom-center polygon test → local IoU tracking → stationary dwell → potential obstruction event → operator review.')
    st.write('YOLOv8n is retained as a lightweight, available substitute for the suggested YOLO11n. No training or GPU is required.')
    st.subheader('System Limitations')
    st.write('Occlusion, camera shake, perspective, small vehicles and classification errors can affect results. Confidence filtering can remove uncertain objects; no detections cannot prove an empty or safe zone. Buses are observed and exempt from obstruction alerts. Clearance does not establish successful boarding. No passenger identity or disability inference is used.')
    st.write('Future 5G concept: roadside processing → filtered event and optional evidence → driver/operator review. This prototype writes local files; it measures no 5G latency or throughput.')
    st.caption('Ultralytics code/models: AGPL-3.0 / Enterprise licensing. See NOTICE.md and LICENSE. Reference-road footage attribution does not establish public-submission permission; use your own authorized recording for submission.')
    st.stop()

if section=='Detection History':
    st.subheader('Detection history · Current Test Run' if not sim else 'Detection history · Manual Simulation')
    st.dataframe(history_rows(contract),width='stretch');exports(contract,'history')
    st.caption('Session-local episodes, not one alert per frame. JSON is an array using OBSTRUCTION_DETECTED / OBSTRUCTION_CLEARED. Min import acceptance still requires testing in Min’s app.')
    st.stop()

if not sim and section=='Video Detection':
    with st.expander('Upload / run recorded video',expanded=not bool(summary)):
        upload=st.file_uploader('Authorized MP4 / recorded clip',type=['mp4','mov','avi','mkv'])
        if upload:
            with tempfile.NamedTemporaryFile(suffix=Path(upload.name).suffix,delete=False) as f:f.write(upload.getvalue());path=Path(f.name)
            try:
                cap=cv2.VideoCapture(str(path));fps=cap.get(cv2.CAP_PROP_FPS);count=cap.get(cv2.CAP_PROP_FRAME_COUNT);ok,img=cap.read();cap.release()
                if ok:
                    st.session_state.calibration_frame=img
                    st.caption(f'{img.shape[1]} × {img.shape[0]} · {fps:.2f} source FPS · {count/fps if fps else 0:.1f}s duration')
                    st.image(annotate(img,{'status':'CLEAR','simulated':False,'video_time_seconds':0,'detections':[]},cfg),channels='BGR',caption='Calibration preview / model has not processed this input')
                if st.button('Run AI analysis',type='primary'):
                    st.session_state.pop('last_result',None);out=ROOT/'outputs/runs'/uuid.uuid4().hex[:10];monitor=st.empty()
                    def update(im,s):monitor.image(im,channels='BGR',caption=f'Processing recorded video · {s["video_time_seconds"]:.1f}s · {s["status"]}')
                    try:
                        report=process_video(path,cfg,out,update);report['source']=upload.name;(out/'summary.json').write_text(json.dumps(report,indent=2));st.session_state.last_result=str(out);st.rerun()
                    except Exception as exc:st.error(f'Analysis failed: {exc}');st.stop()
            finally:path.unlink(missing_ok=True)

left,right=st.columns([2.15,1],gap='medium')
with left:
    with st.container(border=True):
        st.subheader('Recorded detection monitor' if not sim else 'Scenario monitor · Manual Simulation')
        if sim:
            st.image(render_photo(selection,st.session_state.get('show_photo_zone',True),st.session_state.get('show_photo_boxes',True)),channels='BGR',width='stretch')
            with st.container(key="scenario_control"):
                st.markdown(
                    '<div class="scenario-heading">SCENARIO PLAYBACK'
                    '<span>Drag to explore</span></div>',
                    unsafe_allow_html=True
                )
                selected = st.select_slider(
                    "Scenario", options=list(scenarios), key="scenario",
                    label_visibility="collapsed"
                )
                current = list(scenarios).index(selected)
                steps = ""
                for index, label in enumerate(["Clear", "Car Blocking", "Motorcycle", "Cleared"]):
                    active = "active" if index == current else ""
                    steps += (
                        f'<span class="scenario-step {active}">'
                        f'<b>{index + 1:02}</b>{label}</span>'
                    )
                st.markdown(f'<div class="scenario-steps">{steps}</div>', unsafe_allow_html=True)
            with st.expander('Legacy illustrated logic replay (separate from generated photos)'):st.video(str(folder/'preview.webm'),format='video/webm')
        elif summary:
            cap=cv2.VideoCapture(str(result/'annotated.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,summary['frames_processed']-1);ok,im=cap.read();cap.release()
            if ok:st.image(im,channels='BGR',width='stretch')
            st.caption(f'Last processed frame · {snapshot["video_time_seconds"]:.3f}s video time')
            st.download_button('Download annotated video',(result/'annotated.mp4').read_bytes(),'annotated.mp4','video/mp4')
        else:st.warning('UNCERTAIN / INSUFFICIENT EVIDENCE — upload a recording and run analysis.')
with right:
    with st.container(border=True):
        st.subheader('Boarding Zone Status')
        state=snapshot['status'] if sim or snapshot['detections'] else 'UNCERTAIN';blocked=state=='BLOCKED';observing=state in ('UNCERTAIN','OBSERVING','CLEARING')
        title='POTENTIAL OBSTRUCTION — REVIEW' if blocked else 'UNCERTAIN / INSUFFICIENT EVIDENCE' if observing else 'CLEAR / NO POTENTIAL OBSTRUCTION OBSERVED'
        st.markdown(f'<div class="status {"blocked" if blocked else "uncertain" if observing else ""}"><strong>{title}</strong><small>Monitored frame only · human review required<br>{"Scenario fixture time" if sim else "Video time"}: {snapshot["video_time_seconds"]:.2f}s</small></div>',unsafe_allow_html=True)
        st.subheader('Simulated Observations' if sim else 'Detected Objects')
        for d in snapshot['detections']:
            score='Unavailable / scripted' if d['confidence'] is None else f'{d["confidence"]:.2f}'
            st.markdown(f'<div class="object"><div><b>{escape(d["vehicle_type"].title())}</b><small>Confidence: {score} · dwell {d["stationary_seconds"]:.1f}s</small></div><span class="pill {"in" if d["in_zone"] else ""}">{"Inside Zone" if d["in_zone"] else "Outside Zone"}</span></div>',unsafe_allow_html=True)
        if not snapshot['detections']:st.caption('No scored vehicle observation in this frame. This is not a guarantee of boarding safety.')
        st.caption(f'Dwell threshold: {3 if sim else summary.get("config",cfg)["dwell_seconds"]:g}s · clearance window: 1s')
        st.caption('Edit analysis polygon and thresholds in Zone Configuration.')
        if sim:
            st.checkbox('Show simulation zone',True,key='show_photo_zone')
            st.checkbox('Show simulation boxes',True,key='show_photo_boxes')
            st.caption('Presentation overlays are manually positioned on AI-generated scenes.')
            st.image(render_photo(selection,True,False),channels='BGR',width=250,caption='Boarding-zone preview / synthetic scene')
        exports(contract,'main')

st.subheader('Detection Scenarios · Manual Simulation')
for col,(label,(image,t)) in zip(st.columns(4),scenarios.items()):
    with col,st.container(border=True):
        st.markdown('**'+label+'**');st.image(render_photo(label),channels='BGR',width='stretch')
        st.caption('AI-generated scene · manual simulation')
        st.button('Inspect scenario',key=image,width='stretch',on_click=choose_scenario,args=(label,))

st.subheader('Detection History')
st.dataframe(history_rows(contract),width='stretch')
with st.expander('Current Test Run / counts and limitations'):
    st.caption('Counts below are frame-level detection instances, not unique vehicles.')
    cols=st.columns(4)
    for c,label in zip(cols,['car','motorcycle','bus','truck']):c.metric(label.title(),sum(d['vehicle_type']==label for f in allframes for d in f['detections']))
    st.write('Negative test: moving reference-road traffic generated no obstruction event in the earlier reference inference test. This is not a target bus-stop validation. Low-confidence objects are filtered and cannot establish safe clearance. Use authorized staged bus-stop footage for the submission.')
