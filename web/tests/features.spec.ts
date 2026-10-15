import { expect, test, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { zip } from '../src/zip.js';
import type { Project } from '../src/types.js';

// One end-to-end test per v1 feature through the browser app (the CLI has the
// same set in crates/cli/tests/features.rs). examples/parts.svg imports as
// parts-1 frame (80 x 60, 60 x 40 window), parts-2 washer (24 mm), parts-3
// bracket and parts-4 elliptical tab.
const example = (name: string) => fileURLToPath(new URL(`../../examples/${name}`, import.meta.url));
const fixture = (name: string) => fileURLToPath(new URL(`./fixtures/${name}`, import.meta.url));

type Layout = { sheets: { id: string; stock_id: string }[];
  placements: { part_id: string; transform: { rotation_radians: number; mirrored: boolean } }[] };
type ProjectFile = { request: { quick_start?: boolean; common_line?: { kerf_mm: number; search_bonus?: boolean }; spacing_mm: number; edge_spacing_mm: number; sheets: { count?: number | null }[] };
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
  // A result or an error, whichever comes first; an error fails with its own text.
  await expect(page.locator('.summary, .error').first()).toBeVisible({ timeout: 90_000 });
  if (await page.locator('.error').count()) throw new Error(`nesting failed: ${await page.locator('.error').innerText()}`);
  await expect(page.locator('.summary')).toContainText('valid');
}

const metric = async (page: Page, name: string) =>
  Number(await page.locator('.summary div', { hasText: name }).locator('dd').innerText());

test('lead allowances expose flags, reserve offcuts and export a separate review layer', async ({ page }, testInfo) => {
  const source = fileURLToPath(new URL('../../crates/core/tests/fixtures/leads.svg', import.meta.url));
  const sheet = await setUp(page, [source], { 'leads-1': 2 }, 60, 35, 1);
  await sheet.getByLabel('Margin').fill('0');
  await page.getByLabel('Lead-in allowances', { exact: true }).check();
  await expect(page.getByRole('button', { name: 'Nest', exact: true })).toBeDisabled();
  await page.getByLabel('Lead kerf').fill('0.2');
  await page.getByLabel('Lead length').fill('0.4');
  await expect(page.getByRole('button', { name: 'Nest', exact: true })).toBeDisabled();
  await page.getByLabel('Lead length').fill('3');
  await page.getByLabel('Outer lead angle').fill('45.001');
  await expect(page.getByRole('button', { name: 'Nest', exact: true })).toBeDisabled();
  await page.getByLabel('Outer lead angle').fill('45');
  await page.getByLabel('Lead style').selectOption('arc');
  await page.getByRole('button', { name: 'Nest', exact: true }).click();
  await expect(page.locator('.lead-report')).toContainText('4/6 contours have checked space', { timeout: 90_000 });
  await expect(page.locator('.lead-report')).toContainText('2 need manual attention');
  await expect(page.locator('.lead-preview')).toHaveCount(4);
  expect(await page.locator('svg.sheet').first().evaluate(el => el.getBoundingClientRect().height)).toBeGreaterThan(150);
  await expect(page.locator('[role=alert]')).toHaveCount(0);
  const [archive] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Project ZIP' }).click()]);
  const saved = JSON.parse(zipEntry(await archive.path(), 'project.json'));
  expect(saved.request.lead_in.style).toBe('arc');
  expect(saved.result.validation.metrics.placed_area).toBeCloseTo(391.68, 5);
  expect(saved.result.lead_in.validation.valid).toBe(true);
  expect(saved.result.lead_in.validation.source_checked).toBe(true);
  expect(saved.result.lead_in.validation.coverage).toEqual({ expected_contours: 6, reserved_contours: 4, flagged_contours: 2 });
  expect(saved.result.lead_in.parts.flatMap((p: { reservations: { shortened: boolean }[] }) => p.reservations).filter((r: { shortened: boolean }) => r.shortened)).toHaveLength(2);
  await expect(page.locator('.lead-report')).toContainText('1.2 mm lead.');
  const svg = zipEntry(await archive.path(), `sheets/${saved.result.layout.sheets[0].id}.svg`);
  expect(svg).toContain('id="LEADIN"');expect(svg).toContain('stroke="#ff0000"');
  const dxf = zipEntry(await archive.path(), `sheets/${saved.result.layout.sheets[0].id}.dxf`);
  expect(dxf).toContain('LEADIN');
  await testInfo.attach('lead-project', { body: JSON.stringify(saved), contentType: 'application/json' });
  await testInfo.attach('lead-controls', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  await page.locator('.results').evaluate(el => el.scrollTo(0, el.scrollHeight));
  await testInfo.attach('lead-preview', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  await page.getByLabel('Common-line cutting', { exact: true }).check();
  await page.getByLabel('Kerf mm', { exact: true }).fill('0.3');
  await expect(page.getByLabel('Lead kerf')).toHaveValue('0.3');
  await page.getByLabel('Lead-in allowances', { exact: true }).uncheck();
  await expect(page.locator('.lead-report')).toHaveCount(0);
});

for (const bonus of [false, true]) {
test(`common-line kerf overrides spacing and exports its own compensated layer (bonus ${bonus})`, async ({ page }, testInfo) => {
  const source = fileURLToPath(new URL('../../crates/core/tests/fixtures/common-panels.svg', import.meta.url));
  const sheet = await setUp(page, [source], { 'common-panels-1': 2 }, 86, 36, 1);
  await sheet.getByLabel('Margin').fill('0');
  await page.getByLabel('Repeatable', { exact: true }).check();
  await page.getByLabel('Part spacing').fill('5');
  await page.getByLabel('Common-line cutting', { exact: true }).check();
  await expect(page.getByRole('button', { name: 'Nest', exact: true })).toBeDisabled();
  await expect(page.getByLabel('Search for more shared cuts')).not.toBeChecked();
  if (bonus) await page.getByLabel('Search for more shared cuts').check();
  await page.getByLabel('Kerf mm', { exact: true }).fill('0.2');
  await expect(page.getByLabel('Search for more shared cuts')).toBeChecked({ checked: bonus });
  await expect(page.getByLabel('Part spacing')).toBeDisabled();
  await expect(page.getByLabel('Part spacing')).toHaveValue('0.2');
  await nest(page);
  const saved = await project(page);
  expect(!!saved.request.common_line?.search_bonus).toBe(bonus);
  await testInfo.attach('common-line-project', { body: JSON.stringify(saved), contentType: 'application/json' });
  await expect(page.locator('.common-line-report')).toContainText('30.0 mm saved');
  const [archive] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Download all sheets (ZIP)' }).click()]);
  const svg = zipEntry(await archive.path(), `sheets/${saved.result.layout.sheets[0].id}.svg`);
  expect(svg).toContain('id="COMMON"');
  expect(svg).toContain('stroke="#0000ff"');
  await page.getByLabel('Common-line cutting', { exact: true }).uncheck();
  await expect(page.getByLabel('Part spacing')).toHaveValue('5');
  await expect(page.locator('.common-line-report')).toHaveCount(0);
});
}

test('quick initial layout is optional and survives project export and reopening', async ({ page }) => {
  await setUp(page, [example('parts.svg')], { 'parts-3': 8 }, 300, 150, 1);
  const quick = page.getByLabel('Quick initial layout', { exact: true });
  await expect(quick).not.toBeChecked();
  await quick.check();
  await page.getByLabel('Repeatable', { exact: true }).check();
  await nest(page);
  await expect(page.locator('.summary')).toContainText('8/8');
  const saved = await project(page);
  expect(saved.request.quick_start).toBe(true);
  expect(saved.result.validation.valid).toBe(true);
  const [archive] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Project ZIP', exact: true }).click()]);
  const path = await archive.path();
  expect(zipEntry(path, `sheets/${saved.result.layout.sheets[0].id}.svg`)).toContain('<svg');
  await page.getByRole('button', { name: 'New', exact: true }).click();
  await page.locator('input[type=file][accept=".zip"]').setInputFiles(path);
  await expect(quick).toBeChecked();
  await expect(page.locator('.summary')).toContainText('8/8');
  await quick.uncheck();
  expect((await project(page)).request.quick_start).toBeUndefined();
});

test('background archives keep individual cutting files and release their workers', async ({ page }) => {
  await setUp(page, [example('parts.svg')], { 'parts-3': 8 }, 300, 150, 1);
  await page.getByLabel('Quick initial layout', { exact: true }).check();
  await nest(page);
  const saved = await project(page);
  const sheet = saved.result.layout.sheets[0].id;
  const baseline: Record<string, string> = {};
  for (const format of ['SVG', 'DXF']) {
    const [file] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: format, exact: true }).first().click()]);
    baseline[format.toLowerCase()] = readFileSync(await file.path(), 'utf8');
  }
  for (const name of ['Project ZIP', 'Download all sheets (ZIP)']) {
    const [file] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name, exact: true }).click()]);
    const path = await file.path();
    for (const format of ['svg', 'dxf']) expect(zipEntry(path, `sheets/${sheet}.${format}`)).toBe(baseline[format]);
    if (name === 'Project ZIP') expect(JSON.parse(zipEntry(path, 'project.json')).result.validation.valid).toBe(true);
    else expect(() => zipEntry(path, 'project.json')).toThrow();
    // Only the existing import/individual-export utility remains alive.
    await expect.poll(() => page.workers().length).toBe(1);
  }
});

