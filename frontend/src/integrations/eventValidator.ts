import type { ValidAiEvent } from '../app/demoTypes';
const STOP_IDS = ['CYB-DEMO-01', 'CYB-DEMO-02'];
const asObject = (v: unknown): v is Record<string,unknown> => !!v && typeof v === 'object' && !Array.isArray(v);
export function validateAiEvent(value: unknown): { ok: true; event: ValidAiEvent } | { ok: false; error: string } {
  if (!asObject(value)) return {ok:false,error:'The file must contain a JSON object.'};
  if (value.schema_version !== '1.0') return {ok:false,error:'Unsupported schema_version. Expected 1.0.'};
  if (typeof value.event_id !== 'string' || !/^[a-zA-Z0-9._-]{1,100}$/.test(value.event_id)) return {ok:false,error:'event_id must be a unique identifier (1–100 letters/numbers/._-).'};
  if (value.event_type !== 'OBSTRUCTION_DETECTED' && value.event_type !== 'OBSTRUCTION_CLEARED') return {ok:false,error:'This importer supports OBSTRUCTION_DETECTED or OBSTRUCTION_CLEARED.'};
  if (!STOP_IDS.includes(value.stop_id as string)) return {ok:false,error:'Unknown stop_id. Choose CYB-DEMO-01 or CYB-DEMO-02.'};
  if (value.route_id !== 'DEMO-R01') return {ok:false,error:'Unknown route_id. Expected DEMO-R01.'};
  if (typeof value.timestamp !== 'string' || !/^\d{4}-\d\d-\d\dT\d\d:\d\d/.test(value.timestamp) || !Number.isFinite(Date.parse(value.timestamp))) return {ok:false,error:'timestamp must be a valid ISO 8601 date/time.'};
  if (!['manual_simulation','recorded_video_model_inference'].includes(value.source_mode as string)) return {ok:false,error:'Invalid source_mode.'};
  if (value.deployment_status !== 'prototype' || value.is_demo !== true) return {ok:false,error:'This demo accepts only prototype events with is_demo: true.'};
  if (value.event_type === 'OBSTRUCTION_DETECTED') {
    if (!asObject(value.object) || !['car','motorcycle','truck'].includes(value.object.class as string)) return {ok:false,error:'Detected events require object.class = car, motorcycle or truck.'};
  }
  if (value.object !== undefined) {
    if (!asObject(value.object)) return {ok:false,error:'object must be a JSON object.'};
    if (value.object.confidence !== undefined && value.object.confidence !== null && (typeof value.object.confidence !== 'number' || !Number.isFinite(value.object.confidence) || value.object.confidence < 0 || value.object.confidence > 1)) return {ok:false,error:'Confidence must be between 0 and 1.'};
  }
  if (value.zone !== undefined) {
    if (!asObject(value.zone) || typeof value.zone.id !== 'string' || !value.zone.id) return {ok:false,error:'zone.id is required when a zone is supplied.'};
    if (value.zone.dwell_seconds !== undefined && (typeof value.zone.dwell_seconds !== 'number' || !Number.isFinite(value.zone.dwell_seconds) || value.zone.dwell_seconds < 0)) return {ok:false,error:'Dwell seconds must be zero or positive.'};
    if (value.zone.overlap_ratio !== undefined && (typeof value.zone.overlap_ratio !== 'number' || value.zone.overlap_ratio < 0 || value.zone.overlap_ratio > 1)) return {ok:false,error:'Overlap ratio must be between 0 and 1.'};
  }
  if(value.episode_id!==undefined&&(typeof value.episode_id!=='string'||value.episode_id.length>100))return {ok:false,error:'Invalid episode identifier.'};
  const clean=structuredClone(value);
  if(asObject(clean.object)&&clean.object.confidence===null)delete clean.object.confidence;
  return {ok:true,event:clean as unknown as ValidAiEvent};
}
