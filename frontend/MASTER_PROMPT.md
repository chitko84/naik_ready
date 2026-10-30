# NAiKREADY 5G — FINAL MASTER DEVELOPMENT PROMPT

## ROLE & PRIMARY OBJECTIVE

Act as a **Senior Full-Stack React Engineer, Lead UI/UX Designer, Accessibility Specialist, and Smart Mobility Prototype Architect**.

Build a complete, fully functional, visually exceptional, responsive web demonstration prototype named **NaikReady 5G** for the **Cyberjaya 5G Future Talent Innovation Challenge 2026**.

**Competition Track:** 5G Connected & Safe Last-Mile Mobility

**Submission Deadline:** 30 October 2026, 11:59 PM Malaysia Time.

This is a **university innovation demonstration prototype**, not a production transport-management platform.

Your responsibility is to create a polished, professional, interactive web application that demonstrates how passengers, bus drivers, and transport operators can work together to improve accessible public transport boarding.

**Do not only produce a proposal, pseudocode, Figma design, mockup image, or partial frontend. Implement the actual application, including every required page, working interaction, shared state system, mock dataset, validation logic, reusable component, integration placeholder, and deployment configuration.**

The result must be runnable locally and ready for deployment to Vercel.

---

# 1. PROJECT IDENTITY

**Product name:** NaikReady 5G

**Official tagline:**

Every Arrival. A Chance to Board.

**Supporting tagline:**

Smarter boarding. Safer journeys. More inclusive Cyberjaya.

**Additional brand messaging:**

Smart Assistance. Inclusive Journeys. A More Connected Cyberjaya.

People. Mobility. Opportunity. Together.

## The Problem

A bus arriving on time does not guarantee that every passenger can board it.

Wheelchair users, older passengers, people with low vision, parents with strollers, and people carrying luggage may encounter difficulties because:

- Boarding zones are obstructed.
- Drivers are unaware of assistance requirements.
- Communication happens too late.
- Passengers are unable to communicate their needs beforehand.
- Transport operators cannot easily follow up on boarding failures.
- Conventional tracking systems focus on vehicle arrivals rather than whether passengers boarded successfully.

## Proposed Solution

NaikReady 5G is an integrated smart-mobility concept connecting three main stakeholders:

1. **Passengers** request assistance and monitor progress.
2. **Bus Drivers** receive assistance requests, review potential boarding obstructions, and confirm actual boarding outcomes.
3. **Transport Operators** monitor requests and incidents, review problems, and track outcomes.

It also demonstrates how a proposed 5G-connected environment could support timely vehicle, passenger, and roadside-system communication.

The prototype must clearly distinguish simulated connectivity from actual deployment. Do not claim real 5G measurements, real-time field integration, or production accuracy.

## Central Innovation

The most important concept is:

**NaikReady 5G does not stop at knowing when a bus arrives. It closes the loop by checking whether the passenger was actually able to board.**

Every major feature must contribute to demonstrating this distinction.

---

# 2. VISUAL DESIGN — FOLLOW THE THREE PROVIDED REFERENCES

The three reference images define the intended design quality and visual direction.

They are visual inspiration, not screenshots to copy as non-interactive backgrounds.

Recreate their overall aesthetic with genuine responsive React components.

## Reference A — Transport Operator Dashboard

A premium desktop operations command center featuring:

- Large spacious dashboard.
- Left navigation sidebar.
- NaikReady 5G branding.
- Header with dashboard title, notifications, and role indicator.
- Top row of performance metrics.
- Large illustrative route-monitoring map.
- Colored stop markers and transport indicators.
- Assistance request queue.
- Bus-stop conditions.
- Incident timeline.
- Selected incident details.
- Boarding outcomes visualization.
- Clean status pills.
- Professional dashboard cards.

The design should resemble a modern smart-city command center rather than a generic administrative template.

## Reference B — Passenger Mobile Application

A premium mobile-first interface featuring:

- Clean white backgrounds.
- Blue and teal branding.
- Large accessible typography.
- Destination or stop selector.
- Interactive schematic route map.
- Bus arrival information.
- Prominent assistance CTA.
- Assistance selection cards with descriptive icons.
- Selected-stop summary.
- Optional notes.
- Request submission button.
- Vertical assistance-status timeline.
- Clear confirmation and progress messages.

Maintain the same clean, premium, accessible visual language.

## Reference C — Driver Dashboard

A landscape tablet-oriented transport interface featuring:

- Large current-route display.
- Route progress.
- Next bus stop.
- Estimated arrival.
- High-priority assistance alerts.
- Potential boarding-area obstruction warnings.
- Large passenger-status cards.
- Boarding-area review controls.
- Clear successful or unsuccessful boarding buttons.
- A responsive mobile driver alert interface.

The driver experience should prioritize rapid understanding, minimal cognitive effort, and large touch targets.

**Important:** Driver interaction controls are intended only while the vehicle is stationary or for authorized demonstration use. They are not intended to encourage interaction while driving.

## Design Quality Target

The application should feel like a finished innovation competition finalist prototype, with the visual sophistication of modern professional SaaS software.

Avoid:

- Default browser styling.
- Generic AI-generated landing pages.
- Oversized gradients everywhere.
- Excessive glass effects.
- Unnecessary decorative blobs.
- Unreadably small text.
- Crowded cards.
- Inconsistent spacing.
- Dummy nonfunctional buttons.
- Repeated generic layouts for every role.
- Fake realtime indicators without demo labels.
- Layouts that only work at one screen size.

Use subtle animations, carefully controlled visual hierarchy, crisp icons, and intentional whitespace.

