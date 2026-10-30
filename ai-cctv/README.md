# NaikReady Vision AI

**AI Smart CCTV — Boarding Zone Awareness**  
See the blockage. Support the boarding.

A local Python / Streamlit console following the supplied navy-sidebar and bright-panel CCTV reference. Read `CONTEXT.md` for the full user specification.

## Windows installation

Extract the ZIP. Open the `naikready` folder, type `cmd` in Explorer's address bar, and press Enter. Install Python 3.12, then run:

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py --server.port 8520
```

Open http://localhost:8520 . Use this new port to avoid connecting to an older running copy. Next time run the same last command from this folder. The supplied weights are YOLOv8n; no training, cloud service or GPU is needed.

## Five working sections

- **Video Detection:** choose actual recorded-video processing or explicitly labelled manual simulation. Upload an authorized MP4 and run inference. A completed run shows the final encoded frame, predicted classes/confidence, source-video time, status and video download.
- **Detection History:** session-local episode table, Min v1.0 JSON-array export and CSV download.
- **Test Scenarios:** inspect four existing illustrated fixtures with scenario buttons and a snapshot slider. These are manual simulations with no model score; they are not photographic CCTV tests.
- **Zone Configuration:** edit normalized polygon vertices, confidence and dwell threshold; preview the polygon; save settings for this session or download a configuration file. Settings apply to the next analysis.
- **About Prototype:** architecture, limitations, model/licensing and the future 5G concept.

## Operating rules

Actual analysis defaults to **10 seconds** of nearly stationary presence inside the polygon (adjustable 3–15 seconds), confidence 0.35, and a 1-second stable clearance window. The object's bottom-center point is the position proxy. A simple one-to-one IoU tracker estimates continuity. Motion beyond the configured anchor tolerance resets dwell. Buses are detected and observed but do not automatically trigger obstruction alerts.

The short bundled illustrated sequence retains its **3-second** fixture threshold, 24-second duration, and start/clear transitions at 7, 12, 16 and 21 seconds. This exception is clearly labelled on-screen. Its confidence values are null. It demonstrates the same zone engine without pretending YOLO recognized the drawings.

Actual event generation uses video time, not processing speed. Short detection losses are tolerated and clearance is confirmed over a window. Confidence filtering, occlusion, shake, perspective and ID switches can still affect results. A lack of observations is presented as uncertain in the actual-analysis status panel. Clearance means the sensor condition cleared; it does not prove safe or completed passenger boarding.

## Integration contract

`event_export.py` adapts internal sensor episodes to the supplied v1.0 contract. Import `examples/sample-obstruction-events.json` as an **array** in Min's UI. Names are `OBSTRUCTION_DETECTED` and `OBSTRUCTION_CLEARED`; scenario IDs include `CAR_BLOCKING`, `MOTORCYCLE_BLOCKING` and `NORMAL`. Actual source mode is `recorded_video_model_inference`; illustrated fixtures use `manual_simulation`. No confidence or overlap ratio is invented. The position rule is included instead of an uncomputed overlap ratio. Export timestamps identify export generation, explicitly marked by `timestamp_kind`; `video_time_seconds` identifies the recorded offset. Session exports keep stable timestamps across rerenders.

**Min's actual importer has not been available for end-to-end acceptance testing.** Field names and shapes are checked locally; final importer acceptance must be confirmed with Min. No backend/API or message sending is implemented.

## Authorized footage

This package contains our illustrated scenario media and instructions to upload your own permissioned bus-stop recording. Previously downloaded public-road reference clips and their derived images are excluded from this release because redistribution permission was not established. The uploaded visual references guide the layout; they are not used as model evidence. See `assets/README_ASSETS.md`.

To produce real obstruction evidence, record a fixed view with permission. Include a clear zone, a car stationary for at least 12 seconds, clearance, then a motorcycle stationary for at least 12 seconds. Configure the polygon, process the clip, and manually verify the boxes/events. Use appropriate filming consent and avoid unnecessary identifiable footage.

## CLI

```bash
python detect.py --input path/to/authorized_clip.mp4 --config config.json --output outputs/my_test
```

CLI writes internal episode data and frames. The UI exports the shared contract via `event_export.py`. OpenCV's annotated MP4 export uses MP4V; download for VLC if your browser cannot play it. The bundled manual simulation has an optional WebM preview.

## Verification

```bash
python -m pip install pytest
python -m pytest -q
```

19 automated checks cover the existing zone/dwell engine, moving vehicles, bus exemption, clearance, expiry, one-to-one tracking, schema conversion and current UI. Historical model execution on reference road footage is not target-site accuracy validation. No precision, recall, real-time FPS or 5G latency claim is made.

Ultralytics 8.4.187 was used in the earlier actual inference validation; YOLOv8n is retained as the lightweight available substitute for the suggested YOLO11n. See `requirements-tested.txt`, `LICENSE` and `NOTICE.md`. Dependencies and model licensing retain their own terms; the source is AGPL-3.0. No facial recognition or disability inference is implemented.

## Photorealistic scenario interface (latest update)

The main simulation view and four cards now use AI-generated photorealistic Malaysian bus-stop scenes in `assets/photoreal/`. They replace the cartoon stills in the interface, while preserving the actual uploaded-video analysis workflow. Show/hide the manually positioned zone and boxes using the display controls. The zone preview uses the generated scene too.

These are synthetic scene images, not real CCTV photographs. They are independent images, not one continuous recording. Their displayed states, fixture time, dwell and history are manual simulation; confidence remains unavailable. The expandable legacy illustrated video is separate and clearly labelled. Raw assets, prompt set, generation method and provenance are documented in `assets/photoreal/ASSET_NOTES.md`. `photo_scenarios.py` draws optional runtime presentation overlays. No new Python package is needed for this update.
