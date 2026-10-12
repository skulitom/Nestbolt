import { defineConfig } from 'vite';

// Relative asset paths so the site works from a GitHub Pages project path.
// bench.html is the benchmark runner used by scripts/g5_browser.py.
export default defineConfig({
  base: './',
  esbuild: { jsx: 'automatic', jsxImportSource: 'preact' },
  worker: { format: 'es' },
  build: {
    target: 'es2022',
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: { input: { main: 'index.html', bench: 'bench.html' } },
  },
});
