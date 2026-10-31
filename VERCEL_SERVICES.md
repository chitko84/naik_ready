# Vercel service architecture

Full replacement package prepared 31 October 2026 against GitHub main commit 79534b0b3d49dbd47f4ae87485c356f47d244afb. Begin with VERCEL_REDEPLOY.md for copying files, dashboard settings and push commands. No cloud deployment or Git push has been performed in preparing the package.

## Final topology to confirm

| Service | Root | Runtime | Public path | Outbound calls |
| --- | --- | --- | --- | --- |
| frontend | frontend | Vite static build | / and all non-API routes | Browser calls same-origin /api/... |
| backend | backend | FastAPI / Python | /api and /api/... | ai-cctv via AI_CCTV_URL binding |
| ai-cctv | ai-cctv | HTTP container | None; internal only | None |

The only binding is declared on backend: type=service, service=ai-cctv, format=url, env=AI_CCTV_URL. Vercel injects it at runtime. Do not set that variable yourself. A static browser frontend cannot consume a private runtime binding, so none is declared on frontend.

Public rewrites route API paths first, then use the frontend catch-all last. Vercel preserves /api/... when it forwards the public request, and the gateway's routes use that prefix. Unknown API routes return JSON 404. frontend's service-level SPA rewrite supports direct refresh of /passenger, /operator and /experience. Root vercel.json owns service build/runtime configuration; the obsolete frontend/vercel.json is removed.

## AI packaging

The original ai-cctv/app.py is a Streamlit console. It remains available for local use. ai-cctv/service.py supplies FastAPI /health, /analyze and /replay/{mode}; serve.py listens on PORT or default 80. Its Dockerfile installs CPU Torch and the service dependencies, includes the bundled model and detector/config/export modules, and excludes presentation assets, tests and large source videos from the image.

backend/main.py selects the public gateway under Vercel. It does not import Torch, OpenCV, the detector or local runtime job storage on that path. backend/requirements.txt contains only the public API dependencies. Local development installs backend/requirements-local.txt and continues using the original local queued inference implementation relocated to ai-cctv/local_api.py.

## Hosted analysis behavior

Hosted analysis is awaited within one internal HTTP request. It returns the result and a size-bounded JPEG data URL directly, avoiding a later request that depends on a different instance's temporary job files. The frontend understands both this direct response and the original local queued API. Hosted /api/jobs/... responds with 410 and resubmission guidance; local queued endpoints remain available during local development.

Hosted uploads are capped at 3,500,000 bytes. Evidence is compressed, resized to at most 960 pixels on its longest edge and capped at 1 MB before base64 encoding. Temporary job files are deleted after response assembly. No durable cloud evidence history is provided. Gateway inference calls time out after 230 seconds; browser wait is bounded at 250 seconds; the gateway function requests maxDuration 300, subject to platform/account settings. Videos must still satisfy the detector's 60-second/12,000-source-frame limits. Image occupancy does not create a stationary obstruction event.

Local npm run dev retains the original 40 MiB queued upload behavior. Original role state remains browser-local. This deployment update does not add a multi-user database or measured 5G service.

## Validation for this replacement package

- Current official Vercel JSON schema validation passed for the root configuration.
- Fresh npm ci completed.
- 35 frontend tests passed; TypeScript/Vite production build passed.
- 42 Python tests passed: original monitor/export/UI checks, local API actual image/video inference, gateway/private HTTP service tests, a Vercel entrypoint dependency-isolation test, and an actual detector test of the private service's inline result/JPEG/cleanup path. Some unit tests deliberately mock transport or detector outputs; the actual-inference tests use the bundled CPU model.
- An isolated AI-only copy of the container's source context successfully imported, served health and both replay modes, with no sibling backend required.
- ZIP integrity, complete extraction and source hashes are verified before delivery; see VERCEL_PACKAGE_VERIFICATION.json.
- The build retains the existing Three.js size advisory. Python checks emit an upstream TestClient deprecation warning; all checks pass.

These are local code/packaging checks. No Docker engine is available here, so the Docker image itself was not built. No Vercel account project, production binding or deployed inference request has been tested. Check the new commit's Vercel Build Logs and Function Logs after redeployment. Without the earlier failure log, the exact earlier account/build error cannot be established.

## Official references

Checked 31 October 2026:
- https://vercel.com/docs/services
- https://vercel.com/docs/services/bindings
- https://vercel.com/docs/services/routing
- https://vercel.com/docs/services/config-reference
- https://vercel.com/docs/functions/runtimes/container
- https://vercel.com/docs/functions/configuring-functions/duration
- https://vercel.com/docs/functions/limitations