---

# 3. BRAND DESIGN SYSTEM

Use the following exact colors as CSS variables or Tailwind theme tokens.

| Token | Hex | Usage |
|---|---|---|
| Navy 950 | #071C36 | Primary text and dark areas |
| Navy 800 | #11365A | Secondary headings |
| Blue 600 | #1769E0 | Primary actions |
| Teal 600 | #008F96 | Brand identity and accents |
| Teal 400 | #20C4BA | Gradient highlights |
| Green 600 | #159B72 | Confirmed and completed |
| Amber 500 | #F2A633 | Warning and pending review |
| Red 600 | #DD4052 | Potential obstruction and failure |
| Background | #F5F8FC | Main application canvas |
| White | #FFFFFF | Card surfaces |
| Border | #E2EAF1 | Dividers and subtle outlines |
| Muted | #62768A | Supporting information |

**Primary gradient:**

`linear-gradient(120deg, #1769E0 0%, #008F96 65%, #20C4BA 100%)`

## Typography

Primary font: Inter.

Fallback: system-ui, sans-serif.

Use clear heading hierarchy, readable supporting text, and consistent numerical formatting.

## Components

- Rounded cards with 12–20px corners.
- Subtle shadows.
- Fine card borders.
- Smooth button hover and pressed states.
- Clear keyboard focus rings.
- Accessible input controls.
- Modern status badges.
- Small tooltips where useful.
- Subtle animated timelines.
- Proper loading and empty states.
- Toast notifications for completed actions.
- Modal dialogs and drawers when appropriate.

Use Lucide React for icons.

Animations should generally be 150–250ms and respect reduced-motion settings.

## Original Logo

Create a vector SVG logo at:

`src/assets/naikready-logo.svg`

The design should feature:

- An abstract letter N integrating a bus-front or bus-stop marker.
- Two small wireless connectivity arcs.
- "Naik" in navy.
- "Ready" in teal.
- "5G" in blue.

Create an icon-only favicon variant.

Ensure the logo remains readable on mobile and works on light and dark backgrounds.

Do not copy official third-party transport branding.

---

# 4. TECHNICAL ARCHITECTURE

Use a lightweight, reliable modern frontend stack.

**Required:**

- React 18+ or 19.
- Vite.
- TypeScript.
- Tailwind CSS.
- React Router.
- Lucide React.
- React Context with useReducer, or Zustand.
- Local TypeScript/JSON demonstration data.
- Optional localStorage persistence.
- Custom SVG route visualization.
- Reusable accessible components.

**Optional:**

- shadcn/ui for high-quality accessible UI primitives.
- Recharts for simple operator statistics.
- Framer Motion or Motion for subtle interactions, only if it does not complicate the build.
- Lightweight validation utilities.

Do not introduce unnecessary dependencies.

## Strict Architecture Constraints

Do not require:

- User registration.
- Authentication.
- Backend servers.
- Supabase or Firebase.
- Production APIs.
- Paid map services.
- Real GPS permissions.
- WebSocket servers.
- Real CCTV connections.
- Live transport authority data.
- Real 5G hardware.
- Payment processing.

The demonstration must work entirely from local simulated data.

The application should function after:

`npm install`

`npm run dev`

And build successfully using:

`npm run build`

Prepare Vercel deployment with correct single-page-app routing.

---

# 5. WEBSITE STRUCTURE — EIGHT REQUIRED VIEWS

Build the following routes:

| Route | View |
|---|---|
| `/` | Welcome / Role Selector |
| `/passenger` | Passenger Home |
| `/passenger/request` | Assistance Request |
| `/passenger/status` | Assistance Status |
| `/driver` | Driver Dashboard |
| `/operator` | Operator Command Center |
| `/experience` | Digital Twin / Vision AI |
| `/demo` | Scenario Lab |

All eight views must be implemented, linked, and visually polished.

Use consistent navigation, but adapt navigation patterns to the needs of each user role.

---

# 6. VIEW 01 — WELCOME / ROLE SELECTOR

Create an impressive professional landing page.

## Hero Area

Use the NaikReady 5G logo prominently.

Main headline:

**Every Arrival. A Chance to Board.**

Subheading:

**A bus arriving on time means nothing to someone who cannot board.**

Description:

NaikReady 5G connects passengers, drivers, and transport operators so accessibility needs are communicated, potential obstacles are identified, and boarding outcomes are recorded.

Include primary buttons:

- Try Interactive Demo.
- Run Guided Demo.

Both must work.

## Hero Visualization

Create an original responsive UI composition illustrating the three connected systems.

Suggested structure:

- Central smart bus / mobility graphic.
- Passenger request preview card.
- Driver alert preview card.
- Operator monitoring preview card.
- Animated but subtle connecting lines.

Do not make this a static screenshot of the references.

## Role Selection

Create three large cards:

### Passenger

Icon: Accessible person / mobility.

Description:

Find your bus, request boarding assistance, and follow your request progress.

Action: Open Passenger Experience.

### Bus Driver

Icon: Bus.

Description:

View assistance requests, review possible obstructions, and record boarding outcomes.

Action: Open Driver Dashboard.

### Transport Operator

Icon: Monitor / command center.

Description:

Track assistance requests, review incidents, and monitor boarding outcomes.

Action: Open Operator Dashboard.

## Additional Sections

Briefly explain the three-stage system:

1. Request assistance.
2. Driver and operator coordination.
3. Confirm boarding outcome.

Include a section illustrating the problem of an on-time bus with an inaccessible boarding area.

