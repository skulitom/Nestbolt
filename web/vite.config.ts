import { defineConfig } from 'vite';

// Relative asset paths so the site works from a GitHub Pages project path.
export default defineConfig({
  base: './',
  esbuild: { jsx: 'automatic', jsxImportSource: 'preact' },
  worker: { format: 'es' },
  build: { target: 'es2022', outDir: 'dist', emptyOutDir: true },
});
