import { expect, test, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

// One end-to-end test per v1 feature through the browser app (the CLI has the
// same set in crates/cli/tests/features.rs). examples/parts.svg imports as
// parts-1 frame (80 x 60, 60 x 40 window), parts-2 washer (24 mm), parts-3
// bracket and parts-4 elliptical tab.
const example = (name: string) => fileURLToPath(new URL(`../../examples/${name}`, import.meta.url));
const fixture = (name: string) => fileURLToPath(new URL(`./fixtures/${name}`, import.meta.url));

type Layout = { sheets: { id: string; stock_id: string }[];
  placements: { part_id: string; transform: { rotation_radians: number; mirrored: boolean } }[] };
type ProjectFile = { request: { spacing_mm: number; edge_spacing_mm: number; sheets: { count?: number | null }[] };
  result: { layout: Layout; validation: { valid: boolean } } };

/** Read one entry of the app's stored (uncompressed) ZIP. */
function zipEntry(path: string, wanted: string): string {
  const bytes = readFileSync(path);
  for (let at = 0; bytes.readUInt32LE(at) === 0x04034b50;) {
    const size = bytes.readUInt32LE(at + 18);
    const nameLength = bytes.readUInt16LE(at + 26);
    const extra = bytes.readUInt16LE(at + 28);
    const name = bytes.subarray(at + 30, at + 30 + nameLength).toString('utf8');
    const start = at + 30 + nameLength + extra;
    if (name === wanted) return bytes.subarray(start, start + size).toString('utf8');
    at = start + size;
  }
  throw new Error(`${wanted} not in ${path}`);
}

async function project(page: Page): Promise<ProjectFile> {
  const [archive] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Project ZIP' }).click()]);
  return JSON.parse(zipEntry(await archive.path(), 'project.json'));
}

/** Import files, keep only the given parts with quantities, one sheet size, one worker. */
async function setUp(page: Page, files: string[], keep: Record<string, number>, w: number, h: number, seconds = 5) {
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles(files);
  await expect(page.locator('table.parts tbody tr').first()).toBeVisible();
  const ids = await page.getByRole('button', { name: /^Remove / }).evaluateAll((buttons) =>
    buttons.map((b) => b.getAttribute('aria-label')!.replace('Remove ', '')));
  for (const id of ids.filter((id) => !(id in keep))) {
    await page.getByRole('button', { name: `Remove ${id}`, exact: true }).click();
  }
  for (const [id, quantity] of Object.entries(keep)) await page.getByLabel(`Quantity of ${id}`).fill(String(quantity));
  const sheet = page.locator('fieldset.sheet-row').first();
  await sheet.getByLabel('Width').fill(String(w));
  await sheet.getByLabel('Height').fill(String(h));
  await page.getByLabel('Time').fill(String(seconds));
  await page.getByText('Advanced').click();
  await page.getByLabel('Workers').fill('1');
  return sheet;
}

async function nest(page: Page) {
  await page.getByRole('button', { name: 'Nest' }).click();
  await expect(page.locator('.summary')).toBeVisible({ timeout: 90_000 });
  await expect(page.locator('.summary')).toContainText('valid');
}

const metric = async (page: Page, name: string) =>
  Number(await page.locator('.summary div', { hasText: name }).locator('dd').innerText());

test('DXF and SVG import; exports keep arcs and curves', async ({ page }) => {
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles([example('fidelity/plate-in.dxf'), example('fidelity/curves-mm.svg')]);
  await expect(page.locator('table.parts tbody tr td[title*="plate-in.dxf"]').first()).toBeVisible();
  await expect(page.locator('table.parts tbody tr td[title*="curves-mm.svg"]').first()).toBeVisible();
  const sheet = page.locator('fieldset.sheet-row').first();
  await sheet.getByLabel('Width').fill('400');
  await sheet.getByLabel('Height').fill('300');
  await page.getByLabel('Time').fill('5');
  await page.getByText('Advanced').click();
  await page.getByLabel('Workers').fill('1');
  await nest(page);
  const [svg] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'SVG', exact: true }).first().click()]);
  expect(readFileSync(await svg.path(), 'utf8')).toMatch(/ [AC] /);
  const [dxf] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'DXF', exact: true }).first().click()]);
  expect(readFileSync(await dxf.path(), 'utf8')).toMatch(/\n(ARC|ELLIPSE)\r?\n/);
});

test('fewest sheets with margins; the last sheet keeps one offcut', async ({ page }) => {
  // 16 washers fit a 100 mm square, so 20 need two sheets.
  const sheet = await setUp(page, [example('parts.svg')], { 'parts-2': 20 }, 105, 105);
  await sheet.getByLabel('Margin').fill('2.5');
  await page.getByLabel('Edge spacing').fill('0');
  await nest(page);
  expect(await metric(page, 'Sheets')).toBe(2);
  expect(await metric(page, 'Material')).toBeLessThan(1.5);
  await expect(page.locator('.summary')).toContainText('20/20');
  await expect(page.locator('svg.sheet')).toHaveCount(2);
  await expect(page.locator('svg.sheet rect.margin').first()).toBeVisible();
});

