import { expect, test } from '@playwright/test';
import { layoutBounds, previewParts, svgMatrix } from '../src/preview-geometry.js';
import { zip } from '../src/zip.js';
import type { Layout, Library, Point, Polygon, Project, Transform } from '../src/types.js';

const frame: Polygon = { outer: [[-10.123456789, -5], [10, -5], [10, 5], [-10.123456789, 5]],
  holes: [[[-2, -1], [2, -1], [2, 1], [-2, 1]]] };
const island: Polygon = { outer: [[20, 0], [25, 0], [20, 4]], holes: [] };
const library = (): Library => ({ version: 1, tolerance: 0.01, warnings: [], parts: [{
  id: 'frame', source: 'authored-preview-fixture', polygon: frame, components: [frame, island],
  area_mm2: 203.23456789, bounds_mm: [-10.123456789, -5, 25, 5], holes: [],
}] });

// Direct vertex oracle, independent of the cache and SVG matrix representation.
const placedPoint = ([x, y]: Point, t: Transform): Point => {
  if (t.mirrored) x = -x;
  return [x * Math.cos(t.rotation_radians) - y * Math.sin(t.rotation_radians) + t.translation[0],
    x * Math.sin(t.rotation_radians) + y * Math.cos(t.rotation_radians) + t.translation[1]];
};
const vertexBounds = (lib: Library, layout: Layout, sheet: string) => {
  const points = layout.placements.filter(p => p.sheet_id === sheet).flatMap(p => {
    const part = lib.parts.find(q => q.id === p.part_id)!;
    return (part.components?.length ? part.components : [part.polygon]).flatMap(g => g.outer.map(v => placedPoint(v, p.transform)));
  });
  return [Math.min(...points.map(p => p[0])), Math.min(...points.map(p => p[1])),
    Math.max(...points.map(p => p[0])), Math.max(...points.map(p => p[1]))];
};
const near = (a: number[], b: readonly number[]) => a.forEach((v, i) => expect(Math.abs(v - b[i])).toBeLessThan(1e-9));

test('cached extents match all original vertices for free rotations, mirrors and changed snapshots', () => {
  const lib = library();
  // More distinct orientations than the bounded cache retains; revisit old ones.
  for (let i = 0; i < 320; i++) {
    const angle = i < 300 ? i * 0.03141592653589793 : (i - 300) * 0.03141592653589793;
    const layout: Layout = { version: 1, units: 'mm', sheets: [{ id: 'a', stock_id: 'sheet-type-1' }, { id: 'b', stock_id: 'sheet-type-1' }],
      placements: Array.from({ length: 8 }, (_, j) => ({ part_id: 'frame', copy_index: j, sheet_id: j % 2 ? 'b' : 'a',
        transform: { rotation_radians: angle, mirrored: !!(j % 3), translation: [30 * j - 90, 20 * j - 70] } })) };
    for (const sheet of ['a', 'b']) near(vertexBounds(lib, layout, sheet), layoutBounds(lib, layout).get(sheet)!);
    expect(layoutBounds(lib, layout).has('empty')).toBe(false);
    const changed = structuredClone(lib);
    changed.parts[0].components![1].outer[2] = [30, 40];
    for (const sheet of ['a', 'b']) near(vertexBounds(changed, layout, sheet), layoutBounds(changed, layout).get(sheet)!);
  }
});

test('cached paths retain every component and hole vertex without added rounding', () => {
  const lib = library();
  const path = previewParts(lib).get('frame')!.path;
  expect((path.match(/ Z/g) ?? []).length).toBe(3);
  const numbers = [...path.matchAll(/-?(?:\d*\.)?\d+(?:e[+-]?\d+)?/gi)].map(m => Number(m[0]));
  const points = [frame.outer, ...frame.holes, island.outer].flat();
  // SVG number text treats signed zero as the same coordinate.
  expect(numbers).toEqual(points.flatMap(([x, y]) => [x, -y]).map(v => v || 0));
  for (const mirrored of [false, true]) for (const angle of [0, Math.PI / 2, Math.PI, -0.73, 1.381]) {
    const transform: Transform = { translation: [87.123, 63.456], rotation_radians: angle, mirrored };
    const [a, b, c, d, e, f] = svgMatrix(transform, 300);
    for (const point of points) {
      const expected = placedPoint(point, transform);
      near([a * point[0] - c * point[1] + e, b * point[0] - d * point[1] + f], [expected[0], 300 - expected[1]]);
    }
  }
});

