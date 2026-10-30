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