test('a capped sheet count fails in place-all mode and fills by area or priority', async ({ page }) => {
  const sheet = await setUp(page, [example('parts.svg')], { 'parts-2': 40, 'parts-3': 2 }, 100, 100, 3);
  await sheet.getByLabel('Count').fill('1');
  await page.getByLabel('Edge spacing').fill('0');
  await page.getByRole('button', { name: 'Nest' }).click();
  await expect(page.getByRole('alert')).toBeVisible({ timeout: 90_000 });
  await page.getByLabel('Goal').selectOption('fill_area');
  await nest(page);
  const placed = (await page.locator('.summary div', { hasText: 'Placed' }).locator('dd').innerText()).split('/');
  expect(Number(placed[0])).toBeLessThan(42);
  expect(Number(placed[1])).toBe(42);
  await page.getByLabel('Goal').selectOption('fill_priority');
  await page.locator('table.parts tbody tr', { hasText: 'parts-3' }).locator('input[type=number]').nth(1).fill('10');
  await nest(page);
  const saved = await project(page);
  expect(saved.request.sheets[0].count).toBe(1);
  expect(saved.result.layout.placements.filter((p) => p.part_id === 'parts-3')).toHaveLength(2);
});

test('small parts are placed inside the holes of larger parts', async ({ page }) => {
  // The frame nearly fills the only sheet; the washers fit only in its window.
  const sheet = await setUp(page, [example('parts.svg')], { 'parts-1': 1, 'parts-2': 2 }, 90, 70, 3);
  await sheet.getByLabel('Margin').fill('0');
  await sheet.getByLabel('Count').fill('1');
  await nest(page);
  await expect(page.locator('.summary')).toContainText('3/3');
  expect(await metric(page, 'In holes')).toBeGreaterThanOrEqual(2);
});

test('a remnant outline from a drawing is used as the sheet', async ({ page }) => {
  const sheet = await setUp(page, [example('parts.svg')], { 'parts-4': 12 }, 600, 400);
  await sheet.getByLabel('Remnant outline for sheet size 1').setInputFiles(fixture('remnant-l.svg'));
  await expect(sheet.getByText('Remnant outline')).toBeVisible();
  await expect(sheet.getByLabel('Width')).toHaveValue('150');
  await expect(sheet.getByLabel('Height')).toHaveValue('150');
  await sheet.getByLabel('Count').fill('1');
  await nest(page);
  await expect(page.locator('.summary')).toContainText('12/12');
  await expect(page.locator('svg.sheet path.stock')).toHaveCount(1);
});

test('rotation lists, steps, free rotation, mirroring and spacing reach the solver', async ({ page }) => {
  await setUp(page, [example('parts.svg')], { 'parts-1': 1, 'parts-2': 4, 'parts-3': 4, 'parts-4': 6 }, 250, 200);
  await page.getByLabel('Rotations of parts-4').selectOption('0/180° (grain)');
  await page.getByLabel('Rotations of parts-3').selectOption('Every 15°');
  await page.getByLabel('Rotations of parts-2').selectOption('Free');
  await page.getByLabel('Rotations of parts-1').selectOption('Fixed 0°');
  await page.getByLabel('Allow mirroring parts-3').check();
  await page.getByLabel('Part spacing').fill('3');
  await page.getByLabel('Edge spacing').fill('4');
  await nest(page);
  await expect(page.locator('.summary')).toContainText('15/15');
  const saved = await project(page);
  expect(saved.request.spacing_mm).toBe(3);
  expect(saved.request.edge_spacing_mm).toBe(4);
  const onStep = (r: number, step: number) => {
    const k = r / ((step * Math.PI) / 180);
    return Math.abs(k - Math.round(k)) < 1e-6;
  };
  for (const p of saved.result.layout.placements) {
    const r = p.transform.rotation_radians;
    if (p.part_id === 'parts-4') expect(onStep(r, 180)).toBe(true);
    if (p.part_id === 'parts-3') expect(onStep(r, 15)).toBe(true);
    if (p.part_id === 'parts-1') expect(onStep(r, 360)).toBe(true);
    if (p.part_id !== 'parts-3') expect(p.transform.mirrored).toBe(false);
  }
});

test('hundreds of copies of a part', async ({ page }) => {
  await setUp(page, [example('parts.svg')], { 'parts-1': 1, 'parts-4': 300 }, 600, 400, 8);
  await nest(page);
  await expect(page.locator('.summary')).toContainText('301/301');
});
