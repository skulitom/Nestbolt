import { partGeometry } from './types.js';
import type { Library, NestRequest } from './types.js';

// Each search owns its collision indices. The measured curve-heavy scale job
// fits with one worker after lifetime reduction, but two still exceed 1.5 GB.
// This conservative complexity cap is a heuristic, not a memory guarantee for
// arbitrary geometry. Keep the existing cap for simpler high-quantity jobs.
const COMPLEX_JOB_VERTICES = 500_000;
const LARGE_JOB_COPIES = 1000;

export function workersFor(library: Library, request: NestRequest, chosen: number): number {
  const requested = Number.isFinite(chosen) ? Math.max(1, Math.floor(chosen)) : 1;
  const vertices = new Map(library.parts.map(part => [part.id, partGeometry(part).reduce((sum, polygon) =>
    sum + polygon.outer.length + polygon.holes.reduce((n, hole) => n + hole.length, 0), 0)]));
  let copies = 0, work = 0;
  for (const part of request.parts) {
    copies += part.quantity;
    work += part.quantity * (vertices.get(part.id) ?? 0);
  }
  return Math.min(requested, work >= COMPLEX_JOB_VERTICES ? 1 : copies > LARGE_JOB_COPIES ? 2 : requested);
}
