# CONTEXT.md — NaikReady 5G | Min Khant Maung

> **Owner:** Min Khant Maung  
> **Workstream:** Interactive Web Prototype (Passenger + Driver + Transport Operator)  
> **Competition:** Cyberjaya 5G Future Talent Innovation Challenge 2026  
> **Track:** 5G Connected & Safe Last-Mile Mobility  
> **Final submission:** Friday, 30 October 2026, 11:59 PM Malaysia time (MYT)  
> **Build type:** DEMONSTRATION PROTOTYPE, **not** a production/full-stack system  
> **Document version:** 1.0 — 25 October 2026

---

## 0. PRIMARY INSTRUCTION FOR THE CODING ASSISTANT

**Read this entire document before generating code.** You are a senior React engineer, UI/UX designer, and accessibility-minded prototype builder. Build a complete, beautiful, demonstrable, responsive **NaikReady 5G** web prototype that follows this specification. Do not respond with only a development plan or pseudocode. Create the actual files, runnable app, mock datasets, interactive controls, and README. Work with the existing repository when provided; otherwise scaffold a Vite + React + TypeScript project.

**Very important:** This is a university innovation **concept demo**. Use deterministic local mock data, local state, and simulated scenarios. **Do not build or require authentication, a live database, APIs, paid services, GPS tracking, 5G hardware, production server, payments, or actual transit-operator integration.** Add a conspicuous `DEMO / SIMULATED DATA` indication wherever operational statistics, incidents, location data, network status, or vehicle arrival times appear. Every button shown as functional must do something meaningful. Maintain reasonable accessibility and polished transitions.

**Definition of success:** A judge can open a public Vercel link and, in about two minutes, demonstrate an assistance request, see it acknowledged by a driver, trigger a simulated vehicle obstruction, watch the operator respond, and record the final boarding outcome. The digital twin integration is a bonus; the prototype must work without it.

---

## 1. PROJECT IDENTITY AND PURPOSE

- **Official concept name:** NaikReady 5G
- **Product name in UI/logo:** `NaikReady 5G`
- **Tagline:** `Every Arrival. A Chance to Board.`
- **Supporting tagline:** `Smarter boarding. Safer journeys. More inclusive Cyberjaya.`
- **Problem statement:** A bus can arrive on time while passengers still cannot board because the kerb/bus bay is blocked or assistance needs were not communicated and acted upon.
- **Proposed solution:** A combined passenger assistance, boarding-area awareness, driver acknowledgement, operator escalation, and boarding-outcome verification workflow.
- **Who benefits:** Everyone using a bus stop, with specific accessibility considerations for wheelchair users, older people, low-vision passengers, parents with strollers, travellers with luggage, and anyone needing extra help.
- **Primary user story:** A wheelchair passenger requests ramp assistance. The bus-stop area is potentially blocked by a car. The driver sees a request and an advisory obstruction alert before arriving, acknowledges the request, and a dispatcher can monitor the case. Boarding succeeds or fails and the outcome is recorded.
- **Innovation positioning:** Operational integration and verifiable outcomes in a Malaysia-relevant service concept; do **not** claim that the individual underlying features are world-first.
- **5G positioning:** **Proposed** connectivity for mobile vehicles and high-bandwidth roadside sensors; this prototype simulates communications. Simple notifications could also work over 4G/Wi-Fi. **Never invent low latency numbers or claim a real 5G deployment.**

### Short copy for hero section

> **A bus arriving on time means nothing to someone who cannot board.**  
> NaikReady 5G connects passengers, drivers and transit operators so boarding needs are known, obstacles are flagged, and the actual boarding outcome is recorded.

---

## 2. BRAND & VISUAL DESIGN SYSTEM — REQUIRED

Make this look like a credible award-winning smart-mobility SaaS prototype, **not** a generic student form or stock admin panel. Take inspiration from the previously shared NaikReady reference mockups: crisp navy/teal branding, bright white surfaces, attractive mobile passenger cards, informative route visualizations, clear driver action panels, and a spacious operations command center. Avoid replicating third-party logos or real operator branding.

### Brand palette

