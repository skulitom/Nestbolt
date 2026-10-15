import type { Mode, NestResult } from './types.js';

/** The native objective, including original part area rather than lead waste. */
export function betterResult(candidate: NestResult, incumbent: NestResult, mode: Mode): boolean {
  const key = (r: NestResult): number[] => {
    const m = r.validation.metrics;
    if (!r.validation.valid || !m) return [Infinity, Infinity];
    if (mode === 'fill_priority') return [-m.placed_priority, -m.placed_area, m.material_area];
    if (mode === 'fill_area') return [-m.placed_area, m.material_area];
    return [m.sheets_used, m.material_area];
  };
  const a = key(candidate), b = key(incumbent);
  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) return a[i] < b[i];
  }
  return false;
}
