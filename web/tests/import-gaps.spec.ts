import { expect, test } from '@playwright/test';

test('explicit gap repair reports locations and can be reapplied without stale parts', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByLabel('Close larger gaps')).not.toBeChecked();
  await page.locator('.drop input[type=file]').setInputFiles({
    name: 'gaps.svg', mimeType: 'image/svg+xml',
    buffer: Buffer.from('<svg width="100mm" height="100mm" viewBox="0 0 100 100"><path id="broken" d="M0 0 H20 V20 H0 V0.2"/><rect id="complete" x="40" width="10" height="10"/></svg>'),
  });
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  await expect(page.locator('.warnings')).toContainText('Close gaps up to 0.200000 mm');
  await page.getByLabel('Close larger gaps').check();
  await page.getByLabel('Close gaps up to (mm)').fill('0.2');
  await page.getByRole('button', { name: 'Apply import options' }).click();
  await expect(page.locator('table.parts tbody tr')).toHaveCount(2);
  await expect(page.locator('.warnings')).toContainText('closed gap 0.200000 mm');
  await expect(page.locator('.warnings')).toContainText('(0.000000, -0.200000)');
  await page.getByLabel('Close larger gaps').uncheck();
  await page.getByRole('button', { name: 'Apply import options' }).click();
  await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  await expect(page.locator('.warnings')).not.toContainText('closed gap');
});
