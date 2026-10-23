import { defineConfig } from 'vite';
export default defineConfig({ base: './', build: { outDir: '../site/3d', emptyOutDir: true, chunkSizeWarningLimit: 1500 } });
