import { expect, test } from '@playwright/test';

test('explicit gap repair reports locations and can be reapplied without stale parts', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByLabel('Close larger gaps')).not.toBeChecked();
  await page.locator('.drop input[type=file]').setInputFiles({
    name: 'gaps.svg', mimeType: 'image/svg+xml',
    buffer: Buffer.from('<svg width="100mm" height="100mm" viewBox="0 0 100 100"><path id="broken" d="M0 0 H20 V20 H0 V0.2"/><rect id="complete" x="40" width="10" height="10"/></svg>'),
  });
  await expect(page.locator('table.parts tbody tr')).toHaveCount(0);
  await expect(page.locator('.error')).toContainText('Close gaps up to 0.200000 mm');
  await expect(page.getByRole('button', { name: 'Nest', exact: true })).toBeDisabled();
  await page.getByLabel('Close larger gaps').check();
  await page.getByLabel('Close gaps up to (mm)').fill('0.2');
  await page.getByRole('button', { name: 'Apply import options' }).click();
  await expect(page.locator('table.parts tbody tr')).toHaveCount(2);
  await expect(page.locator('.warnings')).toContainText('closed gap 0.200000 mm');
  await expect(page.locator('.warnings')).toContainText('(0.000000, -0.200000)');
  await page.getByLabel('Close larger gaps').uncheck();
  await page.getByRole('button', { name: 'Apply import options' }).click();
  await expect(page.locator('.error')).toContainText('no partial library was created');
  await expect(page.locator('table.parts tbody tr')).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Nest', exact: true })).toBeDisabled();
  await expect(page.locator('.warnings')).toHaveCount(0);
});

test('failed batches keep unrelated files and failed replacements remove stale parts', async ({ page }) => {
  await page.goto('/');
  const file = (name: string, paths: string) => ({ name, mimeType: 'image/svg+xml',
    buffer: Buffer.from(`<svg width="100mm" viewBox="0 0 100 100">${paths}</svg>`) });
  const input = page.locator('.drop input[type=file]');
  await input.setInputFiles(file('kept.svg', '<rect width="20" height="20"/>'));
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  await input.setInputFiles([
    file('complete.svg', '<rect width="10" height="10"/>'),
    file('incomplete.svg', '<rect width="20" height="20"/><path d="M40 0 H60 V20 H40 V0.2"/>'),
  ]);
  await expect(page.locator('.error')).toContainText('no partial library was created');
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  await expect(page.locator('table.parts')).toContainText('kept-1');
  await input.setInputFiles({ name: 'kept.svg', mimeType: 'image/svg+xml', buffer: Buffer.from('<svg><broken') });
  await expect(page.locator('.error')).toContainText('No parts from this import were kept');
  await expect(page.locator('table.parts tbody tr')).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Nest', exact: true })).toBeDisabled();
});
