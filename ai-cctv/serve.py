"""Vercel dev injects PORT; this entrypoint also works on Windows."""
import os
import uvicorn

if __name__ == '__main__':
    uvicorn.run('service:app', host='0.0.0.0', port=int(os.environ.get('PORT', '80')))
