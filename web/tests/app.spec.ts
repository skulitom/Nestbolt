import { expect, test, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const parts = fileURLToPath(new URL('../../examples/parts.svg', import.meta.url));

async function importAndConfigure(page: Page) {
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles(parts);
  await expect(page.locator('table.parts tbody tr')).toHaveCount(4);
  await page.getByLabel('Quantity of parts-2').fill('6');
  await page.getByLabel('Rotations of parts-2').selectOption('Free');
  await page.getByLabel('Allow mirroring parts-3').check();
  const sheet = page.locator('fieldset.sheet-row').first();
  await sheet.getByLabel('Width').fill('300');
  await sheet.getByLabel('Height').fill('200');
  await page.getByLabel('Time').fill('5');
  await page.getByText('Advanced').click();
  await page.getByLabel('Workers').fill('1');
}

test('import, nest, export and keep the main thread responsive', async ({ page }) => {
  await page.addInitScript(() => {
    (window as unknown as { longTasks: number[] }).longTasks = [];
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) (window as unknown as { longTasks: number[] }).longTasks.push(e.duration);
    }).observe({ type: 'longtask', buffered: true });
  });
  await importAndConfigure(page);
  await page.getByRole('button', { name: 'Nest' }).click();
  await expect(page.getByLabel('Search progress')).toBeVisible();
  await expect(page.locator('.summary')).toBeVisible({ timeout: 60_000 });
  await expect(page.locator('.summary')).toContainText('valid');
  await expect(page.locator('.summary')).toContainText('9/9');
  const sheets = page.locator('svg.sheet');
  expect(await sheets.count()).toBeGreaterThanOrEqual(1);
  await expect(sheets.first().locator('path.part')).toHaveCount(9);

  const [svg] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'SVG', exact: true }).first().click()]);
  expect(readFileSync(await svg.path(), 'utf8')).toContain('<svg');
  const [dxf] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'DXF', exact: true }).first().click()]);
  expect(readFileSync(await dxf.path(), 'utf8')).toContain('ENTITIES');

  const notices = await page.request.get('/THIRD_PARTY_NOTICES.txt');
  expect(await notices.text()).toContain('## preact');

  // Firefox has no longtask entries; Chromium's must all stay under 200 ms.
  const longest = await page.evaluate(() => Math.max(0, ...(window as unknown as { longTasks: number[] }).longTasks));
  expect(longest).toBeLessThan(200);
});

test('the example boxes import and nest in one click', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Try an example: two finger-jointed boxes' }).click();
  await expect(page.locator('table.parts tbody tr')).toHaveCount(6);
  await expect(page.locator('.summary')).toContainText('12/12', { timeout: 60_000 });
  await expect(page.locator('.summary')).toContainText('valid');
});

test("a loading state, then a live view in the sheet's proportions, in a window that does not scroll", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/');
  await page.getByRole('button', { name: 'Try an example: a mechanical kit' }).click();
  await expect(page.locator('.pending .sheet-skeleton')).toBeVisible();
  const canvas = page.locator('canvas.live-sheet').first();
  await expect(canvas).toBeVisible({ timeout: 60_000 });
  // A 1220 x 2440 mm sheet is drawn twice as tall as it is wide, never stretched.
  const box = (await canvas.boundingBox())!;
  expect(Math.abs(box.height / box.width - 2)).toBeLessThan(0.02);
  expect(await page.evaluate(() => document.documentElement.scrollHeight - innerHeight)).toBeLessThanOrEqual(0);
  await page.getByRole('button', { name: 'Cancel' }).click();
  await expect(page.getByRole('alert')).toContainText('Cancelled');
});

test('projects save to the browser and to a ZIP', async ({ page }) => {
  await importAndConfigure(page);
  await page.getByLabel('Project name').fill('Bracket run');
  await page.getByRole('button', { name: 'Save', exact: true }).click();
  const [archive] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Project ZIP' }).click()]);
  const zipPath = await archive.path();

  await page.reload();
  await page.getByLabel('Open saved project').selectOption('Bracket run');
  await expect(page.getByLabel('Quantity of parts-2')).toHaveValue('6');

  await page.getByRole('button', { name: 'New' }).click();
  await expect(page.locator('table.parts tbody tr')).toHaveCount(0);
  await page.locator('input[type=file][accept=".zip"]').setInputFiles(zipPath);
  await expect(page.getByLabel('Project name')).toHaveValue('Bracket run');
  await expect(page.locator('table.parts tbody tr')).toHaveCount(4);
});

test('defects, several sheet sizes and fill mode reach the solver', async ({ page }) => {
  await importAndConfigure(page);
  const sheet = page.locator('fieldset.sheet-row').first();
  await sheet.locator('summary').click();
  for (const [k, v] of [['x', '120'], ['y', '60'], ['w', '40'], ['h', '40']]) await sheet.getByLabel(`Defect ${k}`).fill(v);
  await sheet.getByRole('button', { name: 'Add defect' }).click();
  await expect(sheet.locator('summary')).toContainText('Defects (1)');
  await page.getByLabel('Add a sheet size').selectOption('Diode laser 300×200');
  await expect(page.locator('fieldset.sheet-row')).toHaveCount(2);
  await page.getByLabel('Goal').selectOption('fill_area');
  await page.getByRole('button', { name: 'Nest' }).click();
  await expect(page.locator('.summary')).toContainText('valid', { timeout: 60_000 });
  await expect(page.locator('svg.sheet path.defect').first()).toBeVisible();
});
