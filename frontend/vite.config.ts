import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
// Vite runs in the browser; private Vercel bindings belong only to Python functions.
// This proxy is for standalone npm run dev, not production routing.
const localApi = process.env.NAIKREADY_LOCAL_API_URL || 'http://127.0.0.1:8000';
export default defineConfig({ plugins: [react()], server:{allowedHosts:['terminal.local'],proxy:{'/api':localApi}}, build:{rollupOptions:{output:{manualChunks:{react:['react','react-dom','react-router-dom'],three:['three'],charts:['recharts']}}}} });