| Design token | HEX | Use |
|---|---|---|
| `--navy-950` | `#071C36` | Main text, header/sidebar |
| `--navy-800` | `#11365A` | Section headers |
| `--blue-600` | `#1769E0` | Primary actions/links |
| `--teal-600` | `#008F96` | Brand, interactive accents |
| `--teal-400` | `#20C4BA` | Gradients and selected highlights |
| `--green-600` | `#159B72` | Completed/confirmed states |
| `--amber-500` | `#F2A633` | Pending/needs review |
| `--red-600` | `#DD4052` | Obstruction / failed boarding |
| `--background` | `#F5F8FC` | Main canvas |
| `--surface` | `#FFFFFF` | Cards and panels |
| `--border` | `#E2EAF1` | Subtle card outlines |
| `--muted` | `#62768A` | Secondary text |

**Primary gradient:** `linear-gradient(120deg, #1769E0 0%, #008F96 65%, #20C4BA 100%)`.

### Typography, iconography, components

- Font: **Inter** (fallback `system-ui, sans-serif`); strongly differentiated heading vs supporting text; no giant paragraphs.
- Icons: `lucide-react`, consistently outlined and accessible.
- Surfaces: white cards, 12–20 px corners, fine neutral borders, gentle shadow; no excessive glassmorphism.
- Buttons: strong primary blue/teal; green confirm; amber review; red only for danger/failed states.
- Layout: content-first, generous white space, responsive from 375 px phones through 1440 px desktops.
- Motion: 150–250 ms gentle transitions, pulse only for genuinely active states, honor `prefers-reduced-motion`.
- Use a clean *schematic route map* or SVG demo transit route if no trustworthy map tiles are available. **Do not imply a real live Cyberjaya bus route or GPS feed.**

### Logo specification

Generate an original simple vector logo, stored at `src/assets/naikready-logo.svg`:
- Abstract **bus-front / bus-stop marker** forming the letter `N`, with two small **wireless arcs**.
- Wordmark: **Naik** in navy, **Ready** in teal, **5G** in blue.
- Must read clearly at 32 px; also create a favicon-only icon.
- No official Cyberview, Rapid KL, or other third-party logo unless separately approved.
- Support dark and light backgrounds. Create the vector yourself or use simple SVG paths; no paid asset required.

### Responsive page design reference

- **Passenger screens:** premium phone-first layout. Sticky top brand bar; search/location header; simulated route map; bus card; prominent `Request Assistance` button; request wizard; vertical status timeline.
- **Driver screens:** landscape tablet-friendly route header with `NEXT STOP`, large priority alerts, one-tap `Acknowledge`, and `Boarded / Unable to Board` actions. Avoid requiring drivers to interact while driving; mark demo controls as for stationary/authorized use.
- **Operator screens:** left sidebar; top KPI row; large central stop-status/route overview; request queue; incident timeline; drawer for incident detail and next action.
- **Global:** visually consistent across all three roles with visible `DEMO MODE` chip.

---

## 3. RECOMMENDED TECH STACK — KEEP IT LIGHT

| Layer | Recommendation | Why |
|---|---|---|
| UI/runtime | React 18+/19 + Vite + TypeScript | Quick, fast prototype |
| Styles | Tailwind CSS | Reusable responsive styles |
| UI primitives | shadcn/ui if convenient; otherwise custom components | Quality forms, dialogs, tabs |
| Icons | Lucide React | Consistent accessible icons |
| Routing | React Router, or state-based navigation if simpler | Role pages |
| State | React Context + `useReducer` (or Zustand) | One state store for all demo workflows |
| Demo data | Local TS/JSON fixtures, optional `localStorage` | No backend |
| Simple charts | Recharts optional | Demo-only stats |
| Maps | Custom SVG schematic route preferred | No dependency on paid map API |
| 3D integration | Placeholder module + scenario/event contract | Chit owns 3D twin |
| Deployment | Vercel static site | Public judges' link |
| Code assistant | Codex / Claude Code / other | Implement from this specification |

No Supabase, paid SDK, database provisioning, OAuth, backend, or actual WebSocket is required. Don't allow setup complexity to block the finished demo.

