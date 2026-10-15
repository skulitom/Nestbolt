// Actual public app workflow, with whole-pipeline responsiveness and saved ZIP.
// Driven by scripts/h4_scale.py; no product shortcuts or direct solver calls.
import { readFile, writeFile, stat } from 'node:fs/promises';
import { chromium, firefox, expect } from '@playwright/test';

const plan = JSON.parse(await readFile(process.argv[2], 'utf8'));
const engine = plan.browser === 'firefox' ? firefox : chromium;
const browser = await engine.launch({ headless: true,
  ...(plan.browser === 'chrome' ? { channel: 'chrome' } : {}) });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, acceptDownloads: true });
const page = await context.newPage();
page.setDefaultTimeout(30_000);
const record = { browser: plan.browser, version: browser.version(), status: 'running', marks: {}, console_errors: [], worker_events: [], maximum_workers: 0 };
const activeWorkers = new Set();
page.on('worker', worker => {
  const event = { url: worker.url(), opened_at_ms: Date.now() };
  record.worker_events.push(event);
  activeWorkers.add(worker);
  record.maximum_workers = Math.max(record.maximum_workers, activeWorkers.size);
  worker.on('close', () => { event.closed_at_ms = Date.now(); activeWorkers.delete(worker); });
});
page.on('pageerror', error => record.console_errors.push(String(error)));
await context.route('**/*', route => {
  const url = new URL(route.request().url());
  return url.origin === new URL(plan.url).origin ? route.continue() : route.abort();
});
await page.addInitScript(() => {
  const stats = window.h4Stats = { long_tasks: [], event_loop_gaps: [],
    long_tasks_supported: PerformanceObserver.supportedEntryTypes.includes('longtask') };
  if (stats.long_tasks_supported) new PerformanceObserver(list => {
    for (const entry of list.getEntries()) stats.long_tasks.push([entry.startTime, entry.duration]);
  }).observe({ type: 'longtask', buffered: true });
  let previous = performance.now();
  const tick = () => {
    const now = performance.now();
    stats.event_loop_gaps.push([previous, now - previous]);
    previous = now;
    setTimeout(tick, 20);
  };
  setTimeout(tick, 20);
});
const mark = async name => {
  record.marks[name] = await page.evaluate(() => performance.now());
  await writeFile(`${plan.out}/progress.json`, JSON.stringify({ phase: name, ...record }, null, 2));
  console.log(JSON.stringify({ phase: name }));
};
try {
  await page.goto(plan.url);
  record.environment = await page.evaluate(() => ({ user_agent: navigator.userAgent,
    logical_cpus: navigator.hardwareConcurrency, visibility: document.visibilityState }));
  await mark('import_start');
  await page.locator('.drop input[type=file]').setInputFiles(plan.svg);
  const rows = page.locator('table.parts tbody tr');
  await expect(rows).toHaveCount(4, { timeout: 60_000 });
  await mark('import_done');
  for (let i = 0; i < 4; i++) await rows.nth(i).locator('input[type=number]').first().fill('500');
  const sheet = page.locator('fieldset.sheet-row').first();
  await sheet.getByLabel('Width').fill('1250');
  await sheet.getByLabel('Height').fill('2500');
  await page.getByLabel('Part spacing').fill('1.5');
  await page.getByLabel('Edge spacing').fill('1.5');
  await page.getByLabel('Time').fill(String(plan.seconds));
  if (plan.quick_start || plan.workers != null) {
    await page.getByText('Advanced', { exact: true }).click();
    if (plan.quick_start) await page.getByLabel('Quick initial layout', { exact: true }).check();
    if (plan.workers != null) await page.getByLabel('Workers').fill(String(plan.workers));
  }
  await expect(page.getByLabel('Quick initial layout', { exact: true })).toBeChecked({ checked: !!plan.quick_start });
  record.workers_field = await page.getByLabel('Workers').inputValue();
  record.utility_workers_before_nesting = page.workers().length;
  await mark('nest_start');
  await page.getByRole('button', { name: 'Nest', exact: true }).click();
  await page.waitForFunction(() => document.querySelector('[role=alert]')?.textContent
    || document.querySelector('.summary')?.textContent?.includes('2000/2000'), null, { timeout: 600_000 });
  if (await page.getByRole('alert').count()) {
    record.app_error = await page.getByRole('alert').innerText();
    await mark('nest_failed');
    throw new Error(record.app_error);
  }
  await expect(page.locator('.summary')).toContainText('2000/2000');
  await expect(page.locator('.summary')).toContainText('valid');
  await mark('nest_done');
  record.summary = await page.locator('.summary').innerText();
  await mark('export_start');
  const [download] = await Promise.all([
    page.waitForEvent('download', { timeout: 600_000 }),
    page.getByRole('button', { name: 'Project ZIP', exact: true }).click(),
  ]);
  await download.saveAs(`${plan.out}/project.zip`);
  record.zip_bytes = (await stat(`${plan.out}/project.zip`)).size;
  if (record.zip_bytes <= 1000) throw new Error('Export is unexpectedly small');
  await mark('export_done');
  // Let the observer deliver the task that triggered the download, and let the
  // timer bracket it. No setup or export interval is discarded from the gate.
  await page.waitForTimeout(250);
  record.status = 'completed';
} catch (error) {
  record.status = 'failed';
  record.error = String(error);
} finally {
  try {
    record.telemetry = await page.evaluate(() => window.h4Stats);
    record.visible_text = (await page.locator('body').innerText()).slice(0, 12000);
    await page.screenshot({ path: `${plan.out}/screen.png` });
  } catch (error) { record.capture_error = String(error); }
  const times = record.marks;
  for (const phase of ['import', 'nest', 'export']) if (times[`${phase}_done`] !== undefined) {
    record[`${phase}_seconds`] = (times[`${phase}_done`] - times[`${phase}_start`]) / 1000;
  }
  const relevant = entries => entries.filter(([t, d]) => t + d >= (times.import_start ?? 0));
  record.maximum_long_task_ms = record.telemetry?.long_tasks_supported
    ? Math.max(0, ...relevant(record.telemetry.long_tasks).map(([, d]) => d)) : null;
  record.maximum_event_loop_gap_ms = record.telemetry?.event_loop_gaps.length
    ? Math.max(...relevant(record.telemetry.event_loop_gaps).map(([, d]) => d)) : null;
  record.responsive = record.maximum_event_loop_gap_ms !== null && record.maximum_event_loop_gap_ms <= 200
    && (record.maximum_long_task_ms === null || record.maximum_long_task_ms <= 200);
  await writeFile(`${plan.out}/app.json`, JSON.stringify(record, null, 2));
  await browser.close();
}
console.log(JSON.stringify({ status: record.status, responsive: record.responsive,
  maximum_long_task_ms: record.maximum_long_task_ms, maximum_event_loop_gap_ms: record.maximum_event_loop_gap_ms }));
process.exitCode = record.status === 'completed' ? 0 : 1;