Finish with a polished footer including the competition name, product branding, and a conspicuous demo disclaimer.

---

# 7. VIEW 02 — PASSENGER HOME

Route: `/passenger`

Mobile-first, but fully responsive on desktop.

## Header

Include:

- Brand logo.
- Passenger experience title.
- Notification button.
- Demo Mode indicator.
- Navigation to other demo roles.

## Stop Selection

Use these exact demo locations:

- `CYB-DEMO-01` — Cyberjaya City Centre.
- `CYB-DEMO-02` — MMU Area.

Use one illustrative demo route:

- `DEMO-R01` — Cyberjaya Demo Shuttle.

These are fictional demonstration route identifiers. Do not label them as actual published bus services.

## Route Map

Create an attractive custom SVG schematic map visually inspired by the passenger mockup.

It should contain:

- Soft map background.
- Illustrative route path.
- Two selectable demonstration stops.
- Bus icon.
- Selected stop indicator.
- Route information panel.
- Approximate vehicle progress for the simulation.
- Zoom or view controls only if functional.
- A visible "Illustrative Route" label.

The map is not a real live GPS map.

## Bus Information Card

Display:

- Demo route identifier.
- Route name.
- Selected stop.
- Simulated arrival estimate.
- Status information.
- Assistance availability.

Example:

**Next Demo Bus Arriving**

6 min

*Simulated ETA — not live transport information.*

Provide meaningful interactions for choosing the stop and viewing route details.

## Primary CTA

Large teal-gradient button:

**Request Assistance**

Clicking this opens `/passenger/request`.

## Assistance Summary

If a passenger already has an active request, display a compact card showing its status and linking to the status page.

If there is no request, show a clean informational empty state.

## Obstruction Advisory

If a simulated obstruction affects the selected stop, show a general service advisory.

Do not reveal personal assistance information to unrelated passengers.

Do not claim that a detected obstruction proves boarding is impossible.

---

# 8. VIEW 03 — PASSENGER ASSISTANCE REQUEST

Route: `/passenger/request`

Match the second reference image's middle mobile screen.

## Page Heading

**Request Assistance**

Supporting text:

Let us know how we can assist you. Your selected bus driver will receive a demonstration notification.

## Assistance Types

Use six selectable cards:

1. Wheelchair / Ramp.
2. Extra Boarding Time.
3. Low-Vision Guidance.
4. Stroller.
5. Luggage.
6. Other Assistance.

Each card should include:

- Distinct accessible Lucide icon.
- Short title.
- Simple description.
- Clear selected-state border and checkmark.
- A large touch target.

Only one primary type needs to be selected per request.

Do not ask users to disclose medical conditions or prove disability.

## Selected Bus Stop

Show the currently selected stop.

Allow changing it.

Display the demo route identifier.

## Additional Notes

Optional textarea.

Maximum: 140 characters.

Display a live character counter.

Prevent exceeding the limit.

## Submit Button

Prominent blue/teal-gradient action:

**Submit Request**

On click:

- Validate assistance type and selected stop.
- Generate a unique local request ID.
- Store the request in the shared application state.
- Set its status to `REQUESTED`.
- Add an event to the demo activity log.
- Make the request immediately visible in the Driver Dashboard.
- Make the request immediately visible in the Operator Command Center.
- Display successful submission feedback.
- Navigate to `/passenger/status`.

Never show submission success without updating shared state.

---

# 9. VIEW 04 — PASSENGER ASSISTANCE STATUS

Route: `/passenger/status`

Design this as a polished premium mobile status experience.

## Top Summary

Show:

- Request identifier.
- Selected stop.
- Assistance type.
- Demo route.
- Current status.
- Simulated arrival estimate where appropriate.

## Vertical Timeline

Supported states:

1. `REQUESTED`
2. `DRIVER_ACKNOWLEDGED`
3. `BOARDING_ATTEMPT`
4. `COMPLETED` or `UNABLE_TO_BOARD`

Also support `CANCELLED` while cancellation is permitted.

Use:

- Green completed circles.
- Blue active circles.
- Grey pending circles.
- Amber review indicators.
- Red failure indicators.

Each stage needs human-readable wording and an explanatory message.

Example:

**Request Sent**

Your assistance request has been submitted.

**Driver Acknowledged**

The driver has acknowledged your request.

**Boarding in Progress**

The driver has begun the boarding-assistance process.

**Boarding Completed**

Your boarding was confirmed in the demonstration.

For unsuccessful boarding:

**Unable to Board**

The boarding attempt could not be completed. The case requires operator review.

## Critical State Behavior

When the driver acknowledges a request in the Driver Dashboard, this timeline must update from the same shared state.

When the driver confirms the boarding outcome, the passenger view must show the matching result.

An acknowledgment is not the same thing as a completed boarding.

An obstruction being cleared must never automatically imply successful boarding.

## Additional Controls

Allow pending requests to be cancelled.

Show confirmation before cancelling.

For completed, failed, or cancelled requests, show an appropriate final state and a way to begin a new request.

Provide a useful empty state when no request exists.

---

# 10. VIEW 05 — BUS DRIVER DASHBOARD

Route: `/driver`

This must be one of the most impressive and usable screens.

Use the third reference image as the main visual inspiration.

Prioritize landscape tablet layouts while also creating an excellent mobile view.

## Dashboard Header

Include:

- NaikReady 5G logo.
- Driver Dashboard.
- Demo bus identifier.
- Route name.
- Current demo status.
- Stationary-use safety reminder.
- Demo Mode badge.

## Main Layout

On larger screens:

**Left area:** Route and stop progress.

