import { expect, test } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const fixture = fileURLToPath(new URL('../../crates/core/tests/fixtures/roundtrip.lbrn2', import.meta.url));
const source = readFileSync(fixture, 'utf8');

test('legacy LightBurn paths become editable modern sheet files', async ({ page }, info) => {
  const legacy = fileURLToPath(new URL('../../crates/core/tests/fixtures/legacy.lbrn', import.meta.url));
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles(legacy);
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  await page.getByLabel('Quantity of legacy-unit-1').fill('2');
  const sheet = page.locator('fieldset.sheet-row').first();
  await sheet.getByLabel('Width').fill('34');
  await sheet.getByLabel('Height').fill('14');
  await sheet.getByLabel('Margin').fill('0');
  await page.getByLabel('Edge spacing').fill('0.5');
  await page.getByLabel('Time').fill('1');
  await page.getByText('Advanced').click();
  await page.getByLabel('Workers').fill('1');
  await page.getByRole('button', { name: 'Nest', exact: true }).click();
  await expect(page.locator('.summary, .error').first()).toBeVisible({ timeout: 90_000 });
  await expect(page.locator('.error')).toHaveCount(0);
  await expect(page.locator('.summary')).toContainText('valid');
  await expect(page.locator('.summary')).toContainText('2/2');
  await expect(page.getByRole('button', { name: 'LightBurn', exact: true })).toHaveCount(2);
  const [download] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Download all sheets (ZIP)' }).click()]);
  await download.saveAs(info.outputPath('legacy-sheets.zip'));
  const files = entries(await download.path());
  expect(files.size).toBe(2);
  const checked = await page.evaluate(outputs => outputs.map(xml => {
    const doc = new DOMParser().parseFromString(xml, 'text/xml');
    return {
      valid: !doc.querySelector('parsererror'), version: doc.documentElement.getAttribute('FormatVersion'),
      vertices: doc.querySelectorAll('VertList').length, primitives: doc.querySelectorAll('PrimList').length,
      retained: doc.querySelector('V[Future]')?.getAttribute('Future'), start: doc.querySelector('Shape[StartV]')?.getAttribute('StartV'),
      opaque: doc.querySelector('Unknown V')?.getAttribute('vx'),
    };
  }), [...files.values()]);
  for (const value of checked) expect(value).toEqual({ valid: true, version: '1', vertices: 2, primitives: 2, retained: 'a & b', start: '1', opaque: 'opaque' });
  await page.screenshot({ path: info.outputPath('legacy-layout.png'), fullPage: true });
});

function entries(path: string): Map<string, string> {
  const data = readFileSync(path), files = new Map<string, string>();
  for (let at = 0; data.readUInt32LE(at) === 0x04034b50;) {
    expect(data.readUInt16LE(at + 8)).toBe(0);
    const size = data.readUInt32LE(at + 18), length = data.readUInt16LE(at + 26);
    const start = at + 30 + length + data.readUInt16LE(at + 28);
    files.set(data.subarray(at + 30, at + 30 + length).toString('utf8'), data.subarray(start, start + size).toString('utf8'));
    at = start + size;
  }
  return files;
}

