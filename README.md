# NaikReady 5G

### Clear boarding zones. Better support. More accessible journeys.

NaikReady 5G brings passenger assistance, driver response, CCTV evidence and an interactive 3D bus-stop twin into one connected prototype. It helps demonstrate how a boarding request moves from the passenger to the driver and operator, with a clear record of the outcome.

Built by students at **Albukhary International University, Malaysia**, for the **Cyberjaya 5G Future Talent Innovation Challenge 2026**.

[Quick setup](#quick-setup-windows) Â· [Features](#features) Â· [Deployment](#vercel-deployment) Â· [Documentation](#documentation) Â· [Team](#team)

---

## The problem

A vehicle parked in a bus-stop boarding zone can prevent a bus from aligning with the kerb and deploying its wheelchair ramp. Passengers may struggle to signal for assistance, drivers may lack advance information, and operators may have limited evidence for resolving an obstruction.

NaikReady connects these moments into a practical workflow: **request assistance â†’ review conditions â†’ respond â†’ record the outcome**.

## Features

| Workspace | What users can do |
| --- | --- |
| **Passenger** | Find a supported stop, choose from six assistance categories, submit a request, track its status, cancel an eligible request and review history. |
| **Driver** | Review requests, acknowledge an alert while stationary, verify the boarding zone and ramp conditions, and record successful or unsuccessful boarding. |
| **Operator** | Monitor requests and incidents, inspect available evidence, assign a response, add notes, clear incidents and review outcomes. |
| **CCTV / AI** | Explore scenario replay and supplied recorded YOLO evidence, or analyze an uploaded image or video with configurable boarding-zone and dwell settings. |
| **3D digital twin** | Switch between four principal scenes, explore the Blender-derived environment, and use orbit, zoom and reset controls. |
| **Scenario walkthrough** | Follow a guided journey and observe synchronized changes across the role-based workspaces. |

The interface also includes stop and fleet views, searchable activity, JSON history export, responsive navigation, and authentic photography with retained credits.

## User journeys

- **Passenger:** Find a stop â†’ Request assistance â†’ Track progress â†’ View the outcome.
- **Driver:** Review the request â†’ Acknowledge â†’ Verify boarding conditions â†’ Complete the action.
- **Operator:** Identify an incident â†’ Review evidence â†’ Assign a response â†’ Resolve and review.
- **Presentation:** Select a scenario â†’ Start the walkthrough â†’ Observe changes â†’ Review the outcome â†’ Reset.

## Technology

| Layer | Technology |
| --- | --- |
| Frontend | React, TypeScript and Vite |
| Maps and charts | Leaflet and Recharts |
| Interactive twin | Three.js with Blender-derived GLB assets |
| API | Python and FastAPI |
| Computer vision | YOLO, OpenCV and bundled model weights |
| Standalone AI console | Streamlit |
| Hosted configuration | Vercel services with a private AI service binding |

## Quick setup â€” Windows

### 1. Prerequisites

Install **Git**, **Node.js 22 or 24**, and **Python 3.12**. Open a new PowerShell window after installation.

### 2. Get the project

For a new local checkout:

```powershell
git clone https://github.com/chitko84/naik_ready.git
cd naik_ready
```

If you already have the project, open its root folder instead. It should contain `frontend`, `backend` and `ai-cctv` side by side.

### 3. Install the Python dependencies

Run from the **project root**, not your Downloads folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip

if (Test-Path .\backend\requirements-local.txt) {
    .\.venv\Scripts\python.exe -m pip install -r .\backend\requirements-local.txt
} else {
    .\.venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt
}
```

### 4. Install and start the application

```powershell
cd frontend
npm ci --include=dev
npm run dev
```

Open **http://localhost:5173/**.

The development script starts Vite and the local vision API together. It automatically uses the Python environment at the project root's `.venv` directory. Keep the terminal open; press **Ctrl+C** to stop.

## Checks and production build

From `frontend`:

```powershell
npm test
npm run build
```

The production frontend is generated in `frontend/dist`. To preview that build:

```powershell
npm run preview
```

The preview command serves the frontend only. Uploaded-media analysis still needs a running API.

For Python validation instructions and recorded verification results, see [TEST_REPORT.md](TEST_REPORT.md) and [VERCEL_SERVICES.md](VERCEL_SERVICES.md).

## Vercel deployment

Start with **[VERCEL_REDEPLOY.md](VERCEL_REDEPLOY.md)** before changing your Vercel project settings.

The supplied deployment configuration uses this layout:

| Service | Access | Purpose |
| --- | --- | --- |
| `frontend` | Public: `/` and non-API routes | Vite frontend |
| `backend` | Public: `/api` and `/api/...` | FastAPI gateway |
| `ai-cctv` | Internal | Python inference container |

The backend calls `ai-cctv` through the runtime binding **`AI_CCTV_URL`**. Do not manually set that binding variable. The browser calls the public same-origin `/api/...` endpoints.

Use the **repository root** as the Vercel Root Directory. Keep the root `vercel.json` and remove the obsolete `frontend/vercel.json` when applying the multi-service update. Remove old frontend-only project build overrides as explained in the redeployment guide.

Review the service names, public paths and binding against your intended deployment before deploying. A successful frontend build alone does not verify the Python service; check `/api/health` and an actual small-media analysis after deployment.

## Project structure

| Path | Contents |
| --- | --- |
| `frontend/` | React application, frontend tests, photographs and browser-ready twin assets |
| `backend/` | FastAPI API entrypoint, hosted gateway and backend checks |
| `ai-cctv/` | Original AI console, inference source, model weights, supplied evidence, tests and license notices |
| `digital-twin/` | Original editable Blender scene, export/render scripts and export report |
| `documentation/` | Architecture, feature inventory, UI reviews, photography credits and verification notes |
| `vercel.json` | Repository-level service definitions and public routing |

## Data, evidence and scope

**Workflow records are browser-local.** Updates synchronize between tabs on the same origin; different devices do not share records. Requests do not contact real transit staff. Use one consistent browser origin throughout a walkthrough.

**Evidence sources are distinguished.** Scripted replay represents a scenario. The supplied recorded YOLO run contains zero dwell-triggered obstruction events. Uploaded media is processed by the bundled model; a valid result can contain zero events.

**Images and videos answer different questions.** An image can report occupancy observations, but cannot establish stationary dwell. Video analysis combines vehicle position within a configured polygon with a stationary dwell threshold. Findings require human review.

**The twin preserves the original source.** The browser displays four evaluated snapshots from the Blender scene. The original `.blend` retains the full 600-frame animation and editable scene; that animation is not played continuously in the browser.

This prototype does not establish measured 5G performance, certified ramp geometry, live fleet telemetry or field-validated detection accuracy. The map and stop geometry should be interpreted in the context described in the project documentation.

## Troubleshooting

| Message | What to do |
| --- | --- |
| `Python was not found` | Install Python 3.12, reopen PowerShell and create `.venv` from the project root. |
| `Could not open requirements file` | Check your current folder. The project root must contain `backend/`. |
| `Cannot find package ... tsx` | From `frontend`, reinstall dependencies using `npm ci --include=dev`. |
| `ECONNREFUSED 127.0.0.1:8000` | The local API is unavailable. Inspect the Python startup error above the Vite messages. |
| Chunk larger than 500 kB | This is a build-size advisory. Check whether the build completed successfully; the Three.js bundle can trigger it. |
| Hosted upload fails | Review API health and service logs. Hosted uploads are limited to 3,500,000 bytes; local analysis supports up to 40 MiB. |

## Documentation

- [Setup guide](SETUP_GUIDE.md)
- [Vercel redeployment guide](VERCEL_REDEPLOY.md)
- [Service architecture and validation limits](VERCEL_SERVICES.md)
- [Test report](TEST_REPORT.md)
- [Feature inventory](documentation/FEATURE_INVENTORY.md)
- [Integration changes](documentation/CHANGES.md)
- [UI and interaction update](documentation/UPDATE_2_1.md)
- [Simple UI/UX acceptance review](documentation/SIMPLE_UX_ACCEPTANCE.md)
- [Photography additions](documentation/MORE_REAL_PHOTOS.md)
- [Photography refresh](documentation/PHOTO_REFRESH.md)
- [Visual polish notes](documentation/FINAL_POLISH.md)

## Team

| Member | Contribution | Contact |
| --- | --- | --- |
| **Chit Ko Ko** | Team leader and Blender digital twin | chitko.ko@student.aiu.edu.my |
| **Min Khant Maung** | Web prototype | minkhant.maung@student.aiu.edu.my |
| **Aung Zay Yan Phyo** | AI CCTV integration | zayyan.phyo@student.aiu.edu.my |

Research, documentation and presentation are shared team contributions.

## Attribution and licensing

Original web application: **Chit Ko Ko & Min Khant Maung**. AI CCTV application: **Aung Zay Yan Phyo**. Blender digital twin: **Chit Ko Ko**.

The AI project's **AGPL-3.0-only LICENSE and NOTICE** remain under `ai-cctv/`. Model, dependency and third-party asset licenses remain applicable. Photography credits are retained with the project. See [integration changes](documentation/CHANGES.md) for modifications to the supplied sources.
