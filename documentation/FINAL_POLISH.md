# Visual polish · 29 October 2026

Added a connected-journey ribbon with a brief animated light trace, softer teal/blue hero surfaces, gradient typography, gentle entrance motion, floating journey cards, photo hover zooms on pointer devices, and clearer button hover/press feedback. Existing transport, map, CCTV and Blender functionality is retained.

Motion is a progressive enhancement: content remains visible without IntersectionObserver, and reduced-motion preferences disable the effects. Automatic decorative motion finishes within five seconds. Reveal animations do not leave transforms on panels, so fixed dialogs and expanded maps retain their viewport positioning. No animation library or new runtime dependency is required.

Validation:
- 31 frontend tests passed, including shared state, scene transitions, bounded analysis polling and route geometry.
- TypeScript/Vite production build passed (existing Three.js chunk-size advisory remains).
- Browser reviewed at desktop, 320px mobile and 768px tablet; no horizontal page overflow in the checked layouts.
- Normal and Blocked each selected correctly with one click in the browser.
- Browser environment lacks WebGL: rendered Blender fallback verified; this update does not change the 3D renderer.
- Final archive verified with Python testzip(), extracted into a fresh temporary directory, and checked against every manifest hash.

Full application setup remains in README.md and documentation/SETUP_GUIDE.md. Earlier API and original AI source validation logs are retained; backend code and models are unchanged by this visual-only pass.
