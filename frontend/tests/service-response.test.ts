import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readAnalysisStart} from '../src/integrations/analysisClient';
const response=(data:unknown,status=200)=>new Response(JSON.stringify(data),{status});
test('hosted inference is handled without polling a transient job',async()=>{
 const output=await readAnalysisStart(response({status:'complete',mode:'real_yolo_inference',simulated:false,events:[],evidence_data_url:'data:image/jpeg;base64,YWJj'}));
 assert.equal(output.kind,'inline');if(output.kind==='inline')assert.equal(output.result.evidence_url,'data:image/jpeg;base64,YWJj');
});
test('local queued jobs retain the existing polling flow',async()=>{
 assert.deepEqual(await readAnalysisStart(response({status:'queued',job_id:'a'.repeat(32)},202)),{kind:'queued',jobId:'a'.repeat(32)});
});
test('HTML upload-limit responses show an actionable error',async()=>{
 await assert.rejects(()=>readAnalysisStart(new Response('Request too large',{status:413})),/3.5 MB/);
});
test('failed service analysis never becomes scenario inference',async()=>{
 await assert.rejects(()=>readAnalysisStart(response({detail:'Detector unavailable'},503)),/Detector unavailable/);
 await assert.rejects(()=>readAnalysisStart(response({status:'complete',mode:'scenario_analysis',simulated:true,events:[]})),/invalid inference/);
 await assert.rejects(()=>readAnalysisStart(response({status:'complete',mode:'real_yolo_inference',simulated:false,events:[],evidence_data_url:'https://private/internal'})),/invalid image evidence/);
});
