import { expect, test } from '@playwright/test';
import { readFileSync } from 'node:fs';
import type { Project } from '../src/types.js';
import { unzip } from '../src/zip.js';

const svg = readFileSync(new URL('../../crates/core/tests/fixtures/viewport.svg', import.meta.url), 'utf8');
const dxf = readFileSync(new URL('../../crates/core/tests/fixtures/polyline-width.dxf', import.meta.url));

test('a hole drawn in inches matches the browser SVG geometry', async ({ page }) => {
  const source = readFileSync(new URL('../../crates/core/tests/fixtures/inch-hole.svg', import.meta.url), 'utf8');
  await page.setContent(source);
  const expected = await page.locator('circle').evaluate(element => {
    const { x, y, width, height } = (element as SVGCircleElement).getBBox();
    return [x, -y - height, x + width, -y].map(px => px * 25.4 / 96);
  });
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles({ name: 'inch-hole.svg', mimeType: 'image/svg+xml', buffer: Buffer.from(source) });
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  const [archive] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Project ZIP' }).click()]);
  const entries = unzip(readFileSync(await archive.path()));
  const project: Project = JSON.parse(new TextDecoder().decode(entries.get('project.json')));
  const holes = project.library!.parts[0].polygon.holes;
  expect(holes).toHaveLength(1);
  const xs = holes[0].map(p => p[0]), ys = holes[0].map(p => p[1]);
  const measured = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
  measured.forEach((value, i) => expect(Math.abs(value - expected[i])).toBeLessThan(0.005));
});

test('SVG page geometry agrees with browser coordinates and width warnings are visible', async ({ page }) => {
  // An independent browser matrix oracle: the root transform is in outer
  // viewport pixels, while the nonuniform viewBox sets the part dimensions.
  await page.setContent(`<style>body{margin:0}</style>${svg}`);
  const bounds = await page.locator('rect').evaluate((element) => {
    const shape = element as SVGRectElement;
    const b = shape.getBBox(), m = shape.getScreenCTM()!;
    const points = [[b.x,b.y],[b.x+b.width,b.y],[b.x+b.width,b.y+b.height],[b.x,b.y+b.height]]
      .map(([x,y]) => new DOMPoint(x,y).matrixTransform(m))
      .map((p) => [p.x * 25.4 / 96, -p.y * 25.4 / 96]);
    return [Math.min(...points.map(p=>p[0])),Math.min(...points.map(p=>p[1])),Math.max(...points.map(p=>p[0])),Math.max(...points.map(p=>p[1]))];
  });
  // Browser CSS layout rounds page dimensions: Chromium reports 65.399212 mm
  // for the exact 65.4 mm edge. Allow 0.005 mm only for this independent
  // rendering oracle; the native bounds checks retain 1e-9 mm precision.
  [65.4,-62.7,85.4,-42.7].forEach((v,i) => expect(Math.abs(bounds[i]-v)).toBeLessThan(0.005));
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles([
    { name: 'viewport.svg', mimeType: 'image/svg+xml', buffer: Buffer.from(svg) },
    { name: 'width.dxf', mimeType: 'application/dxf', buffer: dxf },
  ]);
  await expect(page.locator('table.parts tbody tr')).toHaveCount(2);
  await expect(page.locator('table.parts tbody tr').filter({ hasText: 'viewport-1' })).toContainText('4.0 cm²');
  await expect(page.locator('table.parts tbody tr').filter({ hasText: 'width-1' })).toContainText('0.5 cm²');
  await expect(page.locator('.warnings')).toContainText('polyline widths ignored; importing the centreline');
});
