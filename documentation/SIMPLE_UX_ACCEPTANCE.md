# Simple, natural UI/UX update · 29 October 2026

This requirement supersedes the earlier decorative motion pass. The interface keeps the blue/teal identity and authentic photographs with their credits. Primary buttons use a solid blue. Decorative page reveals, floating records, photo zooms, glow and broad gradient surfaces are removed from the active interface; useful loading and progress feedback remain.

## Role flows

- Passenger: choose a stop, request support, track the latest request. The map and technical route/source details are optional disclosures; the request action appears before the arrival card and map.
- Driver: stationary-use controls, route and assistance workflow stay in place. The contextual photograph sits after operational content.
- Operator: incidents and assistance requests are the default view. Route/stop details, metrics, charts and recent activity are expandable. All original sidebar sections remain. An incident's CCTV link selects its stop before opening the existing evidence desk; source labels remain visible.
- Presentation: the existing guided walkthrough comes first in both document and visual order. All seven individual scenarios, street preview, event import and activity log remain available through expandable controls. These seven scenario presets are distinct from the separately proposed seven enhancement modules.
- Twin / Vision: working twin and analysis controls remain visible; connectivity explanation and supporting context are expandable.

## Acceptance review

| Criterion | Evidence / limit |
| --- | --- |
| Clear first action | Role-specific request, review or walkthrough action; heuristic review, not a first-time-user study |
| Navigation | Existing header, mobile navigation and operator sections preserved |
| Screen purpose | Role flows and default operator/presentation order reviewed in browser |
| Less clutter | Duplicate home statistics and floating decoration removed; secondary reports/context collapsed |
| Mobile use | Nine routes checked in 320, 390, 768 and 1280 pixel frames; no page-level horizontal overflow. Frame content widths account for 15px scrollbars. Main controls have at least 44px height |
| Restrained effects | Solid surfaces, reduced shadows; no decorative reveal observer or auto-moving hero elements |
| Professional appearance | Desktop landing, passenger, operator and guided progress/outcome inspected visually |
| Functionality | 31 frontend tests and six API tests pass; complete eight-step successful journey verified through browser controls. Native disclosure opens with Enter; all seven scenario choices remain reachable. Incident evidence navigation retains the selected stop |

Maps inside closed disclosures mount when opened so their initial bounds use a visible container. The optional preview similarly defers 3D initialization until opened. Existing scene and record state is preserved centrally.

## Scope and remaining enhancement work

This archive is the UI/UX simplification of the existing prototype, not a claim that the entire proposed seven-feature upgrade has been built. It already contains shared local role state, synchronized scenes, real upload inference, incident actions, a guided journey and a geographic route explorer. A dedicated 5G Network & Recovery view, backend-backed Mission Control and the expanded Judge Presentation Mode are not implemented as the full proposed modules in this source. No fabricated 5G measurements, deployed-network claims or new dashboards were added to imply otherwise.

The browser environment cannot render WebGL; its original rendered-scene fallback is available. Actual GPU rendering was not revalidated here. Backend tests exercise actual image/video inference and API validation. They do not establish field detection accuracy. Build retains the existing Three.js bundle-size advisory and backend tests report one upstream TestClient deprecation warning.

The ZIP is rebuilt using standard DEFLATE, checked with zipfile.testzip(), extracted to a fresh temporary directory and checked against every SHA-256 manifest entry before delivery. Earlier release notes/logs remain for provenance; this note describes the current presentation behavior.