**Right area:** Alerts, assistance actions, boarding checks, outcomes.

On mobile, stack these panels in clear priority order.

## Route Panel

Display:

- Active demo route.
- Current/next stop.
- Simulated ETA.
- Illustrative schematic map.
- Route progress timeline.
- Demo stop selection.
- Pending assistance count.

Stop names must remain consistent with the passenger experience.

## Accessibility Request Cards

When a passenger submits a request, display:

- Request ID.
- Stop.
- Assistance type.
- Optional note.
- Request status.
- Simulated timestamp.
- Large acknowledgment button.

Example:

**HIGH PRIORITY — Assistance Requested**

Wheelchair / Ramp

Cyberjaya City Centre

A passenger requires boarding assistance.

Button:

**Acknowledge Request**

Click behavior:

- Find the correct request.
- Apply `DRIVER_ACKNOWLEDGED`.
- Update the Driver Dashboard.
- Update the Passenger Status page.
- Update the Operator queue.
- Record the event in the activity log.

The button should then visibly change to acknowledged status.

## Potential Boarding Obstruction Alert

Create a prominent alert panel.

Example title:

**Potential boarding-area obstruction — verify on arrival**

Possible obstacle:

- Car.
- Motorcycle.

Show:

- Relevant demonstration stop.
- Potential obstruction category.
- Source: manual simulation or recorded-video demo.
- Detection time.
- Evidence placeholder.
- Operator review state.

Possible controls:

- Review Alert.
- Acknowledge Warning.
- View Demo Evidence.

These must work.

**Critical:** A sensor or vision-model warning is only a potential obstruction advisory, not a safety certification.

Do not automatically mark passengers unable to board because an alert exists.

## Boarding Area Check

Create a dedicated card.

Driver can indicate that an on-arrival check has been performed.

Provide a meaningful `Begin Boarding Attempt` action where appropriate.

This should move a valid acknowledged request to `BOARDING_ATTEMPT`.

## Boarding Outcome

Two large action buttons:

**Boarding Completed** — green.

**Unable to Board** — red outline or red action.

### Successful Boarding

When selected:

- Confirm the correct request.
- Require an appropriate boarding-attempt state.
- Mark the request `COMPLETED`.
- Add a boarding outcome record.
- Update passenger status.
- Update operator records.
- Update simulated metrics.

### Unable to Board

Open a modal requesting a reason.

Options:

- Blocked Boarding Zone.
- Ramp Not Available.
- Could Not Provide Assistance.
- Other / Unknown.

On confirmation:

- Mark request `UNABLE_TO_BOARD`.
- Preserve failure reason.
- Create or update the unresolved operator case.
- Update passenger status.
- Update driver records.
- Update operator metrics.
- Add an event to the log.

No boarding-success claims should be made until a final driver outcome is actually recorded.

## Mobile Driver Alert View

Implement a compact mobile-friendly alert inbox similar to the third reference image.

Show stacked alert cards with:

- Red: high-priority assistance or serious issue.
- Amber: potential obstruction.
- Blue: informational.
- Green: completed.

Each card should open the relevant driver action or detail view.

---

# 11. VIEW 06 — TRANSPORT OPERATOR COMMAND CENTER

Route: `/operator`

Recreate the quality and composition of the first reference image.

This should look like a sophisticated smart-mobility operations dashboard.

## Desktop Layout

Use a professional left sidebar with:

- Overview.
- Live Demo Map.
- Assistance Requests.
- Incidents.
- Bus Stops.
- Buses & Fleet.
- Reports.
- Scenario Lab.
- Digital Twin.
- Settings / Demo Information.

Every clickable navigation item must either open a real view or switch to an implemented section. Do not leave decorative, nonfunctional navigation links.

## Top Header

Include:

- Operator Dashboard.
- Short supporting description.
- Search for demo cases/stops.
- Notifications.
- Operator demo avatar.
- Demo Mode indicator.

## KPI Cards

Include:

1. Pending Assistance Requests.
2. Acknowledged Requests.
3. Potential Obstructions.
4. Boarding Outcomes / Unresolved Cases.

Provide a clear comparison or status visualization where useful.

All values must be derived from deterministic mock data and current application state.

Show:

**DEMO DATA — NOT LIVE STATISTICS**

Do not invent real-world service improvements or operational performance claims.

Avoid fabricated percentage improvements such as claims of a proven 96% boarding success rate.

## Live Demo Stop and Route Overview

Create a large visually appealing route panel containing:

- Schematic route map.
- Bus location marker.
- Two demo stops.
- Assistance request markers.
- Potential obstruction markers.
- Selected stop information.
- Filter legend.

Example status distinctions:

- No active alert.
- Assistance Requested.
- Potential Obstruction.
- Under Review.
- Resolved Incident.

Avoid treating absence of an alert as proof that a stop is safe or accessible.

## Assistance Request Queue

Display request cards or table rows containing:

- Request ID.
- Selected stop.
- Assistance type.
- Status.
- Simulated age or timestamp.
- View Details action.

Filters:

- Pending.
- Acknowledged.
- Needs Review.
- Resolved.

New passenger requests must appear here.

Driver acknowledgments and boarding results must update their corresponding records.

## Bus Stop Conditions

Provide visually refined status cards for both demo stops.

Show:

- Stop name.
- Stop code.
- Route.
- Current simulated advisory.
- View Details.

Do not invent actual local bus-stop operating conditions.

## Incident Timeline

Display chronological simulated events.

Examples:

