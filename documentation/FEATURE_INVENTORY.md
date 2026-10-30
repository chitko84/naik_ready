# Feature inventory — inspected before integration

Foundation: Min Khant Maung’s supplied React 18 / TypeScript / Vite application.

| Original route / module | Existing functionality to preserve |
|---|---|
| / | Landing page, role links, guided walkthrough launch |
| /passenger | Two-stop selector, interactive schematic route map, simulated ETA, current request and alert |
| /passenger/request | Six assistance choices, required-choice validation, stop selection, 140-character note |
| /passenger/status | Timeline, latest outcome, pending cancellation, new request |
| /driver | Request selection, acknowledgment, boarding attempt, success/failure reasons, obstruction acknowledgment and detail |
| /operator | Eight sidebar sections, stop/fleet views, request search and filters, outcome chart, incident drawer, operator notes, clearance, failed-case review, activity log |
| /experience | SVG twin and conceptual AI view (integration targets) |
| /demo | Seven scenario presets, success/failure guided journeys, reset, activity log, validated JSON sensor import |
| Shared state | Reducer, stop-aware records, localStorage persistence, imported event deduplication, request-to-incident links |

Aung Zay Yan Phyo’s source: Streamlit console, OpenCV video decoder / annotation, Ultralytics YOLOv8n weights, normalized polygon editor, stationary bottom-center-in-polygon / dwell monitor, CSV and JSON event export, scripted scenes and real recorded-run outputs. Original source, license, tests, weights and useful media are retained under ai-cctv; the bundled Windows .venv is excluded.

Chit Ko Ko’s source: supplied Blender scene and animation; original README states conceptual visualization, 600 frames / 24 FPS. Source is retained under digital-twin.

## Integration targets
Python API for image / video inference and replay; shared stop-aware incident lifecycle with coordination; Blender-derived GLB snapshots and interactive Three.js viewer; CCTV upload and explicit event application; activity / notification history; responsive navigation and polished operational UI. Final verification and remaining limits are recorded in TEST_REPORT.md.

## Final preservation / additions

All original route paths remain. The eight operator section names and underlying views remain. All original assistance categories, boarding outcomes/failure reasons, scenario presets and successful/unsuccessful guided paths remain. Original SVG schematic source is retained as SchematicTwin.tsx; the main integration uses original Blender GLBs and rendered fallback.

Added modules: VisionConsole.tsx, Activity.tsx, FastAPI backend, Blender export/render scripts, test suites and Windows/local startup support. Central reducer functionality is extended rather than replaced. Model weights remain optional to web startup and included for local inference. The original AI project stays runnable independently.

See TEST_REPORT.md and INTERACTION_AUDIT.md for verified behavior and environment-dependent checks. Original frontend QA_REPORT.md and ORIGINAL_README.md are retained as historical source documentation.
