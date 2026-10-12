import type { Layout, Library, NestRequest, Point, Polygon, Transform } from './types';

const PALETTE = ['#4e79a7', '#f28e2b', '#59a14f', '#e15759', '#76b7b2', '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac'];

function apply(t: Transform, [x, y]: Point): Point {
  const px = t.mirrored ? -x : x;
  const c = Math.cos(t.rotation_radians);
  const s = Math.sin(t.rotation_radians);
  return [c * px - s * y + t.translation[0], s * px + c * y + t.translation[1]];
}

/** Path data in sheet coordinates (Y up), flipped to SVG's downward Y. */
export function pathData(polygon: Polygon, t: Transform | null, height: number): string {
  const ring = (points: Point[]) =>
    points
      .map((p, i) => {
        const [x, y] = t ? apply(t, p) : p;
        return `${i ? 'L' : 'M'}${x.toFixed(3)} ${(height - y).toFixed(3)}`;
      })
      .join(' ') + ' Z';
  return [polygon.outer, ...polygon.holes].map(ring).join(' ');
}

function stockOf(request: NestRequest, layout: Layout, sheet: string) {
  const stockId = layout.sheets.find((s) => s.id === sheet)?.stock_id;
  const index = Number(stockId?.replace('sheet-type-', '')) - 1;
  return request.sheets[Number.isFinite(index) ? index : 0] ?? request.sheets[0];
}

/** The box around a sheet's placed parts and the clear offcut above them, in mm. */
export function sheetUsage(library: Library, request: NestRequest, layout: Layout, sheet: string) {
  const stock = stockOf(request, layout, sheet);
  const polygons = new Map(library.parts.map((p) => [p.id, p.polygon]));
  let [x0, y0, x1, y1] = [Infinity, Infinity, -Infinity, -Infinity];
  for (const p of layout.placements) {
    if (p.sheet_id !== sheet) continue;
    for (const point of polygons.get(p.part_id)?.outer ?? []) {
      const [x, y] = apply(p.transform, point);
      [x0, y0, x1, y1] = [Math.min(x0, x), Math.min(y0, y), Math.max(x1, x), Math.max(y1, y)];
    }
  }
  if (!Number.isFinite(x0)) return null;
  return { box: [x0, y0, x1, y1] as const, width: stock.width_mm, height: stock.height_mm,
    offcut: Math.max(0, stock.height_mm - y1) };
}

export function SheetPreview(props: { library: Library; request: NestRequest; layout: Layout; sheet: string }) {
  const { library, request, layout, sheet } = props;
  const stock = stockOf(request, layout, sheet);
  const width = stock.width_mm;
  const height = stock.height_mm;
  const color = new Map(library.parts.map((p, i) => [p.id, PALETTE[i % PALETTE.length]]));
  const polygons = new Map(library.parts.map((p) => [p.id, p.polygon]));
  const m = stock.margins_mm;
  const usage = sheetUsage(library, request, layout, sheet);
  return (
    <svg class="sheet" viewBox={`-1 -1 ${width + 2} ${height + 2}`} role="img" aria-label={`Layout of ${sheet}`}>
      {stock.outline_mm?.length
        ? stock.outline_mm.map((o, i) => <path key={`o${i}`} d={pathData(o, null, height)} class="stock" fill-rule="evenodd" />)
        : <rect x={0} y={0} width={width} height={height} class="stock" />}
      {(m.left || m.right || m.top || m.bottom) ? (
        <rect x={m.left} y={m.top} width={width - m.left - m.right} height={height - m.top - m.bottom} class="margin" />
      ) : null}
      {usage && usage.offcut > 0.01 * height ? (
        <rect x={0} y={0} width={width} height={usage.offcut} class="offcut"><title>{`Offcut ${width.toFixed(0)} × ${usage.offcut.toFixed(0)} mm`}</title></rect>
      ) : null}
      {stock.defects_mm.map((d, i) => <path key={`d${i}`} d={pathData(d, null, height)} class="defect" />)}
      {layout.placements
        .filter((p) => p.sheet_id === sheet)
        .map((p) => {
          const polygon = polygons.get(p.part_id);
          return polygon ? (
            <path key={`${p.part_id}#${p.copy_index}`} d={pathData(polygon, p.transform, height)}
              fill={color.get(p.part_id)} fill-rule="evenodd" class="part">
              <title>{`${p.part_id} #${p.copy_index + 1}`}</title>
            </path>
          ) : null;
        })}
      {usage ? (
        <rect x={usage.box[0]} y={height - usage.box[3]} width={usage.box[2] - usage.box[0]} height={usage.box[3] - usage.box[1]}
          class="extent"><title>Bounding box of the placed parts</title></rect>
      ) : null}
    </svg>
  );
}

export function PartThumb(props: { polygon: Polygon; color: string }) {
  const xs = props.polygon.outer.map((p) => p[0]);
  const ys = props.polygon.outer.map((p) => p[1]);
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const w = Math.max(x1 - x0, 1e-6);
  const h = Math.max(y1 - y0, 1e-6);
  const t: Transform = { translation: [-x0, -y0], rotation_radians: 0, mirrored: false };
  return (
    <svg class="thumb" viewBox={`0 0 ${w} ${h}`} aria-hidden="true">
      <path d={pathData(props.polygon, t, h)} fill={props.color} fill-rule="evenodd" />
    </svg>
  );
}

export { PALETTE };