- Assistance requested.
- Driver acknowledged.
- Potential obstruction detected.
- Obstruction cleared.
- Boarding attempt started.
- Boarding completed.
- Unable to board.
- Operator reviewed.

Use consistent icon and status colors.

## Incident Details Drawer

Selecting an incident opens a side drawer or panel.

Include:

- Incident ID.
- Related stop.
- Related request, if one exists.
- Event category.
- Timestamp.
- Evidence placeholder.
- Potential obstruction type, if applicable.
- Review status.
- Relevant explanatory information.
- Operator notes.

Buttons:

- Acknowledge / Review Incident.
- Mark Operator Reviewed.
- Add Note.
- Close Details.

Actions must update state.

Operator review must not falsely turn a failed boarding into successful boarding.

## Boarding Outcomes Visualization

Create a donut chart or another clean visualization using only actual local demo records.

Possible categories:

- Completed.
- Unable to Board.
- Pending.
- Cancelled.

Include clear counts and a simulated-data label.

## Operator Search and Filters

The search should filter actual local records by ID, stop, route, or case information.

All filter tabs must work.

Provide useful no-result states.

---

# 12. VIEW 07 — DIGITAL TWIN / VISION AI EXPERIENCE

Route: `/experience`

Build a polished integration-ready showcase for the team's Digital Twin and Vision AI work.

This view should be visually compelling but should never depend on unfinished external components.

## Digital Twin Section

Create a large visual module that can display:

- An illustrative bus stop.
- Road and curb.
- Boarding zone.
- Bus.
- Car.
- Motorcycle.
- Passenger assistance marker.
- Current scenario status.

Use original SVG, CSS illustrations, or a lightweight 3D-style schematic for the default experience.

If an external 3D widget is supplied later, make it easy to embed without changing the rest of the application.

### Scenario Visual Behavior

**Normal:** Clear illustrative boarding zone.

**Car Blocking:** Car highlighted with a red obstruction outline.

**Motorcycle Blocking:** Motorcycle highlighted with amber/red obstruction outline.

**Assistance Requested:** Assistance marker appears.

**Acknowledged:** Acknowledgment/signal state appears.

**Boarding Completed:** Successful boarding visual state.

**Unable to Board:** Unresolved barrier or failed-attempt state.

Do not build a production 3D engine merely for this demonstration.

## Vision AI Section

Show a polished recorded-video detection concept panel.

It may include:

- Demo camera frame.
- Boarding zone overlay.
- Detected object bounding box.
- Object class.
- Confidence value when available.
- Dwell duration.
- Overlap ratio.
- Detection status.
- Review status.

All manual examples must be marked simulated.

A separately imported event may identify itself as recorded-video model inference.

Do not pretend manual scenarios are actual AI inference.

## Integration Notes

The team may provide additional modules.

**Chit:** Interactive 3D Digital Twin.

**Aung:** Recorded-video obstruction detection.

Provide a clean integration interface for these components.

The base application must remain functional if neither module is available.

---

# 13. VIEW 08 — SCENARIO LAB

Route: `/demo`

This is the demonstration control center for judges.

Create a professional control panel with clear explanatory labels.

## Preset Scenarios

Implement all seven scenarios:

1. Normal.
2. Car Blocking.
3. Motorcycle Blocking.
4. Assistance Requested.
5. Assistance Acknowledged.
6. Boarding Completed.
7. Unable to Board.

Each preset must produce a coherent state across relevant roles.

For scenarios requiring an existing request, the preset should create the necessary illustrative prerequisite state rather than generating invalid transitions.

## Scenario Cards

Each scenario card should have:

- Icon.
- Name.
- Description.
- Current active state.
- Run Scenario action.
- Optional preview.

## Guided Demo

Provide a prominent:

**Run Guided Demo**

Create a guided walkthrough showing the complete solution.

The sequence must support:

**Step 1:** Simulate a car obstructing the boarding zone.

**Step 2:** Submit a wheelchair/ramp assistance request from the Passenger interface.

**Step 3:** Show the request appearing in the Driver Dashboard.

**Step 4:** Driver acknowledges the request.

**Step 5:** Show operator monitoring of the request and potential obstruction.

**Step 6:** Simulate the obstruction clearing or proceed with an unresolved obstruction.

**Step 7:** Driver begins boarding and records a successful or unsuccessful outcome.

**Step 8:** Operator reviews the outcome and the passenger sees the corresponding final status.

The walkthrough should offer clear Next Step guidance and role navigation.

Provide a success-path demonstration and a separate failure-path demonstration.

Target an understandable, reliable demonstration in approximately two minutes, without skipping core state transitions.

## Reset

Implement:

**Reset All Demo Data**

On click:

- Display confirmation.
- Reset shared state.
- Clear active generated requests.
- Clear demo incident state.
- Reset scenario state.
- Reset outcome records.
- Restore deterministic initial mock data.
- Return to the normal scenario.

Reset must work repeatedly.

## Activity Log

Include a human-readable chronological event log with timestamps and labels.

Each interaction should appear consistently.

---

# 14. SHARED STATE SYSTEM — ESSENTIAL

Use one central state store across the application.

Do not create independent passenger, driver, and operator mock states that cannot communicate.

The most important requirement is that a single action in one role updates the related views for all roles.

## Suggested Data Models

Implement strong TypeScript types.

### AssistanceRequest

Fields should include:

- id
- stopId
- routeId
- assistanceType
- note
- status
- createdAt
- acknowledgedAt
- boardingStartedAt
- completedAt
- cancelledAt
- failureReason
- relatedIncidentIds

### ObstructionIncident

Fields should include:

