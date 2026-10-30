# Photography update

The landing hero now shows Kuala Lumpur street life, and the final call to action uses a city skyline photograph. Matching photo banners and cards were added to Passenger, assistance requests, Driver, Operator overview and fleet, Digital Twin, Scenario Lab and Activity. The passenger status card uses an existing real bus photograph. Original workflow controls, state, maps, 3D assets and AI processing are preserved.

Images have descriptive alternative text, credits, darkened overlays where text crosses photography, reserved layout space and responsive crops. Informational images use lazy loading; no new application dependency is needed. PHOTO_CREDITS.md records sources and licensing.

Validation: 31 frontend tests passed; TypeScript/Vite production build passed, with the existing large Three.js chunk advisory. Browser checks of eight routes in mobile, tablet and desktop frames found no horizontal page overflow or broken completed photo loads. Actual measured content widths were 305, 753 and 1333 pixels (browser scrollbars/viewport constraints). Desktop landing and driver compositions were visually reviewed. Backend logic was not changed.

Packaging: rebuilt with the standard DEFLATE ZIP method, tested using Python zipfile.testzip(), extracted into a fresh temporary directory, and verified against every SHA-256 manifest entry.
