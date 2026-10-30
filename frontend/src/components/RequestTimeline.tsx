import {Check,Clock3,Send,ShieldCheck,BusFront,CircleAlert,X} from 'lucide-react';
import type {AssistanceRequest} from '../app/demoTypes';
import {formatTime} from '../app/demoData';
export default function RequestTimeline({request:r}:{request:AssistanceRequest}){
 const terminal=['COMPLETED','UNABLE_TO_BOARD','CANCELLED'].includes(r.status);
 const sent={title:'Request sent',desc:'Your assistance request has been submitted.',icon:Send,time:r.createdAt};
 const ack={title:'Driver acknowledged',desc:'The driver has acknowledged your request.',icon:ShieldCheck,time:r.acknowledgedAt};
 const attempt={title:'Boarding in progress',desc:'The driver has started the boarding-assistance attempt.',icon:BusFront,time:r.boardingStartedAt};
 const final={title:r.status==='UNABLE_TO_BOARD'?'Unable to board':r.status==='CANCELLED'?'Request cancelled':'Boarding confirmed',desc:r.status==='UNABLE_TO_BOARD'?`Outcome recorded · ${r.failureReason??'Reason not supplied'}.`:r.status==='CANCELLED'?'Your pending request was cancelled.':'The driver confirmed completed boarding.',icon:r.status==='UNABLE_TO_BOARD'?CircleAlert:r.status==='CANCELLED'?X:Check,time:r.cancelledAt??r.completedAt};
 const entries=r.status==='CANCELLED'?[sent,final]:r.status==='UNABLE_TO_BOARD'&&!r.boardingStartedAt?[sent,ack,final]:[sent,ack,attempt,final];
 const activeIndex=terminal?entries.length-1:r.status==='REQUESTED'?0:r.status==='DRIVER_ACKNOWLEDGED'?1:2;
 return <ol className="request-timeline">{entries.map((entry,index)=>{const pending=index>activeIndex;const done=index<activeIndex||terminal;const Icon=entry.icon;return <li key={entry.title} className={`${done?'timeline-done':''} ${index===activeIndex?'timeline-active':''} ${pending?'timeline-pending':''} ${r.status==='UNABLE_TO_BOARD'&&index===entries.length-1?'timeline-failed':''}`}><div className="timeline-rail"><span className="timeline-circle"><Icon size={19}/></span></div><div className="timeline-copy"><div className="timeline-title"><strong>{entry.title}</strong>{entry.time&&<time dateTime={entry.time}>{formatTime(entry.time)}</time>}</div><p>{pending?'Waiting for previous step to finish.':entry.desc}</p>{index===activeIndex&&!terminal&&<span className="timeline-current"><Clock3 size={12}/> Current stage</span>}</div></li>})}</ol>
}
