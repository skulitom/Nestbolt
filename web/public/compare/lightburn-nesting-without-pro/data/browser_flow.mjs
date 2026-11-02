// The LightBurn-plus-offcut flow in the live browser app (headless Chromium, fresh profile).
// Opens engraved-ornaments.lbrn2, sets each design's quantity to 2, picks traced-offcut.svg as the remnant
// outline, sets part and edge spacing to 2 mm, nests (30 s) and downloads the LightBurn sheet.
// Usage: node browser_flow.mjs <app-url> <kit-gen-dir> <out-dir>
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const [url, gen, out] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
// Set CHROMIUM to a browser executable if Playwright's own Chromium is not installed.
const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const ctx = await browser.newContext({ acceptDownloads: true, viewport: { width: 1400, height: 1100 } });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(url + `?v=${Date.now()}`);
const assets = await page.evaluate(() => [...document.querySelectorAll('script[src],link[rel=modulepreload]')].map((s) => s.src || s.href));
await page.locator('input[type=file][accept=".svg,.dxf,.lbrn,.lbrn2"]').setInputFiles(join(gen, 'engraved-ornaments.lbrn2'));
await page.getByText('LightBurn layers — preserved').waitFor({ timeout: 60000 });
const layers = await page.locator('table.lightburn-layers').innerText();
for (let i = 1; i <= 6; i++) {
  const q = page.getByLabel(`Quantity of engraved-ornaments-unit-${i}`);
  await q.fill('2');
}
await page.getByLabel('Remnant outline for sheet size 1').setInputFiles(join(gen, 'traced-offcut.svg'));
await page.locator('span.remnant').waitFor({ timeout: 60000 });
await page.getByLabel(/^Part spacing/).fill('2');
await page.getByLabel(/^Edge spacing/).fill('2');
const t0 = Date.now();
await page.getByRole('button', { name: 'Nest', exact: true }).click();
await page.locator('.summary').filter({ hasText: /valid|invalid/i }).waitFor({ timeout: 240000 });
const summary = {};
for (const row of await page.locator('.summary > div').all()) {
  summary[(await row.locator('dt').innerText()).trim()] = (await row.locator('dd').innerText()).trim();
}
await page.screenshot({ path: join(out, 'browser-result.png'), fullPage: false });
const [dl] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'LightBurn', exact: true }).first().click()]);
const saved = join(out, dl.suggestedFilename());
await dl.saveAs(saved);
const res = { url, assets, layers, summary, wall_s: (Date.now() - t0) / 1000, download: saved, errors };
writeFileSync(join(out, 'browser-flow.json'), JSON.stringify(res, null, 1));
console.log(JSON.stringify(res, null, 1));
await browser.close();
