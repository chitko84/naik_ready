# More real-life photography

Latest update: [photography additions and validation](documentation/MORE_REAL_PHOTOS.md). [Windows setup commands](SETUP_GUIDE.md).

# Simple, natural UI/UX

The latest interface follows the [usability update and acceptance review](documentation/SIMPLE_UX_ACCEPTANCE.md). This supersedes the earlier decorative motion styling. All original photographs, credits and operational controls are retained.

# Photography refresh

Latest visuals and validation: [photography update](documentation/PHOTO_REFRESH.md). Windows installation commands: [SETUP_GUIDE.md](SETUP_GUIDE.md).

# Final visual polish

See [visual update notes](documentation/FINAL_POLISH.md) for the latest animation, accessibility and verification details.

# NaikReady 5G — Smart Boarding Assurance Platform

Unified competition application integrating Min Khant Maung’s React prototype, Aung Zay Yan Phyo’s YOLO CCTV project and Chit Ko Ko’s Blender digital twin.

Latest UI/control update: **documentation/UPDATE_2_1.md**. Start with **SETUP_GUIDE.md**. Final verification, evidence and limits are in **TEST_REPORT.md**. The before/after feature inventory is in **documentation/FEATURE_INVENTORY.md**.

## Included

- Passenger portal: two stops, six assistance categories, validated requests, tracking, cancellation and history.
- Driver dashboard: shared request queue, stationary response controls, acknowledgment, zone/alignment/ramp verification, boarding outcomes and failure reasons.
- Operator center: preserved eight sections, filters, search, outcomes chart, incident details, response assignment, notes, clearance and review.
- Vision console: labeled scripted replay, supplied recorded YOLO run, image/video upload, polygon and dwell configuration, asynchronous inference, actual observations and explicitly applied sensor events.
- Blender-derived Three.js viewer: original environment, four principal scenes, one-click scenario selection, closer camera framing, orbit/zoom/reset, shared-state scenarios and rendered fallback when WebGL is unavailable.
- Central reducer: stop-specific lifecycle checks, timestamps, incident links, sensor-episode matching, deduplication, local persistence and same-origin tab synchronization.
- Searchable updates and request history, JSON history export, mobile bottom navigation and responsive layouts.

## Project layout

| Path | Contents |
|---|---|
| frontend/ | React / TypeScript / Vite application, tests, public GLBs/media and production build configuration |
| backend/ | FastAPI adapter and API tests; runtime results generated locally |
| ai-cctv/ | Original Streamlit/OpenCV/YOLO source, model weights, tests, notices and useful supplied outputs |
| digital-twin/ | Unmodified .blend, original README, reproducible export/render scripts and export report |
| documentation/ | Feature inventory, architecture, interaction audit and actual test logs |

## Data and provenance

Workflow records are browser-local; they do not reach real transit staff. The same browser origin shares updates across tabs. Different devices do not share records. Keep one origin throughout a demonstration; localhost:5173 and localhost:8000 have separate localStorage.

Scripted replay is labeled and has no fabricated confidence. The supplied real recorded run contains **zero** dwell-triggered obstruction events. Upload analysis executes the bundled YOLO model. An image reports occupancy observations only; it cannot establish stationary dwell. Video analysis combines vehicle bottom-center position inside a calibrated polygon with a stationary dwell threshold, then requests human verification. No measured 5G service or certified ramp geometry is claimed.

The browser twin uses four evaluated snapshots from the original animated scene. The full 600-frame animation, camera cuts and editable scene are preserved in the original .blend; they are not played as a continuous browser animation. Street geography is illustrative, and the same conceptual stop geometry represents both selected stops. Car geometry is representative when the advisory concerns another vehicle class.

## Source attribution

Original web application: Min Khant Maung. AI CCTV application: Aung Zay Yan Phyo. Blender digital twin: Chit Ko Ko. Aung’s AGPL-3.0-only LICENSE and NOTICE remain under ai-cctv; model and dependency licenses remain applicable. Full integration source is included. See documentation/CHANGES.md for integration modifications.
