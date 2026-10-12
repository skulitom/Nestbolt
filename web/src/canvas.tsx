import { useEffect, useMemo, useRef } from 'preact/hooks';
import { PALETTE, sheetUsage } from './preview';
import type { Layout, Library, NestRequest, Point } from './types';

const ring = (path: Path2D, points: Point[]) => {
  points.forEach(([x, y], i) => (i ? path.lineTo(x, y) : path.moveTo(x, y)));
  path.closePath();
};

/**
 * The live preview: one sheet drawn on a canvas from cached part paths, so a
 * 2,000-part layout redraws in a few milliseconds and the page stays
 * responsive while the workers search. Final results use the SVG preview.
 */
export function SheetCanvas(props: { library: Library; request: NestRequest; layout: Layout; sheet: string }) {
  const { library, request, layout, sheet } = props;
  const canvas = useRef<HTMLCanvasElement>(null);
  const paths = useMemo(() => new Map(library.parts.map((p, i) => {
    const path = new Path2D();
    for (const r of [p.polygon.outer, ...p.polygon.holes]) ring(path, r);
    return [p.id, { path, color: PALETTE[i % PALETTE.length] }];
  })), [library]);
  const usage = sheetUsage(library, request, layout, sheet);
  const width = usage?.width ?? request.sheets[0].width_mm;
  const height = usage?.height ?? request.sheets[0].height_mm;
  useEffect(() => {
    const c = canvas.current;
    const ctx = c?.getContext('2d');
    if (!c || !ctx) return;
    const pixels = Math.min(1600, Math.round((c.clientWidth || 600) * (window.devicePixelRatio || 1)));
    const scale = pixels / width;
    c.width = pixels;
    c.height = Math.round(height * scale);
    const style = getComputedStyle(c);
    // Sheet coordinates have Y up: flip once for the whole drawing.
    ctx.setTransform(scale, 0, 0, -scale, 0, c.height);
    ctx.fillStyle = style.getPropertyValue('--stock') || '#efe8d8';
    ctx.fillRect(0, 0, width, height);
    if (usage && usage.offcut > 0.01 * height) {
      ctx.fillStyle = style.getPropertyValue('--offcut') || 'rgba(89,161,79,0.18)';
      ctx.fillRect(0, height - usage.offcut, width, usage.offcut);
    }
    ctx.lineWidth = 1 / scale;
    ctx.strokeStyle = 'rgba(0,0,0,0.45)';
    for (const p of layout.placements) {
      if (p.sheet_id !== sheet) continue;
      const part = paths.get(p.part_id);
      if (!part) continue;
      const t = p.transform;
      const [c0, s0] = [Math.cos(t.rotation_radians), Math.sin(t.rotation_radians)];
      const m = t.mirrored ? -1 : 1;
      ctx.save();
      ctx.transform(c0 * m, s0 * m, -s0, c0, t.translation[0], t.translation[1]);
      ctx.fillStyle = part.color;
      ctx.fill(part.path, 'evenodd');
      ctx.stroke(part.path);
      ctx.restore();
    }
    if (usage) {
      const [x0, y0, x1, y1] = usage.box;
      ctx.setLineDash([5 / scale, 4 / scale]);
      ctx.strokeStyle = style.getPropertyValue('--accent') || '#2f6db5';
      ctx.strokeRect(x0, y0, x1 - x0, y1 - y0);
      ctx.setLineDash([]);
    }
  }, [layout, sheet, paths, width, height]);
  return <canvas ref={canvas} class="sheet live-sheet" role="img" aria-label={`Live layout of ${sheet}`} />;
}