test('a rejected archive reports the validation error and releases its worker', async ({ page }) => {
  await setUp(page, [example('parts.svg')], { 'parts-3': 1 }, 300, 150, 1);
  await page.getByLabel('Quick initial layout', { exact: true }).check();
  await nest(page);
  const saved = await project(page) as unknown as Project;
  saved.result!.layout.placements[0].transform.translation = [-1000, -1000];
  await page.locator('input[type=file][accept=".zip"]').setInputFiles({ name: 'invalid-layout.zip', mimeType: 'application/zip',
    buffer: Buffer.from(zip([{ name: 'project.json', data: JSON.stringify(saved) }])) });
  let downloads = 0;
  page.on('download', () => downloads++);
  await page.getByRole('button', { name: 'Project ZIP', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('layout failed independent validation');
  await expect.poll(() => page.workers().length).toBe(1);
  expect(downloads).toBe(0);
});

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

test('a prearranged drawing keeps CUT parts separate from its SHEET boundary', async ({ page }) => {
  const source = fileURLToPath(new URL('../../crates/core/tests/fixtures/prearranged-sheet.svg', import.meta.url));
  const sheet = await setUp(page, [source], { 'prearranged-sheet-1': 1, 'prearranged-sheet-2': 1 }, 600, 400, 1);
  await expect(page.locator('table.parts tbody tr')).toHaveCount(2);
  await sheet.getByLabel('Imported sheet outline for sheet size 1').selectOption('prearranged-sheet-sheet-1');
  await expect(sheet.getByLabel('Width')).toHaveValue('200');
  await expect(sheet.getByLabel('Height')).toHaveValue('100');
  await sheet.getByLabel('Count').fill('1');
  await nest(page);
  await expect(page.locator('.summary')).toContainText('2/2');
  await expect(page.locator('svg.sheet path.stock')).toHaveCount(1);
  // The stock-file picker also prefers SHEET, even though CUT is the normal
  // part-selection default for this same drawing.
  await sheet.getByRole('button', { name: 'Use the full rectangle for sheet size 1' }).click();
  await sheet.getByLabel('Width').fill('600');
  await sheet.getByLabel('Remnant outline for sheet size 1').setInputFiles(source);
  await expect(sheet.getByLabel('Width')).toHaveValue('200');
  await expect(sheet.getByLabel('Height')).toHaveValue('100');
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
