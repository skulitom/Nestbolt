// Diagnostic CPU samples of the unchanged WASM entry point. Unlike the quality
// runner, this calls it on an isolated page so CDP can profile the whole call.
// It is not an app responsiveness or equal-budget quality measurement.
import { readFile, writeFile } from 'node:fs/promises';
import { chromium } from '@playwright/test';

const plan = JSON.parse(await readFile(process.argv[2], 'utf8'));
const browser = await chromium.launch({ headless: true, channel: 'chrome' });
await writeFile(plan.info, JSON.stringify({ browser: 'chrome', version: browser.version() }, null, 2));
try {
  for (const job of plan.jobs) {
    const page = await browser.newPage();
    page.setDefaultTimeout(150000);
    await page.goto(plan.url);
    await page.waitForFunction(() => window.profileReady === true);
    const session = await page.context().newCDPSession(page);
    await session.send('Profiler.enable');
    await session.send('Profiler.setSamplingInterval', { interval: 1000 });
    const text = await readFile(job.path, 'utf8');
    await session.send('Profiler.start');
    const started = performance.now();
    try {
      const result = await page.evaluate(([source, seconds, seed]) => {
        const parsed = JSON.parse(window.profileJob(source, seconds, seed, false, () => {}));
        return { ...parsed, memory_bytes: window.profileMemory() };
      }, [text, plan.seconds, plan.seed]);
      const wall = (performance.now() - started) / 1000;
      await writeFile(`${job.out}/layout.json`, JSON.stringify(result.layout, null, 2));
      delete result.layout;
      await writeFile(`${job.out}/result.json`, JSON.stringify({ ...result, page_wall_seconds: wall }, null, 2));
      console.log(JSON.stringify({ job: job.id, valid: result.validation.valid, wall_seconds: wall }));
    } catch (error) {
      await writeFile(`${job.out}/error.txt`, String(error));
      console.log(JSON.stringify({ job: job.id, error: String(error) }));
    } finally {
      const { profile } = await session.send('Profiler.stop');
      await writeFile(`${job.out}/cpu.cpuprofile`, JSON.stringify(profile));
      await session.detach();
      await page.close();
    }
  }
} finally {
  await browser.close();
}
