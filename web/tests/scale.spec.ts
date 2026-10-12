import { expect, test } from '@playwright/test';
import { statSync, writeFileSync } from 'node:fs';

// G5 scale: a 2,000-part job imports, solves and exports in the app as shipped
// (default workers). Runs only with SCALE_SVG; scripts/g5_scale.py sets it,
// samples the browser's memory from outside and writes the report.
const svg = process.env.SCALE_SVG;
const seconds = process.env.SCALE_SECONDS ?? '60';

test('a 2,000-part job imports, nests and exports', async ({ page }) => {
  test.skip(!svg, 'SCALE_SVG not set');
  test.setTimeout(20 * 60_000);
  await page.addInitScript(() => {
    const w = window as unknown as { longTasks: [number, number][] };
    w.longTasks = [];
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) w.longTasks.push([e.startTime, e.duration]);
    }).observe({ type: 'longtask', buffered: true });
  });
  const marks: Record<string, number> = {};
  const mark = async (name: string) => { marks[name] = await page.evaluate(() => performance.now()); };
  await page.goto('/');
  await mark('import_start');
  await page.locator('.drop input[type=file]').setInputFiles(svg!);
  const rows = page.locator('table.parts tbody tr');
  await expect(rows).toHaveCount(4, { timeout: 60_000 });
  await mark('import_done');
  for (let i = 0; i < 4; i++) await rows.nth(i).locator('input[type=number]').first().fill('500');
  const sheet = page.locator('fieldset.sheet-row').first();
  await sheet.getByLabel('Width').fill('1250');
  await sheet.getByLabel('Height').fill('2500');
  await page.getByLabel('Part spacing').fill('1.5');
  await page.getByLabel('Edge spacing').fill('1.5');
  await page.getByLabel('Time').fill(seconds);
  await mark('nest_start');
  await page.getByRole('button', { name: 'Nest' }).click();
  await expect(page.locator('.summary')).toContainText('2000/2000', { timeout: 10 * 60_000 });
  await mark('nest_done');
  await expect(page.locator('.summary')).toContainText('valid');
  const summary = await page.locator('.summary').innerText();
  await mark('export_start');
  const [archive] = await Promise.all([page.waitForEvent('download', { timeout: 10 * 60_000 }),
    page.getByRole('button', { name: 'Download all sheets (ZIP)' }).click()]);
  const zipPath = await archive.path();
  await mark('export_done');
  const zipBytes = statSync(zipPath).size;
  expect(zipBytes).toBeGreaterThan(1000);
  const tasks = await page.evaluate(() => (window as unknown as { longTasks: [number, number][] }).longTasks);
  const during = (a: string, b: string) => Math.max(0, ...tasks.filter(([t]) => t >= marks[a] && t <= marks[b]).map(([, d]) => d));
  const report = {
    browser: test.info().project.name, summary, zip_bytes: zipBytes, marks,
    import_seconds: (marks.import_done - marks.import_start) / 1000,
    nest_seconds: (marks.nest_done - marks.nest_start) / 1000,
    export_seconds: (marks.export_done - marks.export_start) / 1000,
    longest_task_while_solving_ms: during('nest_start', 'nest_done'),
    longest_task_ms: Math.max(0, ...tasks.map(([, d]) => d)), long_tasks: tasks.length,
  };
  if (process.env.SCALE_OUT) writeFileSync(process.env.SCALE_OUT, JSON.stringify(report, null, 1));
});