test('actual sheet previews keep references unique and render rotated mirrored multipart copies', async ({ page }) => {
  const lib = library();
  const layout: Layout = { version: 1, units: 'mm', sheets: [{ id: 'sheet-0', stock_id: 'sheet-type-1' }, { id: 'sheet-1', stock_id: 'sheet-type-1' }],
    placements: [0, 1, 2, 3].map(i => ({ part_id: 'frame', copy_index: i, sheet_id: `sheet-${Math.floor(i / 2)}`,
      transform: { rotation_radians: [0, Math.PI / 2, 0.371, -0.621][i], mirrored: !!(i % 2), translation: i % 2 ? [220, 220] : [80, 80] } })) };
  // An authored saved display fixture; solver validity is tested in the actual
  // nesting/export feature tests, rather than inferred from this fixture.
  const project: Project = { version: 1, name: 'Preview transforms', savedAt: '2026-10-15T00:00:00Z', library: lib,
    request: { parts: [{ id: 'frame', quantity: 4, rotations: { kind: 'free' }, allow_mirror: true, priority: 1 }],
      sheets: [{ width_mm: 300, height_mm: 300, count: null, margins_mm: { left: 5, right: 5, top: 5, bottom: 5 }, defects_mm: [] }],
      spacing_mm: 1, edge_spacing_mm: 1, mode: 'all' },
    result: { layout, seed: 0, seconds: 0, repeatable: false, parts_in_holes: 0,
      validation: { valid: true, violation_count: 0, violations: [], metrics: { sheets_used: 2, placed_parts: 4, requested_parts: 4,
        normalized_material: 2, utilization: 0.0045, material_area: 180000, placed_area: 812.93827156, placed_priority: 4 } } } };
  await page.goto('/');
  await page.locator('input[type=file][accept=".zip"]').setInputFiles({ name: 'preview.zip', mimeType: 'application/zip',
    buffer: Buffer.from(zip([{ name: 'project.json', data: JSON.stringify(project) }])) });
  await expect(page.locator('.summary')).toContainText('4/4');
  await expect(page.locator('svg.sheet use.part')).toHaveCount(4);
  const rendered = await page.locator('svg.sheet').evaluateAll(sheets => sheets.map(svg => ({
    definitions: Array.from(svg.querySelectorAll('defs path')).map(p => ({ id: p.id, path: p.getAttribute('d') })),
    copies: Array.from(svg.querySelectorAll<SVGUseElement>('use.part')).map(use => {
      const m = use.transform.baseVal.consolidate()!.matrix;
      return { href: use.getAttribute('href'), title: use.querySelector('title')?.textContent,
        matrix: [m.a, m.b, m.c, m.d, m.e, m.f], fillRule: getComputedStyle(use).fillRule };
    }),
    extent: ['x', 'y', 'width', 'height'].map(a => Number(svg.querySelector('.extent')?.getAttribute(a))),
  })));
  expect(new Set(rendered.flatMap(s => s.definitions.map(d => d.id))).size).toBe(2);
  for (let i = 0; i < 2; i++) {
    expect(rendered[i].definitions).toHaveLength(1);
    expect(rendered[i].definitions[0].path).toContain('-10.123456789');
    const bounds = vertexBounds(lib, layout, `sheet-${i}`);
    near(rendered[i].extent, [bounds[0], 300 - bounds[3], bounds[2] - bounds[0], bounds[3] - bounds[1]]);
    for (let j = 0; j < 2; j++) {
      const copy = rendered[i].copies[j], placement = layout.placements[i * 2 + j];
      expect(copy.href).toBe(`#${rendered[i].definitions[0].id}`);
      expect(copy.title).toBe(`frame #${i * 2 + j + 1}`);
      expect(copy.fillRule).toBe('evenodd');
      // DOM SVG matrices are float32 in some engines; allow only their rounding.
      const [a, b, c, d, e, f] = copy.matrix;
      for (const point of [...frame.outer, ...island.outer]) {
        const expected = placedPoint(point, placement.transform);
        expect(Math.abs(a * point[0] - c * point[1] + e - expected[0])).toBeLessThan(1e-5);
        expect(Math.abs(b * point[0] - d * point[1] + f - (300 - expected[1]))).toBeLessThan(1e-5);
      }
    }
  }
});
