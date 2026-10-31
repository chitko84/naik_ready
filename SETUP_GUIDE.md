# Windows + VS Code setup

Install Node.js 22 or 24, Python 3.12 and VS Code. Blender is optional: the GLBs and fallback images are already included. Extract the ZIP completely before starting. Open the extracted `NaikReady_5G_Unified_Premium_Prototype` folder in VS Code.

## 1. Install the Python backend

Open a **PowerShell** terminal in the project root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r backend\requirements-local.txt
```

Inference uses CPU. Torch is a large dependency, but it is installed separately from the web interface. For an explicitly CPU-only Torch installation, run this before installing backend requirements:

```powershell
.\.venv\Scripts\python.exe -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

No model download is needed: `ai-cctv\yolov8n.pt` is included.

## 2. Install and run the application

From the project root:

```powershell
cd frontend
npm ci
npm run dev
```

Open **http://localhost:5173**. The development runner detects the root `.venv` and starts the Vision API on **127.0.0.1:8000**, then Vite. Keep the terminal open. Ctrl+C stops both services. After installation, `START_WINDOWS.bat` starts the same command.

If Python is installed elsewhere, set its absolute path before startup:

```powershell
$env:NAIKREADY_PYTHON = "C:\path\to\python.exe"
npm run dev
```

If the API cannot start, replays and all local workflows still work; uploads show the API-offline message. API documentation is available at **http://127.0.0.1:8000/docs**.

## 3. Run services separately (optional)

Terminal 1, project root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Terminal 2:

```powershell
cd frontend
npm run dev:frontend
```

Vite proxies `/api` to Python. Do not run two backends on port 8000.

## 4. Build and serve from one origin

```powershell
cd frontend
npm run build
cd ..
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Open **http://localhost:8000**. The Python server serves the built frontend, SPA routes, media and the API together. Rebuild after changing frontend source. The `frontend\dist` output is generated locally by `npm run build`; source and package-lock are authoritative.

## 5. Demonstrate the complete journey

1. Open Scenario Lab. Reset if old test records exist. Start the successful guided journey, or choose a blocked scenario.
2. In Passenger, select the stop and submit Wheelchair / Ramp support.
3. In Driver, enable **Bus safely stationary**, then acknowledge the request. Boarding stays disabled while an obstruction remains active.
4. In Operator → Incidents, open the case, assign the attendant, save notes and mark the obstruction cleared after verification.
5. Return to Driver, enable stationary controls again if the page remounted, verify the clear zone/alignment/ramp, begin boarding and record completion.
6. Check Passenger status, Operator outcomes, Activity history and the updated twin.
7. Use the unsuccessful guided journey to demonstrate blocked boarding and operator review.

For CCTV, open Digital Twin / AI. **Scenario analysis** works immediately without Python: choose Clear zone, Parked car, Motorcycle or Zone cleared, then Analyze boarding area and optionally share the resulting advisory. Evidence source details are available in the evidence panel. **Video evidence** shows the supplied 80-frame inference run with zero obstruction events. **Analyze a file** accepts images or videos (40 MiB, maximum 60-second video), a selected stop, normalized polygon and 1–30-second dwell threshold. Review the results and apply any actual sensor events. No event is generated from a single image.

An uploaded image/video preview is local; clicking Run YOLO analysis sends it to the local Python API. Results and annotated final-frame evidence are kept under backend/runtime. Input uploads are removed after processing. Use authorized test footage and calibrate the polygon to each camera.

## 6. Tests

```powershell
cd frontend
npm test
npm run build
cd ..
.\.venv\Scripts\python.exe -m pip install -r backend\requirements-test.txt
.\.venv\Scripts\python.exe -m pytest -q backend\tests
.\.venv\Scripts\python.exe -m pip install -r ai-cctv\requirements.txt
cd ai-cctv
..\.venv\Scripts\python.exe -m pytest -q tests
```

The last command also needs pytest installed in the venv (provided by requirements-test.txt).

## 7. Original projects and Blender

The standalone CCTV console remains available:

```powershell
cd ai-cctv
..\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the original .blend in Blender **5.2 or newer**, then Space to play frames 1–600. To recreate browser snapshots from the root (replace the executable path with your installation):

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b digital-twin\NaikReady_5G_Final_Digital_Twin.blend --python digital-twin\export_browser.py
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b digital-twin\NaikReady_5G_Final_Digital_Twin.blend --python digital-twin\render_fallback.py
```

Exporting does not overwrite the source .blend. Native camera cuts and full animation remain in Blender; the browser uses optimized scenario snapshots. Enable browser hardware acceleration for interactive WebGL orbiting. Without WebGL, the app shows original Blender renders with zoom/reset controls.

## Troubleshooting

- **`npm` or `py` not recognized:** restart VS Code after installing Node/Python.
- **API offline:** check the terminal, the .venv installation and port 8000. Use separate service commands to see the Python error directly.
- **Long first analysis:** model initialization and CPU inference take time; job progress appears in the console.
- **No detections/events:** this is a valid outcome. Check the image, camera polygon, vehicle labels, motion and dwell duration. A vehicle must satisfy the zone/dwell rule before an event is emitted.
- **Session data differs across pages/devices:** use the same origin. Persistence is local to that browser, not a multi-user server database.
- **Reset:** Scenario Lab → Reset all clears local workflow records; it does not delete analysis evidence on disk. Export history first if needed.
- **Missing thumbnails/GLBs:** run through the web server rather than opening index.html with file://.


## Latest map and scene controls

Normal, Blocked, Assistance and Resolved apply on a single click, including after a completed journey. The selected scene is shared across twin views and resets to operational state when a new request/sensor action arrives. Normal does not delete boarding history. Repeated Blocked clicks do not create duplicate incidents.

The Route Map has bundled Cyberjaya street/building data, zoom controls, Fit entire route, stop focus, an expanded view, Street/Diagram switching and a route animation. It needs no map API key or online tile service. Route geometry/vehicle preview remain planning illustrations, not measured GPS.

After replacing an older project with this update, run `npm ci` again in frontend to install Leaflet. Existing browser records remain compatible.
