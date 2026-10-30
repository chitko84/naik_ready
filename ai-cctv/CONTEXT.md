# CONTEXT.md — NaikReady 5G | Aung Zay Yan Phyo

> **Owner:** Aung Zay Yan Phyo  
> **Workstream:** NaikReady Vision AI — Smart CCTV Boarding-Zone Obstruction Detection  
> **Competition:** Cyberjaya 5G Future Talent Innovation Challenge 2026  
> **Track:** 5G Connected & Safe Last-Mile Mobility  
> **Final submission:** Friday, 30 October 2026, 11:59 PM Malaysia time (MYT)  
> **Build type:** AI DEMONSTRATION PROTOTYPE — prerecorded footage, local inference, no deployment claim  
> **Document version:** 1.0 — 25 October 2026

---

## 0. PRIMARY INSTRUCTION FOR THE AI CODING ASSISTANT

**Read this entire specification before generating code.** You are an applied computer-vision engineer and professional Python dashboard developer. Build a complete, runnable **NaikReady Vision AI** demonstration with a beautiful visual interface, working pretrained object detection on authorized video, an editable boarding-area polygon, defensible obstruction logic, four repeatable scenarios, and event JSON output compatible with the NaikReady web prototype. Write actual Python project files, example configuration, tests, and a README. Prefer a **small working prototype** over unimplemented research features.

Do **not** build or require paid cloud AI, model training, live surveillance, facial recognition, real 5G equipment, access to city cameras, a production backend, or public-road enforcement. Detection is a **potential obstruction flag**, not a formal safety determination. Pre-recorded demonstration video is sufficient. Whenever content is manually staged or simulated, label it accurately. Never claim an invented confidence score was returned by a trained model.

**Definition of success:** A judge watches a short authorized recorded clip showing a vehicle entering a marked bus-stop bay; the running YOLO model identifies it, the demo tracks its presence in the zone over time, the dashboard flags a possible obstruction, and the app exports a clearly labeled JSON event that Min's UI could import.

---

## 1. PROJECT IDENTITY, PURPOSE AND REAL-WORLD CONTEXT

- **Parent project name:** `NaikReady 5G`
- **AI demo product name:** `NaikReady Vision AI`
- **Subtitle:** `AI Smart CCTV — Boarding Zone Awareness`
- **Tagline:** `See the blockage. Support the boarding.`
- **Core transport problem:** Buses may arrive at stops whose boarding areas are obstructed. Drivers and operators may not know this in advance, especially when a passenger needs accessible boarding.
- **Your module's job:** Detect and visualize likely vehicles occupying a user-defined boarding area, and **propose** an obstruction alert for human review. This is only one sensor input to the broader assistance workflow.
- **Other modules:** Min: passenger/driver/operator demo; Chit: interactive Blender/React 3D bus stop. The three modules share event names but do **not** require live API integration.
- **Intended users:** Prototype reviewers, transit operations staff, system designers. Not a deployed public safety tool.
- **Role of 5G in concept:** A future roadside sensor might transmit filtered alerts and optionally evidence snapshots/video over wireless 5G. **This local prototype processes recorded video; it does not test or simulate measured 5G throughput or latency.**

### One-sentence product pitch

> NaikReady Vision AI uses computer vision to flag vehicles that remain inside a designated bus boarding zone and provides evidence that a driver or operator can review before assisted boarding.

---

## 2. PROFESSIONAL BRAND & VISUAL DESIGN SYSTEM

Follow the same overarching NaikReady visual identity as Min's web app, but make this module feel like a high-end **transport AI monitoring console**. Reference the previously shared AI mockups: spacious primary CCTV feed, red or amber detection overlays, dark navy sidebar, clean bright panels, clear controls and four photographic scenario cards. Do not fake a live municipal CCTV connection.

### Visual tokens

| Token | HEX | Meaning |
|---|---|---|
| `NAVY_950` | `#071C36` | Sidebar and important headings |
| `NAVY_800` | `#11365A` | Header/dashboard text |
| `BLUE_600` | `#1769E0` | Active menu, standard actions |
| `TEAL_600` | `#008F96` | Brand and detected/integration accents |
| `TEAL_400` | `#20C4BA` | Highlights, gradient accent |
| `GREEN_600` | `#159B72` | No potential obstruction found / cleared |
| `AMBER_500` | `#F2A633` | Uncertain, review needed |
| `RED_600` | `#DD4052` | Potential obstruction detected |
| `CANVAS` | `#F5F8FC` | Page background |
| `SURFACE` | `#FFFFFF` | Controls / panels |
| `BORDER` | `#E2EAF1` | Card outlines |
| `MUTED` | `#62768A` | Supporting text |

