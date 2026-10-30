// One command for the frontend and optional local Vision API.
import {existsSync} from 'node:fs';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const front=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const root=path.resolve(front,'..');
const venv=path.join(root,'.venv',process.platform==='win32'?'Scripts/python.exe':'bin/python');
const py=process.env.NAIKREADY_PYTHON || (existsSync(venv)?venv:null) || (process.platform==='win32'?'python':'python3');
const api=spawn(py,['-m','uvicorn','backend.main:app','--host','127.0.0.1','--port','8000'],{cwd:root,stdio:'inherit'});
api.on('error',()=>console.log('Vision API could not start. Replay remains available. See SETUP_GUIDE.md.'));
api.on('exit',code=>{if(code)console.log('Vision API is offline. Replay remains available. Install backend requirements or choose NAIKREADY_PYTHON.');});
const web=spawn(process.execPath,[path.join(front,'node_modules/vite/bin/vite.js'),'--host','0.0.0.0',...process.argv.slice(2)],{cwd:front,stdio:'inherit'});
const stop=()=>{api.kill();web.kill()};process.on('SIGINT',stop);process.on('SIGTERM',stop);web.on('exit',code=>{api.kill();process.exit(code??0)});
