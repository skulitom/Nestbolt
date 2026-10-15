import { expect, test } from '@playwright/test';
import { fileURLToPath } from 'node:url';
import { workersFor } from '../src/worker-policy.js';
import type { Library, LibraryPart, NestRequest, Point, Polygon } from '../src/types.js';

const circle = (count: number, radius: number): Point[] => Array.from({ length: count }, (_, i) =>
  [radius * Math.cos(i * 2 * Math.PI / count), radius * Math.sin(i * 2 * Math.PI / count)]);
const part = (id: string, polygon: Polygon, components?: Polygon[]): LibraryPart =>
  ({ id, source: 'authored worker-policy fixture', polygon, components, holes: [], area_mm2: 1, bounds_mm: [-20, -20, 20, 20] });
const library = (parts: LibraryPart[]): Library => ({ version: 1, tolerance: 0.005, warnings: [], parts });
const request = (id: string, quantity: number): NestRequest => ({ parts: [{ id, quantity,
  rotations: { kind: 'free' }, allow_mirror: false, priority: 1 }], sheets: [], spacing_mm: 1, edge_spacing_mm: 1, mode: 'all' });

test('complexity includes every component and hole, without counting unused parts or fallback polygons', () => {
  const frame = { outer: circle(1000, 10), holes: [circle(500, 2)] };
  const island = { outer: circle(500, 1).map(([x, y]): Point => [x + 15, y]), holes: [] };
  const lib = library([part('multi', { outer: circle(10_000, 20), holes: [] }, [frame, island]),
    part('unused', { outer: circle(10_000, 20), holes: [] })]);
  expect(workersFor(lib, request('multi', 200), 4)).toBe(4);
  expect(workersFor(lib, request('multi', 251), 4)).toBe(1);
  expect(workersFor(lib, request('multi', 251), 1)).toBe(1);
  expect(workersFor(lib, request('multi', 0), 4)).toBe(4);
});

test('simpler jobs retain their requested count and the existing high-quantity cap', () => {
  const lib = library([part('box', { outer: [[0, 0], [10, 0], [10, 10], [0, 10]], holes: [] })]);
  expect(workersFor(lib, request('box', 1000), 4)).toBe(4);
  expect(workersFor(lib, request('box', 2000), 4)).toBe(2);
  expect(workersFor(lib, request('box', 2000), 1)).toBe(1);
  expect(workersFor(lib, request('box', 1), 0)).toBe(1);
  expect(workersFor(lib, request('box', 1), Number.NaN)).toBe(1);
});

test('the actual app explains and launches one search worker for the curve-heavy job', async ({ page }) => {
  await page.addInitScript(() => Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 }));
  await page.goto('/');
  const svg = fileURLToPath(new URL('../../benchmarks/datasets/browser-curves/letters-gears-2000.svg', import.meta.url));
  await page.locator('.drop input[type=file]').setInputFiles(svg);
  const rows = page.locator('table.parts tbody tr');
  await expect(rows).toHaveCount(4);
  for (let i = 0; i < 4; i++) await rows.nth(i).locator('input[type=number]').first().fill('500');
  await page.getByText('Advanced', { exact: true }).click();
  await page.getByLabel('Workers', { exact: true }).fill('4');
  await expect(page.getByText('This drawing will use 1 worker to limit memory.', { exact: true })).toBeVisible();
  const spawned: string[] = [];
  page.on('worker', worker => spawned.push(worker.url()));
  await page.getByRole('button', { name: 'Nest', exact: true }).click();
  await expect.poll(() => spawned.length).toBe(1);
  await page.getByRole('button', { name: 'Cancel', exact: true }).click();
  await expect.poll(() => page.workers().length).toBe(1); // Only the import utility remains.
  for (let i = 0; i < 4; i++) await rows.nth(i).locator('input[type=number]').first().fill('1');
  await expect(page.getByText(/This drawing will use .* to limit memory/)).toHaveCount(0);
  expect(spawned).toHaveLength(1);
});
