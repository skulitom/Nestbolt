// Runs polygon benchmark jobs in a real browser through bench.html: every job
// in its own Web Worker, at most `concurrency` at once on one page. Driven by
// scripts/g5_browser.py, which serves the built site and scores the layouts.
import { readFile, writeFile } from 'node:fs/promises';
import { chromium, firefox } from '@playwright/test';

const plan = JSON.parse(await readFile(process.argv[2], 'utf8'));
// `chrome` is the installed Google Chrome; `chromium` and `firefox` are Playwright's builds.
const engine = { chrome: chromium, chromium, firefox }[plan.browser];
const browser = await engine.launch({ headless: true, ...(plan.browser === 'chrome' ? { channel: 'chrome' } : {}) });
const page = await browser.newPage();
await page.goto(plan.url);
await page.waitForFunction(() => window.benchReady === true);
const info = await page.evaluate(() => ({ userAgent: navigator.userAgent, cores: navigator.hardwareConcurrency }));
console.log(JSON.stringify({ browser: plan.browser, version: browser.version(), ...info }));
await writeFile(plan.info, JSON.stringify({ browser: plan.browser, version: browser.version(), ...info }, null, 1));

let next = 0;
async function lane() {
  while (next < plan.jobs.length) {
    const job = plan.jobs[next++];
    const text = await readFile(job.path, 'utf8');
    const started = Date.now();
    try {
      const out = await page.evaluate(([j, s, seed]) => window.nestJob(j, s, seed).then((r) => JSON.stringify(r)),
        [text, plan.seconds, plan.seed]);
      const { result, memoryBytes } = JSON.parse(out);
      await writeFile(`${job.out}/layout.json`, JSON.stringify(result.layout, null, 1));
      delete result.layout;
      await writeFile(`${job.out}/result.json`, JSON.stringify({ ...result, memory_bytes: memoryBytes,
        page_wall_seconds: (Date.now() - started) / 1000 }, null, 1));
      console.log(JSON.stringify({ job: job.id, material: result.validation.metrics?.normalized_material ?? null }));
    } catch (error) {
      await writeFile(`${job.out}/error.txt`, String(error));
      console.log(JSON.stringify({ job: job.id, error: String(error).slice(0, 300) }));
    }
  }
}
await Promise.all(Array.from({ length: plan.concurrency }, lane));
await browser.close();
