# Replace files and redeploy NaikReady 5G

This package contains the full application source, not just vercel.json. It is based on GitHub main commit 79534b0b3d49dbd47f4ae87485c356f47d244afb (checked 31 October 2026).

## 1. Copy the update into your existing Git repository

Extract the ZIP completely. Open its NaikReady_5G_Vercel folder. Copy its CONTENTS into the existing naik_ready repository and allow replacement. Keep your existing .git folder. Do not place the new project inside another nested folder.

The repository root must contain vercel.json, frontend/, backend/, and ai-cctv/ side by side. Original digital-twin source is also included, although Vercel does not upload that editable Blender source because the browser uses frontend/public/twin instead.

A file-copy operation does not remove deleted files. In PowerShell, from your EXISTING repository root, remove the obsolete frontend-only configuration:

```powershell
Remove-Item .\frontend\vercel.json -ErrorAction SilentlyContinue
```

Do not remove frontend/vite.config.ts. Keep the new ROOT vercel.json.

## 2. Check the frontend locally and push

```powershell
cd frontend
npm ci
npm test
npm run build
cd ..
git status
git add -A
git commit -m "Configure Vercel services and private AI integration"
git push origin main
```

Review git status before committing so unrelated personal files are not included. This package excludes .git, local Python environments, node_modules, build output, runtime uploads and temporary files. Existing local runtime records are not part of the deployment.

## 3. Correct the existing Vercel project settings

Open your Vercel project, then Settings > Build and Deployment:

- Root Directory: repository root (leave blank or use the repository-root option). It must NOT be frontend, backend, ai-cctv, or a new enclosing ZIP folder.
- Framework Preset at project level: Other, if a manual preset is required. The root services configuration supplies Vite for frontend and FastAPI for backend, while AI uses its Dockerfile. Allow services detection where the dashboard provides it.
- Remove old project-level Install Command, Build Command and Output Directory overrides intended for a frontend-only deployment. Service-specific settings are already in vercel.json. The frontend service runs npm ci, npm run build, and uses dist.
- Enable Fluid Compute if this is an older project with it disabled. Review your available function duration and container support. The public gateway requests up to 300 seconds; a slow analysis can still time out.
- Do not manually create AI_CCTV_URL. The service binding injects this value at runtime. If an old manually configured value exists, remove that old override so it cannot conflict with the binding.
- Keep unrelated existing secrets/settings. No frontend API key is required by this configuration.

Redeploy the NEW Git commit. For the first retry, deselect Use existing Build Cache if the dashboard offers it. Inspect the deployment logs for three services: frontend, backend, and ai-cctv. The AI service installs CPU Torch and builds an HTTP container, rather than running Streamlit.

## 4. What this fixes

- The original frontend-only setup did not deploy a running Python API.
- The original ai-cctv/app.py is a Streamlit console, not the API entrypoint. service.py and Dockerfile expose the detector over HTTP while preserving the original local console.
- Backend requirements for Vercel are lightweight. Torch, OpenCV and model loading belong in the private AI container.
- Browser requests stay on /api/...; backend routes retain that prefix. The gateway calls the private AI service through AI_CCTV_URL.
- Hosted analysis completes within its request and returns evidence directly. It does not rely on polling a job/evidence file on a different serverless instance.
- The hosted upload cap is 3,500,000 bytes. Use a short/small video, or local inference for the original 40 MiB allowance. Images report observations, not temporal obstruction events.
- Uploaded-media errors remain real errors. The application does not replace failed model results with a scenario result.

These are verified code/configuration corrections. The precise cause of your earlier cloud failure cannot be established without its Vercel deployment log.

## 5. After redeployment

Open the homepage and refresh /passenger, /operator and /experience directly. Check /api/health in the browser. Its JSON should report inference_available: true when detector dependencies and weights are available. Scenario analysis and bundled reference evidence should remain available even if the AI API is unavailable.

Then analyze a small authorized JPEG and a short video under 3.5 MB. A single JPEG can correctly return zero events. A prerecorded video returning zero obstruction events is also a valid result, not a deployment failure. Check actual evidence delivery and browser console/network errors if the upload fails.

The Python gateway health endpoint returns 503 if the binding/AI service is unreachable. Record the first relevant error in Build Logs or Function Logs if Vercel fails. Do not treat a green frontend page as proof that the AI container is working.

## 6. Local development

Use Python 3.12 and Node.js 22 or 24. From the root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements-local.txt
cd frontend
npm ci
npm run dev
```

Open http://localhost:5173. Local development keeps the original queued API and 40 MiB allowance. The standalone Streamlit project remains under ai-cctv; install its own requirements to run that console.

For three-service development, install a current Vercel CLI and Docker Desktop, then run `npx vercel dev --local` from the repository root. Docker CLI and the Docker daemon are needed for the AI container. Generated service bindings come from Vercel; do not substitute a localhost URL into deployment settings.

## Final service choices for owner review

- frontend: public site at / and all non-API paths.
- backend: public API at /api and /api/..., with JSON 404 for unknown API endpoints.
- ai-cctv: private HTTP inference container, no public rewrite.
- One binding: backend calls ai-cctv via AI_CCTV_URL. The static frontend calls the public same-origin API, not a private runtime binding.

Please confirm these service names, public paths and binding before deploying if they differ from your intended topology. The final vercel.json is included at the root. No Git push or cloud deployment was performed while preparing this ZIP.

Official references, checked 31 October 2026:
- https://vercel.com/docs/services
- https://vercel.com/docs/services/bindings
- https://vercel.com/docs/services/routing
- https://vercel.com/docs/services/config-reference
- https://vercel.com/docs/functions/runtimes/container
- https://vercel.com/docs/functions/limitations
