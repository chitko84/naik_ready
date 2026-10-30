# NaikReady 5G — Cyberjaya Interactive Mobility Prototype

**Every Arrival. A Chance to Board.**

A self-contained **concept demonstration** of accessible transit boarding: Passenger requests → Driver acknowledgment → Boarding attempt/outcome → Operator monitoring and review. Built for the **Cyberjaya 5G Future Talent Innovation Challenge 2026** (5G Connected & Safe Last-Mile Mobility).

**This is not a real transit service.** All routing, ETA, locations, status, statistics, and obstruction data are simulated or illustrative. It has no backend, authentication, GPS, live CCTV, passenger identity collection, or real 5G measurement.

## Start locally

Requirements: **Node.js 18+** and npm (Internet connection required for the first dependency install).

```bash
npm install
npm run dev
```

Open the Vite URL printed in the terminal (typically `http://localhost:5173`).

```bash
npm run build
npm run preview
```

The build uses `tsc -b && vite build` and outputs to `dist/`.

## App routes

| Route | Page |
|---|---|
| `/` | Premium welcome/role chooser |
| `/passenger` | Select a simulated demo stop/route |
| `/passenger/request` | Accessible assistance request form |
| `/passenger/status` | Connected passenger timeline |
| `/driver` | Driver route, advisory, and boarding workflow |
| `/operator` | Operator command center, queue, maps, reviews and reports |
| `/experience` | Digital Twin visualization and Vision AI awareness view |
| `/demo` | Seven illustrated scenarios, guided journeys, scene status, optional AI JSON import, shared log |

Use the top navigation to switch roles without signing in. The Scenario Lab includes visual scenario cards, a current-scene status overview, an eight-moment guided journey and an optional recorded-AI-event import.

## Fastest competition demonstration (about 2–3 minutes)

1. Open **Scenario Lab** and start **Successful boarding** Guided Demonstration. It resets to a consistent initial state.
2. Activate moment 1: **Car Blocking** advisory. Inspect `/experience`.
3. Activate moment 2: Create a **Wheelchair / Ramp** request. Open `/passenger/status`.
4. At moment 3, view the incoming request and obstruction on `/driver` (navigation-only step).
5. Activate moment 4: Driver acknowledgment updates Passenger + Operator views.
6. At moment 5, open `/operator` to inspect the queue and potential obstruction.
7. Apply step 6: For **successful boarding**, the obstruction is cleared in the demonstration; for **unsuccessful boarding**, it remains active. Neither state certifies real-world safety.
8. Activate moment 7: A boarding attempt and selected outcome are recorded.
9. Activate moment 8: Operator review is logged.

Alternatively, do the same operations manually: Passenger Request → Driver Acknowledge → Begin Boarding Attempt → Boarding Completed/Unable to Board → Operator review.

For a failure walkthrough choose **Unsuccessful boarding** before starting the guided demonstration.

## Scenario Lab

The seven illustrated scenes are interactive. The Current Scene panel summarizes alerts and requests, and the guided demonstration presents action-by-action controls. The recorded-video JSON importer is available under **Recorded AI event import → Show details**.

Seven presets: NORMAL, CAR_BLOCKING, MOTORCYCLE_BLOCKING, ASSISTANCE, ACKNOWLEDGED, BOARDING_COMPLETED, BOARDING_FAILED. Presets that need a request create a demonstration request when necessary. **Reset All** clears state after confirmation. Normal clears active obstruction advisories but preserves existing demo requests—use Reset All for a clean slate.

State lives in a single `DemoProvider` (React Context + `useReducer`) and is persisted in `localStorage` under `naikready-demo-v1`. Role switching updates all views in the **same browser**; this is **not** multiuser cross-device synchronization.

### State transition invariants

```text
REQUESTED → DRIVER_ACKNOWLEDGED → BOARDING_ATTEMPT → COMPLETED
                                                ↳ UNABLE_TO_BOARD
REQUESTED → CANCELLED
```

- Sensor advisories and passenger assistance requests are independent objects.
- A potential obstruction is **not** a real-world safety determination.
- Clearing an obstruction does **not** imply a successful boarding.
- Acknowledging an assistance request does **not** imply completed boarding.
- Failed boardings preserve their failure reason even after operator review.
- Operator KPIs and charts derive from shared local records rather than made-up real-world performance percentages.

## Recorded-video Vision AI event import

1. Open `/demo` → **Recorded AI event import** → **Show details** → **Choose event JSON**.
2. Select `public/demo-assets/sample-obstruction-event.json`.
3. The importer validates `schema_version`, event ID/type, route/stop ID, timestamp, source mode, prototype flags, detected object class, and numeric confidence/zone bounds.
4. A valid **OBSTRUCTION_DETECTED** event creates a potential obstruction advisory across Driver, Operator, Digital Twin and Scenario Lab.
5. A valid **OBSTRUCTION_CLEARED** event clears a matching stop's active advisory. Re-importing the same event ID is rejected.

Accepted event types in importer: `OBSTRUCTION_DETECTED`, `OBSTRUCTION_CLEARED`. Other shared workflow event types are generated via UI actions (ASSISTANCE_REQUESTED, DRIVER_ACKNOWLEDGED, BOARDING_COMPLETED, BOARDING_FAILED, OPERATOR_REVIEWED, DEMO_RESET).

`recorded_video_model_inference` describes an external input source. The web prototype does not run an AI model. Manually generated fixtures use `manual_simulation`.

The 3D adapter in `src/integrations/digitalTwinAdapter.ts` exports `getDigitalTwinSnapshot` and `OnScenarioChange` interfaces for the team's later component integration. The current self-contained Digital Twin is an original SVG schematic.

## Deployment to Vercel

1. Push this folder to a Git repository.
2. Import the repository into Vercel as a **Vite** project.
3. Build command: `npm run build`.
4. Output directory: `dist`.
5. No environment variables are required.
6. `vercel.json` rewrites deep links to `index.html`.
7. Test all eight routes after deploying. Ensure you do not describe the route simulation as a live bus feed.

## Important constraints and limitations

- The illustrative route **DEMO-R01** has only two demonstration stops: CYB-DEMO-01 (Cyberjaya City Centre) and CYB-DEMO-02 (MMU Area). It is not an actual transit route.
- All ETAs and timings are illustrative.
- A clear warning state means **no active simulated alert**, not verified physical safety.
- No backend, production database, server-to-server events, real passenger identities, real video or 5G hardware are connected.
- The sample event's confidence is sample metadata, not an independently measured performance claim.
- A future 3D widget and externally processed video data can be integrated, but the prototype works without them.

## Reference material

Three supplied images are saved in `design-reference/` for continuity. The app uses **native responsive UI** and **custom SVG illustrations**, not the images as backgrounds. `CONTEXT.md` is the initial project brief; `MASTER_PROMPT.md` contains the detailed development instructions.

## Competition presentation description

NaikReady 5G is a proposed smart-mobility system connecting passenger assistance requests with driver acknowledgments, boarding-area obstruction advisories, and verified boarding outcomes. In the demonstration, a wheelchair user can ask for ramp support before arrival while a recorded-video or simulated advisory flags a potential boarding-zone obstruction. The driver can review and acknowledge the request, explicitly record whether the passenger boarded, and make the outcome visible to the operator. The prototype uses shared local state and a standard JSON event contract to demonstrate the workflow without claiming a deployed 5G or live transport system.