- id
- stopId
- routeId
- objectClass
- confidence
- sourceMode
- detectedAt
- clearedAt
- detectionStatus
- driverAcknowledged
- reviewStatus
- operatorNotes
- evidenceReference

### DemoState

Include:

- activeScenario
- selectedStopId
- route
- vehicle
- requests
- incidents
- boardingOutcomes
- activityLog
- guidedDemoProgress
- settings

Separate assistance requests from obstruction events.

A car being detected must never automatically create an assistance request.

## Request State Machine

Use:

`REQUESTED`

→ `DRIVER_ACKNOWLEDGED`

→ `BOARDING_ATTEMPT`

→ `COMPLETED` or `UNABLE_TO_BOARD`

Allow `CANCELLED` for eligible pending requests.

Validate transitions.

Disallow or explain invalid actions.

Do not silently skip required states during ordinary user interaction.

## State Persistence

Use localStorage if useful.

Role switching in the same browser must retain demo state.

Optionally support synchronization between tabs in the same browser using storage events.

Never claim that simulated changes are synchronized between separate users or devices.

## Derived Metrics

Compute counts and chart values from stored demo records.

Avoid hardcoding unrelated metric numbers that disagree with the visible queues or timelines.

## Timestamps

Use deterministic fixture timestamps or local demo timestamps.

Label them appropriately.

Do not present them as verified operational records.

---

# 15. SHARED EVENT CONTRACT

This event contract must be compatible with the team's integration work.

Use the following exact event names:

`OBSTRUCTION_DETECTED`

`OBSTRUCTION_CLEARED`

`ASSISTANCE_REQUESTED`

`DRIVER_ACKNOWLEDGED`

`BOARDING_COMPLETED`

`BOARDING_FAILED`

`OPERATOR_REVIEWED`

`DEMO_RESET`

## Sample AI Event JSON

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

The sample values are illustrative.

## JSON Import Feature

Create:

**Import AI Event JSON**

Allow local `.json` file selection.

Validate:

- JSON syntax.
- Schema version.
- Supported event type.
- Unique event ID.
- Supported stop ID.
- Supported route ID.
- Timestamp validity.
- Required type-specific fields.
- Numeric ranges when provided.
- Simulation/prototype constraints.

Use only the supported source modes:

- `manual_simulation`
- `recorded_video_model_inference`

When a valid obstruction event is imported:

1. Update shared obstruction state.
2. Display the corresponding driver warning.
3. Create or update the operator incident.
4. Update the appropriate stop advisory.
5. Update the Digital Twin/AI visualization.
6. Add the event to the activity log.

Handle duplicate event IDs safely.

Show clear validation errors for malformed or unsupported events.

Importing a recorded-video event must not require a live API.

Create a sample file:

`public/demo-assets/sample-obstruction-event.json`

## Integration Interface

Provide a simple reusable interface or callback such as:

`onScenarioChange(scenarioId)`

Also create a clean adapter for future Digital Twin integration.

Do not hardcode the visual simulation logic directly into every screen.

---

# 16. SIMULATION DATA & SCENARIOS

Create deterministic demo fixtures.

## Stops

- `CYB-DEMO-01` — Cyberjaya City Centre.
- `CYB-DEMO-02` — MMU Area.

## Route

- `DEMO-R01` — Cyberjaya Demo Shuttle.

## Scenario Semantics

### NORMAL

No active assistance request or obstruction in the clean baseline.

Do not claim stop safety is certified.

### CAR_BLOCKING

Show a potential car obstruction.

Driver receives an advisory.

Operator receives an incident for review.

Digital Twin highlights the car.

### MOTORCYCLE_BLOCKING

Similar to car obstruction, but object type is motorcycle.

### ASSISTANCE

Create a passenger assistance request.

Driver and operator see the request.

### ACKNOWLEDGED

Create or use a valid pending request and acknowledge it.

Passenger status updates accordingly.

### BOARDING_COMPLETED

Use a valid request progression and show confirmed boarding.

### BOARDING_FAILED

Record an unsuccessful boarding attempt with a reason.

Keep the associated operator case unresolved until reviewed according to the demo workflow.

## Important Logic

Obstruction detection is not proof of boarding failure.

Obstruction clearance is not proof of successful boarding.

Driver acknowledgment is not proof that physical assistance occurred.

Operator review does not rewrite the actual driver-recorded boarding outcome.

Maintain these distinctions throughout the UI.

---

# 17. ACCESSIBILITY & INCLUSIVE DESIGN

Accessibility is the purpose of this concept and must also be reflected in the software itself.

Implement:

- Semantic HTML.
- Proper form labels.
- Keyboard navigation.
- Visible focus states.
- Accessible dialogs.
- Screen-reader-friendly status announcements.
- Sufficient color contrast.
- Text labels alongside status colors.
- Large driver action controls.
- Minimum practical touch target of approximately 44 × 44px.
- Proper alternative text.
- Descriptive button names.
- Responsive typography.
- Reduced-motion support.
- Useful validation messages.
- No unnecessary medical or disability information collection.

The app should remain usable at narrow mobile widths and at browser zoom levels such as 200%.

Do not classify passenger disability from AI camera input.

All assistance requests must be voluntary.

---

# 18. RESPONSIVE DESIGN

Support at minimum:

**Mobile:** 375px and above.

**Tablet:** 768px and above.

**Desktop:** 1024px and above.

**Large Desktop:** 1440px and above.

## Passenger

Mobile-first.

Use compact navigation, stacked cards, readable maps, and large CTAs.

On desktop, present the mobile experience in a useful responsive application layout, not merely a stretched phone screen.