Fonts: Inter preferred, or system-ui. Rounded cards (12–18px); subtle border/shadow; strong data hierarchy; very legible object classes, confidence and timestamps. UI should be usable at 1280×720 and 1440×900 without horizontal scrolling. A mobile view is nice but not necessary for the CCTV workstation; keep page responsive at tablet width.

### Logo direction

Use the same main `NaikReady 5G` wordmark as Min. Add a companion module icon: circular camera lens + scanning arcs + a tiny bus-stop outline. Subtitle `VISION AI`. Create a simple original inline SVG/logo if Min's shared asset is unavailable. **Do not use official transport-authority, CCTV vendor, or YOLO trademarks as if they were partners.**

### Exact dashboard layout

**Desktop left rail** (about 220–260px): logo, `Live/Video Detection`, `Detection History`, `Test Scenarios`, `Zone Configuration`, `About Prototype`; model info and `DEMO — RECORDED FOOTAGE` label.

**Top navigation:** `NaikReady Vision AI`, selected `Demo Stop: CYB-DEMO-01`, selected file, model name, run/pause status, `Export JSON`.

**Main grid (hero):**
- Large 16:9 annotated video frame occupying about **65%** width.
- **Right column** with `Boarding Zone Status` card, `Detected Objects` list, configurable threshold/control card, small zone preview.
- Clear overlaid dashed polygon marking the boarding area; bounding boxes with `car 0.92`, `motorcycle 0.86`, `bus 0.90` labels, with **actual** model confidence only.

**Second row:** four scenario cards with still image/frame and status pill (Normal / Car Blocking / Motorcycle Blocking / Cleared).

**Bottom:** event/detection history table and a modest data panel with **recorded test counts**; avoid made-up city-wide analytics. Label all numbers as `Current Test Run` or `Example Demo Data`.

**Optional extras:** editable region handles, frame scrubber, detection object filters, analysis FPS meter (measured not invented).

---

## 3. RECOMMENDED TECH STACK — LIGHTWEIGHT AND OFFLINE-FRIENDLY

| Component | Tool | Purpose |
|---|---|---|
| Runtime | **Python 3.11+** | Core logic |
| Detection | **Ultralytics YOLO** pretrained small/nano object detector | Detect car, motorcycle, bus, truck |
| Video | **OpenCV (`cv2`)** | Decode video, draw boxes, polygons, save clips |
| Geometry | OpenCV polygon operations; optional Shapely | Test if tracked object occupies bus bay |
| Numeric | NumPy | Coordinates and processing |
| Dashboard | **Streamlit** | Upload, process, monitor, scenarios |
| Data/events | JSON and CSV files | Export demo events and incident history |
| Visual charts | Streamlit native charts or Plotly (optional) | Count chart |
| Automated tests | pytest | Verify zone logic and cooldown |
| Editor | VS Code | Development |
| Git | GitHub repository | Source sharing |

**Model:** Start with a lightweight pretrained Ultralytics vehicle detector such as `yolo11n.pt` if supported by installed version. Do not depend on a GPU; limit frame size/inference frequency if CPU-only. Check current library interface and model asset availability, and document any substitute. Do **not** train from scratch.

**Licensing:** Ultralytics software/models may be subject to AGPL-3.0 or commercial licensing requirements. Record the exact package version/licence and do not promise unrestricted proprietary reuse.

---

## 4. REQUIRED FEATURES — EXACTLY 10 MVP FEATURE GROUPS

### Feature 01 — Video import and sample operation

Upload one authorized MP4 file. Support a bundled *license-cleared* sample if available; otherwise show a friendly drag-and-drop upload instead of inventing footage. Detect clip metadata (resolution, FPS, duration) and display `Recorded Video Analysis — NOT LIVE CCTV`.

### Feature 02 — Real pretrained AI vehicle recognition

Actually run a pretrained object detector on video frames. Detect classes `car`, `motorcycle`, `bus`, optionally `truck`. Show class, object-level confidence and bounding boxes. The app must **not** pretend drawn boxes are YOLO output without model inference.

### Feature 03 — Configurable boarding-area polygon

Show editable vertices if practical; at minimum provide a clear zone configuration through normalized polygon points. Allow enable/disable overlay and save zone settings. Different camera perspectives require different polygons.

