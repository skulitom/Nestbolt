import { expect, test } from '@playwright/test';
import { readFileSync } from 'node:fs';

const svg = readFileSync(new URL('../../crates/core/tests/fixtures/viewport.svg', import.meta.url), 'utf8');
const dxf = readFileSync(new URL('../../crates/core/tests/fixtures/polyline-width.dxf', import.meta.url));

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
