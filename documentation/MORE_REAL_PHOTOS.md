# Real-life photography update 2.5

Added four real photographs: Kuala Lumpur evening travel, terminal commuters, a wheelchair user at a Delft bus shelter, and accessibility markings on a bus door. The home page includes a quiet three-photo editorial section. Existing supporting photo slots are updated in Passenger, Request Assistance, Fleet and Activity. Main actions remain ahead of supporting photography; the simple blue/teal design and progressive disclosure are preserved.

All ten photographs now have small responsive WebP versions. Shared photo components include srcset, sizes, intrinsic dimensions, crop positions, asynchronous decoding and lazy loading. The landing hero photo loads eagerly with high priority. Credits and descriptive alternative text remain visible/available; no motion or new controls were added. A low-contrast photo-story caption was corrected.

Validation: 31 frontend tests passed and TypeScript/Vite production build passed (existing Three.js chunk advisory). Browser checks across eight routes in 320, 768 and 1280 pixel frames found no page-level horizontal overflow or broken completed photo loads. The new editorial section was visually reviewed after loading. Every local original JPEG and responsive WebP was decoded and verified. Backend, shared state and 3D behavior are unchanged; their earlier test logs are retained.

The complete ZIP was rebuilt with standard DEFLATE, tested with Python zipfile.testzip(), extracted to a new temporary directory, and verified against all manifest hashes. It includes React sources, original AI CCTV source/model, backend, twin assets, photographs, credits and setup/configuration files. See SETUP_GUIDE.md for Windows startup commands.

The scope limits recorded in SIMPLE_UX_ACCEPTANCE.md remain applicable; this is a visual update and does not complete the separate proposed seven-feature upgrade.