## Driver

Tablet-first.

Use a large split dashboard.

On phones, prioritize alerts and essential boarding actions.

## Operator

Desktop-first.

Use responsive sidebar behavior, flexible grid panels, and collapsible navigation.

On mobile, metrics, queues, and incidents should remain readable without horizontal page scrolling.

Tables may use contained scrolling only when absolutely necessary.

---

# 19. MICROINTERACTIONS & VISUAL POLISH

Use subtle, professional animation.

Recommended:

- Smooth route selection.
- Button hover and press feedback.
- Animated status progression.
- Toast entrance/exit.
- Small badge updates.
- Map marker selection.
- Incident drawer transition.
- Request card appearance.
- Success confirmation animation.
- Notification count update.
- Guided Demo step progression.

Avoid excessive movement.

No animation should interfere with keyboard navigation or accessibility.

Use skeleton loading only where it makes sense. Do not pretend a local synchronous action needs a remote server.

Create helpful empty states for:

- No requests.
- No incidents.
- No search results.
- No selected case.
- No passenger request.
- Digital Twin unavailable.
- Invalid JSON.
- Missing optional integration assets.

---

# 20. PROFESSIONAL APPLICATION BEHAVIOR

Every user-visible action must have a purpose.

Implement:

- Working role switching.
- Working route navigation.
- Working stop selection.
- Working assistance selection.
- Working form validation.
- Working assistance submission.
- Working request cancellation.
- Working driver acknowledgment.
- Working boarding attempt progression.
- Working boarding outcome recording.
- Working incident review.
- Working operator notes.
- Working filters.
- Working search.
- Working status details.
- Working scenarios.
- Working demo reset.
- Working JSON import.
- Working notifications or meaningful notification panels.
- Working guided demo.

If an optional feature cannot be implemented, do not show a misleading active button. Provide an explanatory disabled state or remove the control.

---

# 21. SUGGESTED PROJECT STRUCTURE

Use a clean, maintainable structure.

```text
naikready-web-demo/
├── public/
│   ├── favicon.svg
│   └── demo-assets/
│       └── sample-obstruction-event.json
├── src/
│   ├── assets/
│   │   └── naikready-logo.svg
│   ├── app/
│   │   ├── App.tsx
│   │   ├── routes.tsx
│   │   ├── demoReducer.ts
│   │   ├── demoData.ts
│   │   ├── demoTypes.ts
│   │   └── demoContext.tsx
│   ├── components/
│   │   ├── BrandHeader.tsx
│   │   ├── RoleSwitcher.tsx
│   │   ├── DemoModeBadge.tsx
│   │   ├── StatusBadge.tsx
│   │   ├── RouteMapDemo.tsx
│   │   ├── BusCard.tsx
│   │   ├── AssistanceCard.tsx
│   │   ├── IncidentCard.tsx
│   │   ├── Timeline.tsx
│   │   ├── KPIStatCard.tsx
│   │   ├── IncidentDetailsDrawer.tsx
│   │   ├── BoardingOutcomePanel.tsx
│   │   └── DigitalTwinPlaceholder.tsx
│   ├── pages/
│   │   ├── Welcome.tsx
│   │   ├── PassengerHome.tsx
│   │   ├── RequestAssistance.tsx
│   │   ├── PassengerStatus.tsx
│   │   ├── DriverDashboard.tsx
│   │   ├── OperatorDashboard.tsx
│   │   ├── Experience.tsx
│   │   └── ScenarioLab.tsx
│   ├── integrations/
│   │   ├── eventValidator.ts
│   │   ├── aiEventImporter.ts
│   │   └── digitalTwinAdapter.ts
│   ├── hooks/
│   ├── utils/
│   ├── styles/
│   │   └── globals.css
│   └── main.tsx
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── README.md
└── vercel.json
```

Adjust the structure to fit existing repository conventions, but preserve component separation and clear state ownership.

---

# 22. ERROR HANDLING & RELIABILITY

Handle:

- Empty request submissions.
- Missing stop selection.
- Too-long notes.
- Duplicate actions.
- Cancelled request acknowledgment attempts.
- Invalid state transitions.
- Missing request IDs.
- Unsupported JSON.
- Duplicate imported events.
- Unknown stops.
- Unavailable optional assets.
- Reloading a page with localStorage data.
- Corrupt or outdated localStorage content.
- Reset followed by a new walkthrough.

The prototype must not crash during an ordinary judge demonstration.

Use predictable state behavior and understandable error messages.

---

# 23. QUALITY CONTROL & TESTING

You must validate the completed application.

## Test 1 — Successful Assistance

1. Open Passenger Home.
2. Select Cyberjaya City Centre.
3. Select Wheelchair / Ramp.
4. Submit request.
5. Verify the passenger timeline shows REQUESTED.
6. Open Driver Dashboard.
7. Confirm request appears.
8. Acknowledge request.
9. Verify Passenger Status updates.
10. Begin boarding attempt.
11. Confirm Boarding Completed.
12. Verify Operator Dashboard reflects the completed outcome.

## Test 2 — Car Obstruction

1. Open Scenario Lab.
2. Trigger Car Blocking.
3. Confirm driver sees the warning.
4. Confirm operator sees the incident.
5. Confirm Digital Twin highlights the car.
6. Import a valid recorded-video car event.
7. Verify the correct event is processed without duplicate inconsistent records.

## Test 3 — Motorcycle Obstruction

1. Trigger Motorcycle Blocking.
2. Confirm driver warning.
3. Confirm operator incident.
4. Confirm boarding failure is not automatically recorded.

