# Vision AI v2 validation

Client date: 26 October 2026, Malaysia time.

19 automated checks cover zone geometry, stationary dwell, temporary loss and clearance hysteresis, moving vehicles, bus exemption, multi-object matching, fixture timings, current UI, polygon validation, default ten-second obstruction and v1.0 event export.

Browser checks: the four manual simulation states, Zone Configuration and Detection History screens were rendered in Chromium 140 via Playwright 1.55 on Linux, at 1440px width. No Streamlit exception or document horizontal overflow was observed. Six actual UI screenshots are included. Windows installation has not been executed here.

The existing pretrained-model adapter was previously exercised on 80 frames of public reference road footage. This release does not claim a fresh model run on target-site footage or photographic obstruction evidence. No authorized bus-stop recording was supplied. The included model allows local analysis of an authorized upload. Min's importer was not available, so actual cross-app acceptance remains unverified; exported arrays are checked against the supplied field contract locally.

The four illustrated fixtures are explicitly manual simulation. They use the existing three-second sequence, while real analysis defaults to ten seconds. The timing exception is shown in the UI. Confidence is null for fixtures. No 5G communication, real-time FPS, passenger identity, disability recognition, enforcement or successful boarding is claimed.


## Photorealistic scene update

Four new synthetic photographic assets are bundled unchanged in assets/photoreal. All four scenario screens, zone configuration and history were captured again in the actual running browser. The 19 existing tests pass. Runtime boxes and polygons are manual presentation overlays, not detector output. Display toggles control those overlays; confidence remains unavailable. The source images are not a continuous recording. No new actual-inference or network-performance measurement is claimed.