---

## 4. REQUIRED FEATURES — EXACTLY 12 MVP FEATURE GROUPS

Implement **all 12**. They may share screens.

### Feature 01 — Role-based demo launcher

Landing/home `Try Demo` with three role cards: `Passenger`, `Bus Driver`, `Transport Operator`; switch roles freely via nav. No login. Include `Guided Demo` and `Reset Demo` actions.

### Feature 02 — Passenger stop/route selection

Use two demo stops `CYB-DEMO-01 — Cyberjaya City Centre` and `CYB-DEMO-02 — MMU Area`. Use route `DEMO-R01 — Cyberjaya Demo Shuttle`. Show fake bus ETA with explicit `Simulated ETA` label. The route is illustrative, not a published transit service.

### Feature 03 — Inclusive assistance request form

Choose an assistance type: `Wheelchair / Ramp`, `Extra Boarding Time`, `Low-Vision Guidance`, `Stroller`, `Luggage`, `Other Assistance`. Request need not imply disability disclosure. Optional note limited to 140 characters. Submit with user feedback and unique local ID.

### Feature 04 — Passenger request-status timeline

State progression `REQUESTED → DRIVER_ACKNOWLEDGED → BOARDING_ATTEMPT → COMPLETED` or `UNABLE_TO_BOARD`. Timeline updates from simulated driver actions. Clear next-step guidance, error state, and option to cancel pending request.

### Feature 05 — Driver route/next-stop overview

Show active demo route, next-stop, sample passenger assistance queue, and status. Distinguish requests from sensor warnings. Include big buttons for accessibility and tablet usability.

### Feature 06 — Driver acknowledges passenger request

Press `Acknowledge Request` → changes request status across passenger and operator views using shared local state. The UI must show acknowledgment, not pretend physical assistance has already occurred.

### Feature 07 — Driver receives obstruction warnings

Respond to `OBSTRUCTION_DETECTED` in demo state; show potential blocking vehicle, relevant stop, reason, video/image evidence placeholder, and `Review / Acknowledge` buttons. Warning should say **`Potential boarding-area obstruction — verify on arrival`**, not “Safe/Unsafe to board” certification.

### Feature 08 — Driver records final boarding outcome

Buttons: `Boarding Completed` and `Unable to Board`. For unsuccessful case choose reason such as `Blocked Boarding Zone`, `Ramp Not Available`, `Could Not Provide Assistance`, `Other / Unknown`. These choices create a case record and visible status change.

### Feature 09 — Operator live overview

Dashboard KPIs from **local mock data only**: pending requests, acknowledged, potential obstructions, completed and unresolved. Add `DEMO DATA — NOT LIVE STATISTICS` near KPI row.

### Feature 10 — Operator request/incident queue

View filtered queue by `Pending`, `Acknowledged`, `Needs Review`, `Resolved`; open case detail, mark an operator-reviewed response, and annotate demo outcome. No real dispatcher powers are claimed.

### Feature 11 — Scenario control center

An obvious demo control with preset scenarios: `Normal`, `Car Blocking`, `Motorcycle Blocking`, `Assistance Requested`, `Assistance Acknowledged`, `Boarding Completed`, and `Unable to Board`. Each must lead to coherent UI state across roles. Provide one `Run Guided Demo` flow and `Reset All`.

### Feature 12 — Integration-ready 3D / CCTV panel

Create `Digital Twin` and `Vision AI` cards or tabs with graceful fallback placeholder: a schematic/illustration and scenario labels even before external components exist. If Chit's exported React 3D widget is ready, embed it; if not, web prototype must remain fully functional. Support a **local JSON event import** from Aung so his AI demo can drive an obstruction alert without requiring a real API.

---

## 5. EXPECTED SCREENS & NAVIGATION — 8 VIEWS

