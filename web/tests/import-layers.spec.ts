import { expect, test } from '@playwright/test';
import { readFileSync } from 'node:fs';

test('a custom stock layer is offered separately from the cut selection', async ({ page }) => {
  await page.goto('/');
  const source = readFileSync(new URL('../../crates/core/tests/fixtures/prearranged-sheet.svg', import.meta.url), 'utf8').replace('id="SHEET"','id="MATERIAL"');
  await page.locator('.drop input[type=file]').setInputFiles({ name: 'custom.svg', mimeType: 'image/svg+xml', buffer: Buffer.from(source) });
  await expect(page.locator('table.parts tbody tr')).toHaveCount(2);
  await expect(page.getByLabel('Imported sheet outline for sheet size 1')).toHaveCount(0);
  await page.getByLabel('Sheet layer MATERIAL in custom.svg', { exact: true }).check();
  await page.getByRole('button', { name: 'Apply import options' }).click();
  await page.getByLabel('Imported sheet outline for sheet size 1').selectOption('custom-sheet-1');
  await expect(page.locator('table.parts tbody tr')).toHaveCount(2);
  await expect(page.locator('fieldset.sheet-row').first().getByLabel('Width')).toHaveValue('200');
  await expect(page.locator('fieldset.sheet-row').first().getByLabel('Height')).toHaveValue('100');
});

test('closed retraced holes survive cleanup with a visible warning', async ({ page }) => {
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles({ name: 'closed-retrace.svg', mimeType: 'image/svg+xml',
    buffer: readFileSync(new URL('../../crates/core/tests/fixtures/closed-retrace.svg', import.meta.url)) });
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  await expect(page.locator('.warnings')).toContainText('retained 2 overlapping segment pair(s) to keep closed paths connected');
});

test('legacy DXF text keeps layer names and offers an explicit inches choice', async ({ page }) => {
  await page.goto('/');
  const dxf = '0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1009\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n0\nLWPOLYLINE\n8\nCUT_Ø\n70\n1\n90\n4\n10\n0\n20\n0\n10\n20\n20\n0\n10\n20\n20\n10\n10\n0\n20\n10\n0\nENDSEC\n0\nEOF\n';
  await page.locator('.drop input[type=file]').setInputFiles({ name: 'legacy.dxf', mimeType: 'application/dxf', buffer: Buffer.from(dxf, 'latin1') });
  await expect(page.getByLabel('Layer CUT_Ø in legacy.dxf', { exact: true })).toBeChecked();
  await expect(page.locator('table.parts tbody tr')).toContainText('2.0 cm²');
  await expect(page.locator('.warnings')).toContainText('this may be an inches drawing');
  await page.getByLabel('DXF units when missing — legacy.dxf').selectOption('25.4');
  await page.getByRole('button', { name: 'Apply import options' }).click();
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  await expect(page.locator('table.parts tbody tr')).toContainText('1290.3 cm²');
});

test('cleanup shows duplicate, zero-length and overlap counts', async ({ page }) => {
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles({ name: 'cleanup.svg', mimeType: 'image/svg+xml',
    buffer: Buffer.from('<svg width="100mm" viewBox="0 0 100 100"><path d="M0 0 H12 M8 0 H20 V20 H0 V0 M20 0 V20 M0 0 L0 0"/></svg>') });
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  await expect(page.locator('.import-channels')).toContainText('1 duplicate segments removed; 1 zero-length segments removed; 1 collinear overlaps merged');
});

test('layer and colour choices retain counts and replace the selected parts', async ({ page }) => {
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles({ name: 'layers.svg', mimeType: 'image/svg+xml',
    buffer: Buffer.from('<svg width="100mm" viewBox="0 0 100 100"><g id="CUT" stroke="black"><rect width="20" height="20"/></g><g id="SCORE" stroke="red"><rect x="40" width="10" height="10"/><text>label</text></g></svg>') });
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  await expect(page.getByLabel('Layer CUT in layers.svg', { exact: true })).toBeChecked();
  await expect(page.getByLabel('Layer SCORE in layers.svg', { exact: true })).not.toBeChecked();
  await expect(page.locator('.import-channels')).toContainText('2 entities');
  await page.getByLabel('Layer CUT in layers.svg', { exact: true }).uncheck();
  await page.getByLabel('Layer SCORE in layers.svg', { exact: true }).check();
  await page.getByRole('button', { name: 'Apply import options' }).click();
  await expect(page.locator('table.parts tbody tr')).toContainText('1.0 cm²');
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  await page.getByRole('button', { name: 'Use automatic selection for layers.svg' }).click();
  await page.getByLabel('Colour #000000 in layers.svg', { exact: true }).check();
  await page.getByLabel('Colour #ff0000 in layers.svg', { exact: true }).uncheck();
  await page.getByRole('button', { name: 'Apply import options' }).click();
  await expect(page.locator('table.parts tbody tr')).toContainText('4.0 cm²');
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
});

test('open-only drawings still expose the inventory and gap repair', async ({ page }) => {
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles({ name: 'open.svg', mimeType: 'image/svg+xml',
    buffer: Buffer.from('<svg width="100mm" viewBox="0 0 100 100"><g id="CUT"><path d="M0 0 H20 V20 H0 V0.2"/></g></svg>') });
  await expect(page.getByLabel('Layer CUT in open.svg', { exact: true })).toBeVisible();
  await expect(page.locator('table.parts tbody tr')).toHaveCount(0);
  await page.getByLabel('Close larger gaps').check();
  await page.getByLabel('Close gaps up to (mm)').fill('0.2');
  await page.getByRole('button', { name: 'Apply import options' }).click();
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
});