## Test 4 — Unsuccessful Boarding

1. Create a passenger request.
2. Acknowledge it.
3. Begin a boarding attempt.
4. Select Unable to Board.
5. Select Blocked Boarding Zone.
6. Confirm the passenger sees the failed outcome.
7. Confirm the operator sees an unresolved case.
8. Review the case.
9. Verify the recorded boarding outcome is preserved.

## Test 5 — Reset

1. Run the guided demo.
2. Generate multiple actions.
3. Reset all data.
4. Verify requests and incidents return to their deterministic baseline.
5. Verify maps and timelines match the reset state.
6. Run the demonstration again successfully.

## Additional Validation

- All eight routes load correctly.
- No broken buttons.
- No console runtime errors.
- No persistent TypeScript errors.
- No broken SVGs.
- No mobile page overflow.
- No broken browser back/forward navigation.
- No incorrect colors for statuses.
- No fake live-data claims.
- All 12 required feature groups are demonstrable.
- `npm run build` completes successfully.

If a testing framework is available, add focused tests for state transitions and event validation.

---

# 24. DEPLOYMENT

Prepare the application for Vercel static hosting.

Ensure:

- Correct Vite build configuration.
- SPA fallback routing.
- No secrets or environment variables required.
- All assets load correctly.
- Deep links work after refresh.
- Local demo state works in the browser.
- Responsive layout functions on the public deployment.

Provide clear installation and deployment commands.

Do not invent a live Vercel URL or claim deployment is complete unless it has genuinely been performed and verified.

---

# 25. REQUIRED DELIVERABLES

Produce:

1. A complete working React + TypeScript project.
2. All eight fully designed views.
3. All 12 functional MVP feature groups.
4. Original SVG brand assets.
5. A consistent professional design system.
6. Complete local demo data and state management.
7. Interactive passenger workflow.
8. Interactive driver workflow.
9. Interactive operator workflow.
10. Digital Twin and Vision AI integration placeholders.
11. A valid AI event JSON importer.
12. Sample obstruction-event JSON.
13. Scenario Lab with guided walkthrough.
14. Reset functionality.
15. README with setup and demonstration instructions.
16. Deployment-ready Vercel configuration.
17. At least six representative screenshots if the environment supports screenshot capture.
18. A short technical explanation suitable for competition submission slides.

If file-export capabilities are available, package the source as a ZIP.

Do not substitute screenshots or static mockups for the actual application.

---

# 26. PRIORITY ORDER

Follow this implementation priority:

**Priority 1 — Core Functional Workflow**

Passenger request → Driver acknowledgment → Boarding attempt → Boarding outcome → Operator visibility.

**Priority 2 — Demonstration Scenarios**

Car obstruction, motorcycle obstruction, incident handling, guided demo, reset.

**Priority 3 — Visual Excellence**

Match the reference designs with original, polished, accessible UI.

**Priority 4 — Integration Readiness**

JSON event import, 3D placeholder, Vision AI demonstration.

**Priority 5 — Final Validation**

Responsive testing, state reliability, build verification, Vercel readiness, README.

Do not sacrifice the working demonstration to add speculative features.

---

# 27. NON-NEGOTIABLE REQUIREMENTS

- This must be a working application, not only a design.
- Passenger, Driver, and Operator must share one coherent state.
- Every functional button must perform a meaningful action.
- All eight views must exist.
- All 12 specified feature groups must work.
- All simulated data must be labelled honestly.
- No false real-world 5G or AI deployment claims.
- No invented operational improvements or verified safety claims.
- No actual passenger personal data.
- No paid services or backend requirement.
- No dependency on unfinished Digital Twin or AI modules.
- No incomplete placeholder pages.
- No broken mobile layouts.
- No TypeScript build errors.
- No final response claiming functionality that has not been implemented.
- Preserve the exact supplied event types and demo route identifiers.
- Keep the application reliable and easy to present to competition judges.

---

# 28. FINAL EXECUTION INSTRUCTIONS

You are now responsible for implementing **NaikReady 5G — Final Competition Prototype**.

Use the supplied visual references for the design direction and the detailed requirements above as the functional specification.

If a project repository already exists, inspect and extend it while preserving working functionality.

If no project exists, create a complete Vite + React + TypeScript application.

Proceed through architecture, component creation, state management, pages, simulated workflows, integration placeholders, testing, and build verification.

**Do not stop after producing a plan. Do not return pseudocode in place of implementation. Do not leave essential features for the user to build manually.**

Create the actual project files.

Before finishing, verify the end-to-end demonstration.

When complete, provide:

- The final project structure.
- Instructions for running the application.
- A feature completion summary.
- The key demo workflow.
- Any remaining limitations.
- Build verification results.
- Deployment instructions.
- A source ZIP if supported.

## FINAL PRODUCT VISION

NaikReady 5G should feel like three interconnected, professionally designed applications within one seamless smart-mobility ecosystem.

The Passenger interface must feel welcoming, accessible, and effortless.

The Driver interface must feel clear, action-oriented, and operationally practical.

The Operator interface must feel intelligent, comprehensive, and credible.

The Digital Twin and Scenario Lab must make the innovation understandable through an engaging live demonstration.

**The defining moment of the prototype must be when a passenger's assistance request appears in the driver and operator interfaces, receives an acknowledgment, and progresses to a verified boarding outcome.**

That is what distinguishes NaikReady 5G from an ordinary bus-tracking application.

**Build a competition-ready, visually outstanding, reliable, and genuinely interactive demonstration that communicates this innovation clearly.**