1. **Welcome / Role Selector** (`/`) — identity, impact hook, cards, Start Demo.
2. **Passenger Home** (`/passenger`) — selected bus stop, illustrative route map, mock ETA, assistance CTA.
3. **Assistance Request** (`/passenger/request`) — accessible assist-type selection + optional note + submit.
4. **Passenger Status** (`/passenger/status`) — request timeline and final outcome.
5. **Driver Dashboard** (`/driver`) — upcoming stop, requests, hazards, acknowledgements, outcome controls.
6. **Operator Command Center** (`/operator`) — KPI cards, stop overview, case queue, incident details.
7. **Digital Twin / Vision AI Demo** (`/experience`) — 3D placeholder integration, CCTV scenario card, role-linked states.
8. **Scenario Lab** (`/demo`) — one-click simulation fixtures, guided walkthrough, reset, JSON import.

If speed is a concern, combine adjacent views in tabs/sections; preserve all required user workflows.

---

## 6. DEMO SCENARIOS AND EXACT BEHAVIOR

| Scenario ID | Trigger | Passenger | Driver | Operator | 3D / AI |
|---|---|---|---|---|---|
| `NORMAL` | Reset and select clear | No pending problems | Stop available (not safety-certified) | Normal demo state | Clear stop |
| `CAR_BLOCKING` | Demo button or JSON import | General service advisory | Potential obstruction alert | Open potential incident | Red outline around car |
| `MOTORCYCLE_BLOCKING` | Demo button or JSON import | General service advisory | Potential obstruction alert | Open potential incident | Amber/red outline around motorcycle |
| `ASSISTANCE` | Submit passenger request | `Request sent` | One request pending | New assistance case | Assistance marker |
| `ACKNOWLEDGED` | Driver taps acknowledge | `Driver notified / acknowledged` | Acknowledged | Case advances | Signal indicator |
| `BOARDING_COMPLETED` | Driver confirms | `Boarding confirmed` | Completed | Closed record | Bus/ramp animation if available |
| `BOARDING_FAILED` | Driver selects reason | `Could not board — operator review` | Failed attempt noted | Unresolved case | Barrier remains |

**In a complete guided walkthrough:** select `CAR_BLOCKING` → submit wheelchair assistance → driver acknowledges → driver attempts resolution → record successful boarding (after simulated obstruction clears) OR unable to board → operator reviews. Don't automatically mark boarding successful merely because the warning vanished.

---

## 7. SHARED EVENT CONTRACT — CRITICAL FOR ALL 3 TEAM MEMBERS

Chit owns interactive 3D; Aung owns recorded-video AI detection. Min owns the **demo state semantics** and optional event import. Use these exact event types:

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

### Example event payload

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

Values above are **illustrative**, not real measured outputs. `source_mode` choices:
- `recorded_video_model_inference` — actual model inference from a recorded/demo video;
- `manual_simulation` — pre-scripted event from demo controls.

Store driver/passenger request state separately from sensor events; for instance, a detected parked car is **not itself** evidence that a wheelchair passenger requested help.

For loose integration without a backend, provide `Import AI Event JSON` button or file input that validates this structure and updates state. For 3D, export/apply a callback such as `onScenarioChange(scenarioId)`; when Chit's component is available, mount it on `/experience`.

---

## 8. RECOMMENDED APP STRUCTURE

```text
naikready-web-demo/
├── public/
│   └── demo-assets/
├── src/
│   ├── assets/naikready-logo.svg
│   ├── app/App.tsx
│   ├── app/demoReducer.ts
│   ├── app/demoData.ts
│   ├── components/BrandHeader.tsx
│   ├── components/StatusBadge.tsx
│   ├── components/RouteMapDemo.tsx
│   ├── components/IncidentCard.tsx
│   ├── components/Timeline.tsx
│   ├── components/DigitalTwinPlaceholder.tsx
│   ├── pages/Welcome.tsx
│   ├── pages/PassengerHome.tsx
│   ├── pages/RequestAssistance.tsx
│   ├── pages/PassengerStatus.tsx
│   ├── pages/DriverDashboard.tsx
│   ├── pages/OperatorDashboard.tsx
│   ├── pages/Experience.tsx
│   ├── pages/ScenarioLab.tsx
│   ├── styles/globals.css
│   └── main.tsx
├── package.json
├── README.md
└── CONTEXT.md
```

Adapt the exact structure to project conventions, but keep components and state cleanly separated.

---

