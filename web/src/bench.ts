// Benchmark hook for scripts/g5_browser.py: runs one polygon job per call in a
// fresh worker and reports the result with the engine's linear memory.
import { nestJob } from './engine';

declare global {
  interface Window {
    nestJob: typeof nestJob;
    benchReady: boolean;
  }
}

window.nestJob = nestJob;
window.benchReady = true;
