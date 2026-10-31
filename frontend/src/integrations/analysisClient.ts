export type JobSnapshot={status:'queued'|'processing'|'complete'|'failed';progress?:number;phase?:string;error?:string;[key:string]:unknown};
export async function waitForAnalysis(jobId:string,options:{signal:AbortSignal;onUpdate:(job:JobSnapshot)=>void;request?:typeof fetch;wait?:(ms:number)=>Promise<void>;now?:()=>number;maxWaitMs?:number}):Promise<JobSnapshot>{
 const request=options.request??fetch;const now=options.now??Date.now;const start=now();let failures=0;
 const wait=options.wait??((ms:number)=>new Promise<void>((resolve,reject)=>{const abort=()=>{clearTimeout(timer);reject(new DOMException('Stopped waiting for analysis.','AbortError'))};const timer=setTimeout(()=>{options.signal.removeEventListener('abort',abort);resolve()},ms);options.signal.addEventListener('abort',abort,{once:true})}));
 while(true){
  options.signal.throwIfAborted();if(now()-start>(options.maxWaitMs??240000))throw Error('Analysis took too long. Try a shorter video or use Scenario analysis.');
  let job:JobSnapshot;
  try{const signal=AbortSignal.any([options.signal,AbortSignal.timeout(15000)]);const response=await request(`/api/jobs/${encodeURIComponent(jobId)}`,{signal});if(!response.ok)throw Error(`Cannot read analysis status (${response.status}).`);job=await response.json();if(!['queued','processing','complete','failed'].includes(job.status))throw Error('Vision API returned an invalid job status.');failures=0;}
  catch(error){if(options.signal.aborted)throw error;if(++failures>=3)throw Error('Vision API connection was interrupted. Retry the analysis or use Scenario analysis.');await wait(1000);continue}
  options.onUpdate(job);
  // A failed job is terminal, never a retryable polling error.
  if(job.status==='failed')throw Error(job.error??'The analysis failed. Choose another file and try again.');
  if(job.status==='complete')return job;
  await wait(1000);
 }
}
export type ScenarioCase='clear'|'car'|'motorcycle'|'cleared';
export function scenarioResult(data:{events:unknown[];summary?:Record<string,unknown>},scene:ScenarioCase,episodeId?:string){
 const events=data.events as {event_type:string;episode_id?:string;object?:{class:string}}[];
 const event=scene==='car'||scene==='motorcycle'?events.find(e=>e.event_type==='OBSTRUCTION_DETECTED'&&e.object?.class===scene):scene==='cleared'?events.find(e=>e.event_type==='OBSTRUCTION_CLEARED'&&(!episodeId||e.episode_id===episodeId)):undefined;
 return {mode:'scenario_analysis',events:event?[event]:[],summary:data.summary,zone_status:scene==='car'||scene==='motorcycle'?'POTENTIAL':'CLEAR',note:scene==='car'||scene==='motorcycle'?'A stationary vehicle occupies the boarding area. Review the advisory and coordinate clearance.':'The boarding area is clear in this scenario. The driver verifies the zone before deploying the ramp.'};
}

// Hosted services return complete evidence in this request; local development returns a queued job.
export async function readAnalysisStart(response:Response):Promise<{kind:'inline';result:JobSnapshot}|{kind:'queued';jobId:string}>{
 let data:JobSnapshot;
 try{data=await response.json()}catch{throw Error(response.status===413?'The hosted upload is too large. Use a file under 3.5 MB.':'The analysis API returned an invalid response.')}
 if(!response.ok)throw Error(typeof data.detail==='string'?data.detail:'Analysis could not start. Check the selected file.');
 if(data.status==='complete'){
  if(data.mode!=='real_yolo_inference'||data.simulated!==false||!Array.isArray(data.events))throw Error('The analysis API returned an invalid inference result.');
  if(typeof data.evidence_data_url==='string'){
   if(!/^data:image\/jpeg;base64,[A-Za-z0-9+/=]+$/.test(data.evidence_data_url))throw Error('The analysis API returned invalid image evidence.');
   data.evidence_url=data.evidence_data_url;
  }
  return {kind:'inline',result:data};
 }
 if((data.status==='queued'||data.status==='processing')&&typeof data.job_id==='string'&&/^[a-f0-9]{32}$/.test(data.job_id))return {kind:'queued',jobId:data.job_id};
 throw Error('Vision API did not return a valid analysis result or job identifier.');
}