## 9. QUALITY, ACCURACY, ETHICS

- The output is a **conceptual proof-of-workflow**, not an operational transit service.
- No real passenger records or identifiers, real tracking or actual operator authority.
- No invented service reliability figures, passenger counts, boarding success improvements or actual 5G test results. KPI numbers must be clearly **simulated**.
- Treat all AI/camera input as `potential obstruction`; a clear zone does not prove the overall stop is safe/accessibility-compliant.
- Avoid discriminatory classification or inferring disability from video; assistance is voluntary.
- Accessibility: keyboard navigation, semantic form labels, minimum contrast, clear errors, large tap targets, alternative text, no color-only status, focus visibility, `prefers-reduced-motion`.
- Avoid fragile copyrighted photography/logos. Use custom vector visuals or permitted assets.
- Consider graceful handling for unsupported devices, empty queue, cancelled request, and missing twin/AI demo.

---

## 10. ACCEPTANCE CHECKLIST — MUST PASS

- [ ] `npm install && npm run dev` starts without errors.
- [ ] Brand logo, palette, clean typography and responsive layout are consistent.
- [ ] All **12 features** have demonstrable interactions.
- [ ] Passenger can submit a request and see it in Driver and Operator views.
- [ ] Driver acknowledgement changes passenger status correctly.
- [ ] Driver can record successful / unsuccessful boarding; operator sees correct outcome.
- [ ] Demo controls can trigger both car and motorcycle obstruction warnings.
- [ ] JSON import can consume Aung's example event without a backend.
- [ ] 3D area has coherent placeholder; app works if twin not connected.
- [ ] Reset restarts the guided demo deterministically.
- [ ] No dead buttons, missing links, persistent TypeScript errors, or horizontal scrolling on phone.
- [ ] All fake data clearly labelled `DEMO`, `SIMULATED`, or `ILLUSTRATIVE`.
- [ ] `npm run build` succeeds; deployment works on Vercel.
- [ ] README explains installation, demo workflow, limitation, and event import.

### Test cases to demonstrate

1. Request wheelchair help → driver acknowledgement → boarding completed.
2. Recorded-video car obstruction event imported → driver warning and operator incident.
3. Motorbike obstruction scenario → potential blockage, not automatic boarding failure.
4. Failed boarding → reason selection → operator review remains open.
5. Reset → initial clear scenario with clean timeline.

---

## 11. DAY-BY-DAY DELIVERY TARGETS

| Date | Target |
|---|---|
| **25 Oct** | Scaffold Vite app; brand system; Welcome, Passenger, Driver, Operator shell. |
| **26 Oct** | Implement request → acknowledgement → outcome flow; state reducer; scenario data. |
| **27 Oct** | Finalize operator case management and scenario lab; add JSON import contract. |
| **28 Oct** | Polish responsive UI; coordinate with Aung and Chit; integrate available assets. |
| **29 Oct** | Test end-to-end, record screen walkthrough, deploy final Vercel link. |
| **30 Oct** | Submission verification only; no major new features. |

**Prefer completing a coherent five-minute live demonstration over speculative additional features.**

---

## 12. FINAL HANDOFF FILES

1. Source repository / source ZIP.
2. Public, tested **Vercel URL**.
3. `README.md` with `npm install`, `npm run dev`, `npm run build`, demo navigation and limitations.
4. At least 6 polished screenshots (passenger, request, status, driver, operator, scenarios).
5. 60–90-second screen recording if available.
6. `sample-obstruction-event.json` and short event contract for Aung/Chit.
7. A 3–5 sentence technical description for the official submission slides.

---

## 13. FINAL EXECUTION REQUEST TO AI CODING ASSISTANT

> Implement **NaikReady 5G** exactly as described in this CONTEXT.md. This is a demo-only, static Vite + React + TypeScript prototype. Build all 12 required functional features with exceptional professional UI, accessible interaction, stable local shared state, realistic but explicitly simulated sample cases, an event JSON importer, a 3D placeholder/integration point, and a deployable README. Avoid full-stack infrastructure. Prioritize an attractive, working judge walkthrough over speculative scope. Create all project files and verify the build if your environment allows it.
