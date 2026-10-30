# Integration changes

- Preserved all original routes, six assistance types, two stops, operator sections, request/incident workflows, scenario presets, outcome reasons, reset and guided success/failure journeys.
- Extended the reducer with stop-specific boarding verification and obstruction gates, response assignment, episode-aware clears, general case notes, linked incidents and validated hydration.
- Added Activity/history, same-origin storage synchronization, source-aware Vision console and backend API.
- Fixed original event compatibility issues: scripted null confidence, legacy stop IDs, truck labels and array imports. Duplicate events are skipped without creating duplicate incidents.
- Replaced the primary SVG twin with original Blender-derived GLBs; retained the schematic source. Added rendered fallback, responsive viewer controls and four shared-state scenarios. Full source Blender animation is preserved rather than converted into a continuous browser timeline.
- Added stationary driver controls; preserved failure reporting when an obstruction prevents starting a ramp boarding attempt.
- Corrected cancelled/blocked request timelines so they do not imply an unperformed boarding attempt.
- Refined navy/teal surfaces, operator sidebar, cards, loading/empty states, mobile bottom navigation, small-screen forms, drawer spacing and safe-area support. Fixed the original body minimum width that caused overflow at 320 px. Times display in Asia/Kuala_Lumpur.
- Added a combined local dev runner, Windows start script, Vite API proxy, built-app Python serving, tests and documentation.
- Excluded bundled .venv, node_modules, redundant dist output, caches and generated analysis jobs from the archive. Original AI source, weights, useful supplied media, licenses and Blender source remain included.
