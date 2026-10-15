import { partGeometry } from './types.js';
import type { Layout, Library, Polygon, Transform } from './types.js';

type Bounds = readonly [number, number, number, number];
interface PreviewPart { path: string; polygons: Polygon[]; orientations: Map<string, Bounds> }

// Imported libraries and received layouts are immutable snapshots in the app.
// Weak keys release old projects/layouts; free rotations have a bounded cache.
const libraries = new WeakMap<Library, Map<string, PreviewPart>>();
const layouts = new WeakMap<Library, WeakMap<Layout, ReadonlyMap<string, Bounds>>>();
const ORIENTATIONS_PER_PART = 128;

/** One original polygon path per part, in SVG's downward-Y coordinates. */
export function previewParts(library: Library): ReadonlyMap<string, PreviewPart> {
  let parts = libraries.get(library);
  if (!parts) {
    parts = new Map(library.parts.map(part => {
      const polygons = partGeometry(part);
      const path = polygons.flatMap(p => [p.outer, ...p.holes]).map(ring =>
        ring.map(([x, y], i) => `${i ? 'L' : 'M'}${x} ${-y}`).join(' ') + ' Z').join(' ');
      return [part.id, { polygons, path, orientations: new Map<string, Bounds>() }];
    }));
    libraries.set(library, parts);
  }
  return parts;
}

function orientedBounds(part: PreviewPart, transform: Transform): Bounds {
  const key = `${transform.mirrored}/${transform.rotation_radians}`;
  const cached = part.orientations.get(key);
  if (cached) return cached;
  const c = Math.cos(transform.rotation_radians), s = Math.sin(transform.rotation_radians);
  const m = transform.mirrored ? -1 : 1;
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const polygon of part.polygons) for (const [x, y] of polygon.outer) {
    const u = c * (m * x) - s * y, v = s * (m * x) + c * y;
    x0 = Math.min(x0, u); y0 = Math.min(y0, v);
    x1 = Math.max(x1, u); y1 = Math.max(y1, v);
  }
  const bounds: Bounds = [x0, y0, x1, y1];
  if (part.orientations.size >= ORIENTATIONS_PER_PART) {
    part.orientations.delete(part.orientations.keys().next().value!);
  }
  part.orientations.set(key, bounds);
  return bounds;
}

/** Exact vertex extents, computed once per received layout and reused by every view. */
export function layoutBounds(library: Library, layout: Layout): ReadonlyMap<string, Bounds> {
  let cached = layouts.get(library);
  if (!cached) { cached = new WeakMap(); layouts.set(library, cached); }
  const known = cached.get(layout);
  if (known) return known;
  const parts = previewParts(library);
  const boxes = new Map<string, Bounds>();
  for (const placement of layout.placements) {
    const part = parts.get(placement.part_id);
    if (!part) continue;
    const b = orientedBounds(part, placement.transform);
    const [x, y] = placement.transform.translation;
    const previous = boxes.get(placement.sheet_id) ?? [Infinity, Infinity, -Infinity, -Infinity];
    boxes.set(placement.sheet_id, [Math.min(previous[0], b[0] + x), Math.min(previous[1], b[1] + y),
      Math.max(previous[2], b[2] + x), Math.max(previous[3], b[3] + y)]);
  }
  cached.set(layout, boxes);
  return boxes;
}

/** Transform a cached downward-Y part path into downward-Y sheet coordinates. */
export function svgMatrix(t: Transform, height: number): [number, number, number, number, number, number] {
  const c = Math.cos(t.rotation_radians), s = Math.sin(t.rotation_radians), m = t.mirrored ? -1 : 1;
  return [c * m, -s * m, s, c, t.translation[0], height - t.translation[1]];
}
