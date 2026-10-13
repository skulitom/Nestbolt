import { expect, test } from '@playwright/test';

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
