# NaikReady interface and interaction update

## Changes

- Fixed Normal remaining on Resolved after historical completed boarding. Explicit, stop-scoped scene selection now takes priority until the next operational action.
- Fixed Blocked opening Assistance when a request was pending. One click selects the requested scene; repeated clicks do not duplicate incidents. Original request/boarding history is preserved.
- Corrected a multi-stop request lookup used by scenario presets. Scene selection and new requests now remain scoped to their stop.
- Added closer 3D camera framing, balanced lighting, legible scene status bars and idempotent GLB loading.
- Replaced the cropped schematic-only map with a Leaflet vector map using 2,723 bundled OpenStreetMap road/building/park/water features for Cyberjaya. The map supports pan, zoom, route fit, stop focus, expanded view, route animation and the retained local diagram. Both street and diagram route previews move. No online tile server or API key is required.
- Added three real-world Pexels photos to the homepage, role cards, passenger support and fleet view; embedded locally with photographer/source credits in PHOTO_CREDITS.md.
- Added immediate Scenario analysis for four boarding-area conditions. The main interface uses neutral scenario/result language; expandable evidence details retain source provenance. No fabricated confidence is shown and uploaded-file failures are not replaced with unrelated scenario outputs.
- Fixed an infinite polling loop: a failed API job is now terminal. Added a four-minute wait limit, three-failure network limit, request timeouts, a Stop waiting action and visible model-initialization status. Stale jobs are marked failed after a backend restart.
- Preserved every route, original operator sections and standalone AI/Blender source. Route Map and Workspace Information are clearer labels for the former map/information sections.

## Verification in this update

- Production TypeScript/Vite build passed.
- 31 frontend tests passed (including the original 20 and 11 scene/polling/map regression tests).
- 19 original AI/CCTV tests passed.
- 6 API tests passed, including actual image/video inference. Total: 56 automated tests.
- Browser: Resolved → Normal → Blocked → Normal → Assistance → Blocked each showed its correct scene after one click. Fallback scene image and pressed state were checked.
- Browser: Scenario analysis returned a parked-car advisory immediately, without a running Python backend.
- Browser: bundled road/building geometry, zoom, Fit route, MMU selection, Play/Pause, expanded map and diagram switching/zoom were checked.
- Browser: all three photo assets loaded on the homepage; mobile menu opened and closed at 320 px.
- Responsive checks: nine routes at 320, 390, 768 and 1440 px; 36 combinations had no page-level horizontal overflow.

## Scope and limits

The browser environment disables WebGL. Scene selection, rendered fallback and GLB parsing were verified; native WebGL orbit interaction still needs a device check. The user-provided screenshot shows the original WebGL renderer working on their machine. Camera/lighting code changes compiled but are not claimed to be visually GPU-tested here.

Real model inference tests are execution checks, not field-accuracy evidence; their fixtures had zero detections/events. Scenario analysis uses supplied reference data, with source details available in the evidence panel. The vector street extract is real OSM geography; route/stop anchors and vehicle progress remain illustrative. Geographic data/attribution terms and photographer credits are included in PHOTO_CREDITS.md.

Original reports describe earlier releases; this document and UPDATED_* test logs cover the current changes.
