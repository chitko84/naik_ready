> Historical report for the previous release. The current UI/control update and verification results are in documentation/UPDATE_2_1.md.

# NaikReady 5G — Final test report

Verified 29 October 2026 (Asia/Kuala_Lumpur). Results below are actual execution results, not intended checks. Raw outputs are under documentation/.

## Automated checks

| Check | Result | Evidence |
|---|---|---|
| Frontend TypeScript + Vite production build | PASS | documentation/BUILD_OUTPUT.txt |
| Workflow / validation / persistence tests | 16 passed | documentation/FRONTEND_TEST_OUTPUT.txt |
| Four GLB assets parsed by Three.js GLTFLoader | 4 passed | documentation/FRONTEND_TEST_OUTPUT.txt |
| Original Aung CCTV tests (monitor, export, media and Streamlit dashboard) | 19 passed | documentation/ORIGINAL_AI_TEST_OUTPUT.txt |
| New API tests, including real image and video model calls | 6 passed | documentation/API_TEST_OUTPUT.txt |
| Original Blender source preserved byte-for-byte | PASS | SHA256 394ad5d0211a1a1e8b555536d99f511bca6addf602f761a143b10bc76e335571 |
| Browser GLB headers, lengths, materials and finite scene bounds | PASS | Four exported assets / loader tests |

**45 tests passed in total.** There were no pre-existing frontend automated tests in the supplied ZIP; the new frontend suite verifies its original workflows plus the integration rules.

The production build retains Vite’s advisory about Three.js chunk above 500 kB. They are separate from the main application and React chunks and load only on relevant routes/features. This advisory is not a compilation failure. API testing emitted a dependency deprecation warning from the installed Starlette/httpx test-client combination; all six tests passed.

## Actual model execution

The bundled YOLOv8n weights loaded and CPU inference executed. API image test: one supplied annotated reference image, one frame processed, zero detections and zero events. API video test: a controlled three-second, 15-frame video made from that reference image, 15 actual model calls, zero detections and zero events. These tests establish that decoding/model/API/result/evidence paths work; they are **not** evidence of field detection accuracy or obstruction recall.

The supplied prerecorded actual YOLO run reports 80 frames and zero dwell-triggered events. The scripted replay reports 288 frames and four events, with model_executed=false and no model confidence. These sources remain clearly separated in the interface. The preserved original monitor tests cover dwell, motion reset, timeout, clear debounce, bus exemption, motorcycle blocking, multiple tracks and simulation provenance. No invented score or generic vehicle-to-obstruction conversion was introduced.

## Browser interaction verification

Chrome preview verified:

- Landing page and all nine application routes load; unsupported paths retain the original home redirect.
- Passenger required-choice validation displays an error before submission.
- Wheelchair/ramp request with a note reaches the shared driver queue and passenger timeline.
- Driver response is disabled before stationary confirmation. Acknowledgment alone does not enable boarding; zone/alignment/ramp verification is required.
- Driver verification → begin boarding → completion updates the Operator outcome count and activity log.
- Scripted CCTV event application creates an operator incident and updates the twin to Blocked.
- Operator incident details, assignment to a station attendant, clearance and saved review notes work. Saved notes and workflow records were verified after reload.
- Rendered fallback zoom/reset controls and scene updates work when WebGL is unavailable.
- Mobile bottom navigation is visible on narrow viewports; route-specific controls remain available.

The interactive orbit renderer could **not** be visually exercised in this browser: its GPU/WebGL context is disabled (`GL_VENDOR = Disabled`). Rather than representing the SVG as 3D, the application shows actual Blender-rendered fallback images. Four GLBs were successfully exported with Blender 5.2.3, parsed by Three.js, and checked for finite bounds/materials. Orbit/touch interaction on a WebGL-capable physical device still needs a device check.

The managed preview mirrors the frontend alone, so its local Python API is offline. Uploaded-media frontend/API interaction was verified through source/type checks and real FastAPI TestClient HTTP requests, not a cloud-browser file upload. The delivered local runner starts both services on a normal Windows machine; native Windows execution itself was not available here.

## Responsive verification

All nine routes were rendered in six iframe viewports: **320, 375, 390, 430, 768 and 1440 px** (54 route/viewport checks). DOM scrollWidth equaled clientWidth in every recorded check after fixing the original 340 px body minimum. Narrow iframe content was 15 px smaller where the browser reserved a scrollbar; the smallest checked content width was 305 px. Passenger mobile and desktop operator layouts were also visually inspected.

Mobile changes include five-role bottom navigation, safe-area padding, stacked evidence/configuration panels, touch-sized primary actions, responsive request summaries, mobile drawer padding and long-text wrapping. These are browser emulation checks, not physical-device or assistive-technology certification. Dynamic modal, keyboard and zoom combinations were not exhaustively tested at every size.

## Issues found and resolved

1. Original reducer allowed beginning/completing boarding with an active obstruction. Added stop-specific clearance and physical-verification gates; preserved inability-to-board reporting without a fictitious ramp deployment.
2. Imported clear events could affect unrelated incidents. Added source/episode/stop/time matching and deduplication tests.
3. Scripted confidence=null and legacy stop IDs broke integration with Aung’s exported events. Added compatible normalization; no score is fabricated.
4. Original car/motorcycle schema did not accept the detector’s truck output. Added truck compatibility throughout records and validation.
5. Original body min-width caused overflow at 320 px. Fixed sizing and verified 54 combinations.
6. Source Blender was written by 5.2. An initial 5.0 inspection warned about a newer file; final exports/renders used matching Blender 5.2.3.
7. Original opening fade produced a dark Normal fallback. Rendered the Normal view at frame 40 with a fixed camera/daylight setup; visually checked the corrected image.
8. Original terminal timelines could imply an unperformed boarding attempt. Cancellation and blocked outcomes now show only applicable stages and timestamps.
9. General case notes had no save action outside failed cases. Added meaningful note saving without closing pending requests.
10. The first frontend test runner required an unavailable IPC socket. Switched to Node’s test runner with the tsx loader; all 20 frontend tests pass.

## Remaining limitations

- Browser 3D uses four native-scene snapshots with loading fades; full continuous Blender animation, original camera cuts, procedural effects and cinematic lighting remain in the supplied .blend. Browser lighting approximates original materials. No continuous browser animation is claimed.
- Twin geometry is a conceptual scene reused for both stops. Non-car advisories use labeled representative car geometry; the original schematic source remains retained.
- Browser records are local and last-writer across tabs, not a multi-user backend database. There is no authentication, live bus connection, real notification delivery or measured 5G service.
- GPU rendering, Windows dependency installation, long/large upload performance and physical mobile touch behavior remain environment/device dependent.
- The vision model, simple IoU tracker and bottom-center dwell rule require field calibration and validation. Occlusion, perspective, false positives and false negatives are possible; only human verification enables boarding.
- Video API limits: 40 MiB, 60 seconds, 12,000 source frames; analysis samples approximately 5 FPS. Evidence is the annotated final frame, not a complete newly encoded video. The original standalone CCTV processor retains its full annotated-video output functionality.
- Interrupted server jobs are not resumed automatically. Runtime evidence is local and excluded from the delivered archive.
