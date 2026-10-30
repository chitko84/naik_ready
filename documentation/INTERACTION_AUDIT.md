# Interaction audit

| Area | Meaningful behavior | Verification |
|---|---|---|
| Global navigation / mobile menu / bottom navigation | Original routes plus notifications/history | Browser route and mobile checks |
| Stop selectors / map markers / focus | Shared selected stop, contextual route/ETA | Source inspection + rendered route checks |
| Passenger form | Six choices, required validation, stop/note, request creation | Browser submission + reducer tests |
| Passenger status / cancel / new request | Timeline, pending cancellation, follow-up request | Browser status + reducer cancellation tests |
| Driver queue / tabs | Request selection and scroll destinations | Preserved source / rendered queue |
| Driver stationary / acknowledge / verify / begin / complete | Gated lifecycle and shared updates | Browser successful flow + reducer tests |
| Driver unable-to-board / reasons | Failure from acknowledged or boarding stage | Preserved modal / reducer guided-failure tests |
| Driver warnings / evidence | Source metadata, acknowledgment while stationary, close review | Source audit + shared incident checks |
| Operator eight sections | Overview, map, requests, incidents, stops, fleet, reports, information | Preserved branches + route render |
| Search / queue filters / cards | Record filtering, selected details, stop focus | Source audit / browser case selection |
| Incident drawer | Response assignment, notes, manual clearance, review | Browser assignment/clear/notes/reload |
| Request drawer notes | Saves notes without changing nonterminal status | Reducer test |
| Scenario presets / guided modes / step / replay / reset | Original scenarios and both outcomes retained | 16 workflow tests + source audit |
| JSON import | Validated object or array, errors, duplicate skipping, chronological application | Validator / episode tests |
| Twin selectors | Mutate shared scenario records | Browser sensor-to-scene check |
| Twin zoom / reset | Three.js camera or rendered fallback zoom/reset | Fallback browser check; WebGL interaction unverified |
| Vision source tabs / video disclosure | Labeled sources and supplied annotated media | Browser replay view / source audit |
| Vision upload / zone / stop / dwell / analysis | Form configuration, validation, job polling, results/evidence | Actual API image/video tests; browser upload unverified |
| Apply sensor event | Validated, deduplicated reducer actions | Browser scripted application + reducer tests |
| History tabs / search / export | Updates or request list, filtering, downloadable JSON | Source/type audit + rendered history route |

Every retained visible control has an implementation path; this table distinguishes interactive browser checks from code/automated verification. It does not claim every possible combination was clicked.
