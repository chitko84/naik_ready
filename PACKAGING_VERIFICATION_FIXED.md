> Historical report for the previous release. The current UI/control update and verification results are in documentation/UPDATE_2_1.md.

# Fixed ZIP packaging verification

This release was rebuilt from the full merged project tree, not renamed or copied from the broken archive.

## Diagnosis

The earlier delivered file is 44,982,096 bytes. It begins with a ZIP local-file header but lacks a readable central directory/end record. Python reports `BadZipFile: File is not a zip file`. This is consistent with an incomplete/truncated archive. The exact point at which truncation occurred is not established.

## Source audit

- All 36 original web-project paths are represented in the merged frontend. Integration changes are retained; the original README and SVG twin source have their preserved copies.
- All 57 original AI/CCTV files outside the bundled environment/caches are present. The updated event exporter is included with the rest of the original project.
- The original Blender .blend and supporting README are byte-identical to their uploaded originals.
- React source, package-lock, TypeScript/Vite configuration, YOLO weights, FastAPI integration, all four GLBs and four rendered fallback views, README, Windows setup and test reports are included.
- Detailed path-by-path results: documentation/SOURCE_FILE_AUDIT_FIXED.json.

## Repackaging method

Python's standard zipfile writer uses ordinary DEFLATE compression (method 8), DOS-compatible regular-file attributes and ZIP version 2.0. ZIP64 and encryption are disabled. Paths use forward slashes and were checked for Windows-invalid characters, case collisions, symlinks and excessive path lengths. The longest archive path in the initial verification build was 96 characters.

The ZIP is fully closed, flushed and fsynced before it is atomically moved to the final output path. A partially written ZIP is never published under the final filename. tools/rebuild_zip.py reproduces this method.

## Verification performed

1. Fresh ZIP creation from source.
2. Python zipfile.testzip(): all entry CRC checks passed.
3. Independent Info-ZIP unzip -t: no errors in compressed data.
4. Full extraction to a separate temporary folder and byte comparison of every extracted file.
5. Fresh npm ci, production build and tests executed from that extracted project, not the working project.
6. Final archive rebuilt with the new verification logs and per-file SHA256 manifest, followed by another complete ZIP/CRC/extraction/hash check.

## Rerun results

| Check on extracted project | Result |
|---|---|
| npm ci | PASS — 122 dependencies installed |
| npm run build | PASS — TypeScript and Vite |
| npm test | PASS — 20 frontend/GLB tests |
| Original AI/CCTV pytest suite | PASS — 19 tests |
| Backend API pytest suite | PASS — 6 tests, including actual image/video inference |

45 tests passed. Raw rerun logs are the documentation/FIXED_*_OUTPUT.txt files. Existing non-fatal Vite chunk-size and Starlette/httpx deprecation advisories remain; no application source changes were needed for packaging repair.

The tests did not add field accuracy claims: the actual image/video fixtures produced no detections/events. Native Windows Explorer was not available for a direct OS test. Archive compatibility was checked using the standard ZIP format, CRC tests, independent unzip and full extraction. Original WebGL/physical-device limitations remain documented in TEST_REPORT.md.

## Included/excluded files

Only reproducible environments and runtime/build outputs are excluded: node_modules, .venv, Python/test caches, backend/runtime and frontend/dist. Run the included Windows setup commands to install dependencies and build locally. All essential source, model and 3D/media assets remain included.

PACKAGE_MANIFEST_FIXED.json lists byte sizes and SHA256 values for every packaged file other than the manifest itself. The archive's final SHA256 is provided with delivery verification outside the ZIP to avoid a self-referential checksum.
