export type TwinMode = 'normal' | 'blocked' | 'assistance' | 'resolved';
export type StopId = 'CYB-DEMO-01' | 'CYB-DEMO-02';
export type Scenario = 'NORMAL' | 'CAR_BLOCKING' | 'MOTORCYCLE_BLOCKING' | 'ASSISTANCE' | 'ACKNOWLEDGED' | 'BOARDING_COMPLETED' | 'BOARDING_FAILED';
export type RequestStatus = 'REQUESTED' | 'DRIVER_ACKNOWLEDGED' | 'BOARDING_ATTEMPT' | 'COMPLETED' | 'UNABLE_TO_BOARD' | 'CANCELLED';
export type AssistanceType = 'Wheelchair / Ramp' | 'Extra Boarding Time' | 'Low-Vision Guidance' | 'Stroller' | 'Luggage' | 'Other Assistance';
export type FailureReason = 'Blocked Boarding Zone' | 'Ramp Not Available' | 'Could Not Provide Assistance' | 'Other / Unknown';
export type EventType = 'OBSTRUCTION_DETECTED' | 'OBSTRUCTION_CLEARED' | 'ASSISTANCE_REQUESTED' | 'DRIVER_ACKNOWLEDGED' | 'BOARDING_COMPLETED' | 'BOARDING_FAILED' | 'OPERATOR_REVIEWED' | 'DEMO_RESET';
export interface AssistanceRequest {
  id: string; stopId: StopId; routeId: 'DEMO-R01'; type: AssistanceType; note: string; status: RequestStatus;
  createdAt: string; acknowledgedAt?: string; boardingStartedAt?: string; completedAt?: string; cancelledAt?: string; failureReason?: FailureReason; operatorReviewed?: boolean; operatorNotes?: string; safeVerifiedAt?: string; relatedIncidentIds: string[];
}
export interface ObstructionIncident {
  id: string; eventId?: string; episodeId?: string; assignedTo?: string; coordinatedAt?: string; stopId: StopId; routeId: 'DEMO-R01'; objectClass: 'car' | 'motorcycle' | 'truck'; confidence?: number;
  sourceMode: 'manual_simulation' | 'recorded_video_model_inference'; detectedAt: string; clearedAt?: string;
  detectionStatus: 'POTENTIAL' | 'CLEARED'; driverAcknowledged: boolean; reviewStatus: 'PENDING_OPERATOR_REVIEW' | 'REVIEWED'; operatorNotes: string; evidenceReference?: string; dwellSeconds?: number; overlapRatio?: number;
}
export interface LogEntry { id: string; at: string; type: string; message: string; detail?: string; }
export interface DemoState {
  sceneSelection?: {stopId:StopId; mode:TwinMode}; version: 1; activeScenario: Scenario; selectedStopId: StopId; requests: AssistanceRequest[]; incidents: ObstructionIncident[];
  activityLog: LogEntry[]; importedEventIds: string[]; guidedStep: number; guidedOutcome: 'success' | 'failure';
}
export type DemoAction =
  | { type:'SELECT_TWIN_MODE'; mode:TwinMode }
  | { type: 'RESTORE'; state: DemoState }
  | { type: 'VERIFY_BOARDING'; id: string }
  | { type: 'COORDINATE'; id: string; assignee: string }
  | { type: 'SELECT_STOP'; stopId: StopId }
  | { type: 'REQUEST'; stopId: StopId; assistanceType: AssistanceType; note: string }
  | { type: 'ACKNOWLEDGE'; id: string }
  | { type: 'BEGIN_BOARDING'; id: string }
  | { type: 'COMPLETE'; id: string }
  | { type: 'FAIL'; id: string; reason: FailureReason }
  | { type: 'CANCEL'; id: string }
  | { type: 'OBSTRUCT'; objectClass: 'car' | 'motorcycle' | 'truck'; stopId: StopId; imported?: ValidAiEvent }
  | { type: 'CLEAR_OBSTRUCTION'; id?: string }
  | { type: 'IMPORT_CLEAR'; event: ValidAiEvent }
  | { type: 'ACK_WARNING'; id: string }
  | { type: 'REVIEW_INCIDENT'; id: string; note?: string }
  | { type: 'REVIEW_REQUEST'; id: string; note?: string }
  | { type: 'PRESET'; scenario: Scenario }
  | { type: 'GUIDE_START'; outcome: 'success' | 'failure' }
  | { type: 'GUIDE_NEXT' }
  | { type: 'RESET' };
export interface ValidAiEvent {
  schema_version: '1.0'; event_id: string; episode_id?: string; event_type: 'OBSTRUCTION_DETECTED' | 'OBSTRUCTION_CLEARED';
  scenario_id?: string; stop_id: StopId; route_id: 'DEMO-R01'; timestamp: string;
  source_mode: 'manual_simulation' | 'recorded_video_model_inference'; deployment_status: 'prototype';
  object?: { class: 'car' | 'motorcycle' | 'truck'; confidence?: number }; zone?: { id: string; dwell_seconds?: number; overlap_ratio?: number };
  review_status?: 'PENDING_OPERATOR_REVIEW' | 'REVIEWED'; is_demo: true;
}
