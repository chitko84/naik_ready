# Integration architecture

React 18 + TypeScript + React Router keep the supplied routes and components. The existing reducer is the shared operational model; new coordination and physical-verification actions extend it. localStorage retains records, storage events synchronize same-origin tabs, and hydration rejects malformed records. This is a competition workspace, not concurrent distributed storage; simultaneous writes in separate tabs can use last-writer behavior.

Three.js and GLTFLoader are lazy-loaded. Original Blender geometry is evaluated at frames 1, 190, 285 and 468, merged into material primitives, then exported as four GLBs (roughly 5.4–7.1 MB each). The viewer derives the visual mode from selected-stop obstruction/request records, uses damping and camera reset interpolation, and crossfades while a new snapshot loads. The full source animation remains editable in the .blend. Fallback JPEGs come from the original Blender scene using a consistent camera/daylight setup (normal fallback uses frame 40 after the original opening fade).

FastAPI adapts Aung’s actual `YoloDetector`, `ZoneMonitor`, annotation and event exporter. Models load only when analysis is requested. One inference worker limits CPU contention. Uploads are restricted by media extension/size and video metadata/duration. Image results contain observations without obstruction events. Video processing samples approximately 5 FPS and uses actual clip timestamps for dwell, with the original stationary and track-timeout rules. Results are written atomically to disk. Evidence is an annotated final frame; event history and per-frame JSONL are retained separately. API results do not automatically mutate workflow records: an explicit Apply action preserves reviewer control.

## API contract

| Endpoint | Behavior |
|---|---|
| GET /api/health | API and dependency/weight availability |
| POST /api/analyze | Multipart file, media_type, stop_id, zone JSON, dwell_seconds → 202 + job_id |
| GET /api/jobs/{job_id} | queued / processing / complete / failed, progress, observations and exported events |
| GET /api/jobs/{job_id}/evidence | Annotated JPEG final frame |
| GET /api/replay/simulation | Original scripted summary + schema-normalized events |
| GET /api/replay/recorded | Original recorded summary + zero obstruction events |
| GET /docs | FastAPI interactive schema |

Sensor events retain event and episode IDs, source mode, selected stop and timestamp. Legacy `CYBERJAYA-DEMO-*` stop IDs normalize to `CYB-DEMO-*`. Scripted null confidence stays null in the original exporter and becomes an absent metric when validated by the frontend. No overlap score is invented: the source rule uses bottom-center-in-polygon, not bounding-box overlap.

## Lifecycle rules

REQUESTED → DRIVER_ACKNOWLEDGED → verified clear zone/alignment/ramp → BOARDING_ATTEMPT → COMPLETED. Pending requests may be cancelled. Acknowledged or attempted requests may end UNABLE_TO_BOARD with a reason. A new same-stop obstruction invalidates physical verification. An active same-stop obstruction prevents starting/successful boarding; another stop’s advisory does not. Terminal requests cannot be reopened by driver actions. Operator review records follow-up without changing the boarding outcome.

Obstruction POTENTIAL → operator coordination/review → CLEARED. Manual clearance is scoped to the selected stop or selected incident. Sensor clearance matches the same source, stop, episode and chronological order, preserving unrelated incidents. Reset/guided-start are explicit scenario controls; guided-start resets the local workflow before replaying its eight moments.

## Performance and persistence limits

The main web UI never downloads the Python model. The initial JS bundle is split from charts and Three.js; heavier chunks are loaded by the routes/features that use them. The browser retains only the displayed GLB and disposes geometry/materials when replaced. Three.js pixel ratio is capped at 1.5. API jobs/evidence persist on the local filesystem; inputs are deleted on completion/failure. A server restart does not resume an interrupted job. No login, live CCTV ingest, real driver messaging, cloud synchronization or deployed 5G telemetry is implemented.