### Feature 04 — Zone overlap / object-position evaluation

Use a consistent rule such as **detected object bottom-center point within polygon** or **minimum footprint/box overlap ratio**. Document choice and limitations. Merely passing through the polygon must not immediately create a persistent obstruction incident.

### Feature 05 — Dwell-time / obstruction-event detection

Maintain lightweight object tracking (YOLO's built-in tracking if stable; otherwise frame-to-frame approximation with clear documented limitations). Flag **potential obstruction** when a non-bus vehicle remains within the zone for a configurable duration (demo default **10 seconds of video time**, adjustable 3–15s). Apply a brief cooldown to avoid duplicate events. **A bus arriving normally is not automatically an obstruction.**

### Feature 06 — High-clarity annotated video monitor

Paint translucent zone polygon, colored bounding boxes and alert labels. Status: `CLEAR / NO POTENTIAL OBSTRUCTION OBSERVED`, `POTENTIAL OBSTRUCTION — REVIEW`, or `UNCERTAIN / INSUFFICIENT EVIDENCE`. “CLEAR” describes only the monitored zone and frame, not overall safe boarding.

### Feature 07 — Alert detail panel and evidence

Show vehicle type, actual detection confidence, estimated dwell duration, video timestamp, stop ID, and event review status. When a scene is blocked, visually emphasize the incident with red or amber; when it is cleared, resolve the sensor condition without claiming successful passenger boarding.

### Feature 08 — Four repeatable scenarios

Demonstrate: `Normal/Clear`, `Car Blocking`, `Motorcycle Blocking`, `Obstruction Cleared`. Prefer real sample segments or staged recordings. If using synthetic UI buttons without corresponding video detection, explicitly label as **Manual Simulation**. A sample bus arrival can be a fifth optional scenario.

### Feature 09 — Detection event history and export

Keep a session-local incident log: timestamp (or clip time), object class, score, zone status, duration, evidence provenance. Export events to `.json` and incident table to `.csv`. Prevent one alert per video frame. Use the exact shared event contract below.

### Feature 10 — Quality/limitations report

Display the model used, video source, known limitations and simple recorded-test summary. Clearly distinguish actual detections from manually created fixture values. Demonstrate at least one negative test to explain false alarms and limitations.

---

## 5. OPERATING LOGIC — IMPLEMENT SIMPLY AND CORRECTLY

### Inputs

- video file (user-supplied or permissioned sample)
- selected demonstration stop: `CYB-DEMO-01`
- area polygon points normalized to `(x,y)` between 0 and 1
- detection confidence threshold (suggest **0.35** default, user adjustable)
- obstruction dwell threshold (suggest **10 seconds**)
- object types monitored: `car`, `motorcycle`, `truck`; recognize `bus` but **don't auto-classify an arriving bus as an obstruction**

### Processing pipeline

```text
Authorized MP4/video
   ↓ decode frame (OpenCV)
Pretrained YOLO inference (actual model)
   ↓ object boxes, classes, confidence
Filter relevant classes, draw bounding boxes
   ↓ estimate object position relative to polygon
Temporal tracking + dwell timer
   ↓ if eligible vehicle in boarding zone long enough
Create POTENTIAL obstruction event with video timestamp
   ↓ show dashboard + history + JSON export
When vehicle leaves / is no longer confirmed:
   ↓ emit OBSTRUCTION_CLEARED after a stable clearance window
```

### Example pseudocode (only as guidance; implement actual code)

```python
if object_class in {"car", "motorcycle", "truck"} and inside_boarding_zone(track):
    start_or_continue_timer(track_id, video_time_s)
    if dwell_seconds(track_id, video_time_s) >= dwell_threshold and not already_reported(track_id):
        register_event("OBSTRUCTION_DETECTED", track)
else:
    mark_track_outside(track_id)
```

Important edge cases: temporary occlusion, dropped frames, stationary camera shake, bus pulling into stop, two cars simultaneously, camera angle foreshortening, small distant objects, false-positive classifications. **Don't silently mark a zone clear based only on a missing detection in one frame**: use timeout/clearance hysteresis.

### Performance expectation

Real-time speed is a *nice-to-have*. CPU processing of a prerecorded clip at reduced resolution and reduced sample FPS is acceptable. Provide frame progress and processing status. Do not claim GPU speed or 5G latency not measured.

---

## 6. SHARED EVENT CONTRACT — MUST MATCH MIN AND CHIT

Use these shared names:

```text
OBSTRUCTION_DETECTED
OBSTRUCTION_CLEARED
ASSISTANCE_REQUESTED
DRIVER_ACKNOWLEDGED
BOARDING_COMPLETED
BOARDING_FAILED
OPERATOR_REVIEWED
DEMO_RESET
```

**Aung owns only `OBSTRUCTION_DETECTED` and `OBSTRUCTION_CLEARED`.** Min owns passenger requests, driver acknowledgements and boarding outcomes. Chit uses event `scenario_id` to animate 3D.

### Sample export — schema v1.0

```json
{
  "schema_version": "1.0",
  "event_id": "demo-evt-0001",
  "event_type": "OBSTRUCTION_DETECTED",
  "scenario_id": "CAR_BLOCKING",
  "stop_id": "CYB-DEMO-01",
  "route_id": "DEMO-R01",
  "timestamp": "2026-10-27T10:24:18+08:00",
  "source_mode": "recorded_video_model_inference",
  "deployment_status": "prototype",
  "object": {
    "class": "car",
    "confidence": 0.92
  },
  "zone": {
    "id": "boarding-zone-01",
    "dwell_seconds": 12,
    "overlap_ratio": 0.45
  },
  "review_status": "PENDING_OPERATOR_REVIEW",
  "is_demo": true
}
```

**This JSON is a contract example, not evidence of actual inference.** Never emit the sample confidence `0.92` as a model measurement unless your model truly produced it in that clip. `source_mode` values:
- `recorded_video_model_inference` — object detection is real model inference on a prerecorded or staged clip;
- `manual_simulation` — developer manually triggers fixture and no model inference is claimed.

For cleared state use `"event_type": "OBSTRUCTION_CLEARED"` and `"scenario_id": "NORMAL"`; omit `object` when not applicable. Export event(s) in an array for Min's `Import AI Event JSON` demo button. **No FastAPI server or authenticated endpoint is required.**

---

## 7. EXPECTED PAGES/TABS — 5 PRIMARY SECTIONS

1. **Video Detection** — upload, run analysis, annotated frame/video, current zone status, object list.
2. **Detection History** — sortable event table with export JSON and CSV.
3. **Test Scenarios** — four scenario cards with clearly attributed recorded-video inference or manual simulation.
4. **Zone Configuration** — boarding area polygon, confidence threshold, dwell duration, test overlay.
5. **About / Technical Notes** — architecture, model name/version, demo limitations, future 5G concept, privacy.

Avoid turning this into a complex platform; **one Streamlit dashboard with tabs is acceptable** and may be faster/safer than multiple pages.

---

## 8. RECOMMENDED PROJECT FILE STRUCTURE

```text
naikready-vision-ai/
├── app.py                  # Streamlit front-end
├── vision/
│   ├── detector.py         # YOLO inference
│   ├── boarding_zone.py    # polygon region evaluation
│   ├── obstruction.py      # temporal rule, tracking, cooldown
│   ├── event_export.py     # schema and JSON output
│   └── overlay.py          # draw polygon/boxes/status
├── config/
│   └── demo_zone.json      # normalized ROI, thresholds
├── tests/
│   ├── test_zone_logic.py
│   ├── test_obstruction.py
│   └── test_event_schema.py
├── examples/
│   └── sample-obstruction-event.json
├── assets/
│   └── README_ASSETS.md    # footage provenance/licensing
├── requirements.txt
├── README.md
└── CONTEXT.md
```

Only bundle video when you have permission and a reasonable file size. If not, use `assets/README_ASSETS.md` to tell the reviewer how to add their own authorized MP4.

---

## 9. TEST CASES, QUALITY CONTROL AND SAFETY

### Minimum test cases

| # | Test | Expected result |
|---|---|---|
| T1 | Empty bus stop | No potential obstruction event |
| T2 | Car stationary in polygon beyond threshold | One `OBSTRUCTION_DETECTED` event |
| T3 | Motorcycle stationary in polygon beyond threshold | One `OBSTRUCTION_DETECTED` event |
| T4 | Car briefly drives through zone | No long-dwell alert |
| T5 | Bus stops normally | No parking-obstruction event based only on bus classification |
| T6 | Car moves away | After clearance window, `OBSTRUCTION_CLEARED` |
| T7 | Ambiguous/low-confidence classification | Uncertain, not definitive alarm |
| T8 | Export then import JSON in Min's demo | Schema accepted, relevant state appears |

### Important integrity requirements

- These are **prototype AI inferences on prerecorded footage**, not production monitoring.
- AI classification does not establish legal parking violations, boarding safety, or traffic authority actions.
- Never infer passenger disability or identity through CCTV. Do not use facial recognition.
- Blur or avoid identifiable faces/license plates where reasonable and obtain appropriate filming/usage consent.
- Keep confidence scores honest; sampled inference FPS and clip statistics must reflect actual computation.
- Avoid storing unnecessary personal data; prefer local-only processing.
- Add an explicit `System Limitations` panel noting possible false positives, occlusions, visual conditions, camera angle sensitivity, and threshold effects.
- Never infer that obstruction clearance equals successful wheelchair boarding; only driver/operator can record that outcome.
- Use videos and images you have rights to process. Avoid unlicensed copyrighted clips for public submission.
- Revalidate Ultralytics licence before shipping/redistributing a product commercially.

---

## 10. ACCEPTANCE CHECKLIST — MUST PASS

- [ ] `python -m pip install -r requirements.txt` works on a typical Python environment.
- [ ] `streamlit run app.py` starts without traceback.
- [ ] Original NaikReady wordmark and brand design are visually consistent with Min's app.
- [ ] Uploaded authorized video is processed using an actual pretrained YOLO model.
- [ ] Bounding boxes display class + **real** model confidence.
- [ ] ROI polygon is visible, configurable and correctly scaled on resized video frames.
- [ ] Vehicle inside zone beyond threshold triggers a clear **potential** obstruction event.
- [ ] Passing vehicle does not trigger the same alarm as long-dwell vehicle.
- [ ] Recognized bus arrival is not automatically classified as illegal parking.
- [ ] Four scenario cards / states are demonstrable; synthetic states labelled as simulations.
- [ ] Event timeline does not create duplicate alerts every frame.
- [ ] Exported event is compatible with Min's v1.0 schema.
- [ ] Tests cover clear, blocked, passing, departure, low confidence and event schema.
- [ ] README details setup, sample data rules, limitations and command-line usage.

---

## 11. DELIVERY MILESTONES

| Date | Outcome |
|---|---|
| **25 Oct** | Set up Python + Streamlit + pretrained model; prove object detection on a short licensed clip. |
| **26 Oct** | Implement zone definition, dwell threshold and annotated output. |
| **27 Oct** | Dashboard, four repeatable demo states, incident history and JSON export. |
| **28 Oct** | Run negative tests, coordinate contract with Min, share screenshot/footage with Chit. |
| **29 Oct** | Freeze stable demo, record sample walkthrough, finish README and technical notes. |
| **30 Oct** | Submission verification only. |

### Coordination checklist

- Give Min: schema v1.0 sample JSON, event type descriptions, one screenshot, an annotated short clip.
- Give Chit: car/motorcycle bounding-box visual reference, detected vs cleared scenario IDs, and the timing sequence for synchronized 3D scenario animation.
- Get from Min: test confirmation that exported JSON produces the correct driver/operator warning in the web UI.

---

## 12. FINAL HANDOFF FILES

1. Working Python + Streamlit source code and `requirements.txt`.
2. Documented test video with permission, or instructions to load authorized footage.
3. Annotated sample detection frames / short video demonstrating clear and blocked conditions.
4. JSON event sample / export containing schema v1.0.
5. At least 4 polished dashboard screenshots: detection, car blocking, motorcycle blocking, clear.
6. `README.md` with installation, launch, demo steps and model/licence notes.
7. Short test matrix with honest pass/fail notes and known limitations.
8. A brief technical explanation of why roadside sensing matters, plus proposed future 5G architecture (not measured 5G claims).

---

## 13. FINAL EXECUTION REQUEST TO AI CODING ASSISTANT

> Build the runnable **NaikReady Vision AI** demo from this CONTEXT.md. Use Python 3.11+, OpenCV, a lightweight Ultralytics pretrained YOLO model and Streamlit. Implement genuine recorded-video object detection, customizable bus-bay polygon, temporal obstruction logic, polished CCTV monitoring UI, four demo scenarios, event history, and v1.0 JSON export. Create real project files, tests, and a complete README. No cloud dependencies or production backend. Never fabricate model measurements or call the demo live CCTV/5G. Prioritize a visually impressive, reliable review of a likely obstruction and its correct integration handoff to the NaikReady web prototype.
