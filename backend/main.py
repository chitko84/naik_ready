"""Public API entrypoint. Vercel uses a private binding; local development keeps queued YOLO jobs."""
import importlib.util
import os
import sys
from pathlib import Path

def _create_app():
    if os.environ.get('AI_CCTV_URL') or os.environ.get('VERCEL'):
        try:
            from .gateway import create_app
        except ImportError:  # Vercel imports main:app from the backend service root.
            from gateway import create_app
        return create_app()
    else:
        source = Path(__file__).resolve().parents[1] / 'ai-cctv' / 'local_api.py'
        spec = importlib.util.spec_from_file_location('naikready_local_api', source)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module.app


# Keep the ASGI export at module scope for Vercel handler discovery.
app = _create_app()