test('LightBurn rigid units nest and download as editable per-sheet projects', async ({ page }, info) => {
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles(fixture);
  await expect(page.locator('table.parts tbody tr')).toHaveCount(3);
  const group = page.locator('table.parts tbody tr').filter({ hasText: 'roundtrip-unit-1' });
  await expect(group).toContainText('2.0 cm²');
  expect((await group.locator('.thumb path').getAttribute('d'))!.match(/M/g)).toHaveLength(2);
  await expect(page.getByText('LightBurn layers — preserved')).toBeVisible();
  await expect(page.locator('.import-channels tbody tr').first()).toContainText('0.2');
  await expect(page.getByLabel('Include sheet outline on T1')).toBeChecked();
  await expect(page.locator('.warnings')).toContainText('spacing is not changed automatically');
  await page.getByLabel('Quantity of roundtrip-unit-1').fill('2');
  await page.getByLabel('Allow mirroring roundtrip-unit-1').check();
  const sheet = page.locator('fieldset.sheet-row').first();
  await sheet.getByLabel('Width').fill('34');
  await sheet.getByLabel('Height').fill('24');
  await sheet.getByLabel('Margin').fill('0');
  await page.getByLabel('Edge spacing').fill('0.5');
  await page.getByLabel('Time').fill('1');
  await page.getByText('Advanced').click();
  await page.getByLabel('Workers').fill('1');
  await page.getByRole('button', { name: 'Nest', exact: true }).click();
  await expect(page.locator('.summary, .error').first()).toBeVisible({ timeout: 90_000 });
  await expect(page.locator('.error')).toHaveCount(0);
  await expect(page.locator('.summary')).toContainText('valid');
  await expect(page.locator('.summary')).toContainText('4/4');
  const buttons = page.getByRole('button', { name: 'LightBurn', exact: true });
  const count = await buttons.count();
  expect(count).toBeGreaterThanOrEqual(2);
  await expect(page.getByRole('button', { name: 'SVG', exact: true })).toHaveCount(0);
  const [first] = await Promise.all([page.waitForEvent('download'), buttons.first().click()]);
  expect(first.suggestedFilename()).toBe('roundtrip-sheet-1.lbrn2');
  const firstText = readFileSync(await first.path(), 'utf8');
  const [all] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Download all sheets (ZIP)' }).click()]);
  const files = entries(await all.path());
  await all.saveAs(info.outputPath('sheets.zip'));
  expect(files.size).toBe(count);
  expect(files.get('sheets/roundtrip-sheet-1.lbrn2')).toBe(firstText);
  for (let i = 1; i <= count; ++i) expect(files.has(`sheets/roundtrip-sheet-${i}.lbrn2`)).toBe(true);
  const checked = await page.evaluate(({ source, outputs }) => {
    const parser = new DOMParser();
    const original = parser.parseFromString(source, 'text/xml');
    const settings = Array.from(original.documentElement.children).filter(e => e.tagName !== 'Shape').map(e => e.outerHTML);
    let groups = 0, texts = 0, bitmaps = 0;
    for (const xml of outputs) {
      const doc = parser.parseFromString(xml, 'text/xml');
      if (doc.querySelector('parsererror')) throw new Error('Malformed output XML');
      if (doc.documentElement.getAttribute('MirrorX') !== 'True') throw new Error('Origin changed');
      const kept = Array.from(doc.documentElement.children).filter(e => e.tagName !== 'Shape').map(e => e.outerHTML);
      if (JSON.stringify(kept) !== JSON.stringify(settings)) throw new Error('Project settings changed');
      const outline = doc.querySelector('Shape[Type="Rect"][CutIndex="30"][W="34"][H="24"]');
      if (!outline) throw new Error('Missing T1 outline');
      if (!doc.querySelector('Shape[Type="Rect"][CutIndex="30"][W="3"][H="4"]')) throw new Error('Fixed shape lost');
      for (const g of Array.from(doc.querySelectorAll('Shape[Type="Group"]'))) {
        ++groups;
        if (g.querySelector('Children')!.outerHTML !== original.querySelector('Children')!.outerHTML) throw new Error('Group children changed');
      }
      for (const text of Array.from(doc.querySelectorAll('Shape[Type="Text"]'))) {
        ++texts;
        if (text.querySelector('BackupPath')!.outerHTML !== original.querySelector('BackupPath')!.outerHTML) throw new Error('Text cache lost');
      }
      for (const bitmap of Array.from(doc.querySelectorAll('Shape[Type="Bitmap"]'))) {
        ++bitmaps;
        const hash = bitmap.getAttribute('SourceHash');
        if (!Array.from(doc.querySelectorAll('Shape[Type="Bitmap"]')).some(b => b.getAttribute('SourceHash') === hash && b.hasAttribute('Data'))) throw new Error('Shared bitmap data lost');
      }
    }
    return { groups, texts, bitmaps };
  }, { source, outputs: [...files.values()] });
  expect(checked).toEqual({ groups: 2, texts: 1, bitmaps: 2 });
  await page.screenshot({ path: info.outputPath('lightburn-layout.png'), fullPage: true });
  await page.getByText('LightBurn layers — preserved').scrollIntoViewIfNeeded();
  await page.screenshot({ path: info.outputPath('lightburn-layers.png'), fullPage: true });
  await page.getByLabel('Include sheet outline on T1').uncheck();
  const [without] = await Promise.all([page.waitForEvent('download'), buttons.first().click()]);
  expect(readFileSync(await without.path(), 'utf8')).not.toMatch(/Type="Rect"[^>]*W="34"[^>]*H="24"/);
  const [project] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Project ZIP' }).click()]);
  await project.saveAs(info.outputPath('project.zip'));
  const saved = JSON.parse(entries(await project.path()).get('project.json')!);
  expect(saved.library.lightburn.xml).toBe(source);
  expect(saved.library.parts[0].components).toHaveLength(2);
  expect(saved.lightburnOutline).toBe(false);
  expect(saved.result.validation.valid).toBe(true);
});
