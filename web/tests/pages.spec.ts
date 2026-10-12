import { expect, test } from '@playwright/test';

// G5 hosting: the deployed GitHub Pages site works with no special headers.
// Runs only with PAGES_URL, for example https://skulitom.github.io/Nestbolt/.
const url = process.env.PAGES_URL;

test('the deployed app nests the example from GitHub Pages', async ({ page }) => {
  test.skip(!url, 'PAGES_URL not set');
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(e.message));
  const response = await page.goto(url!);
  expect(response?.ok()).toBe(true);
  // No cross-origin isolation is required: workers and WebAssembly suffice.
  expect(response?.headers()['cross-origin-embedder-policy']).toBeUndefined();
  await page.getByRole('button', { name: 'Try an example: two finger-jointed boxes' }).click();
  await expect(page.locator('.summary')).toContainText('12/12', { timeout: 60_000 });
  await expect(page.locator('.summary')).toContainText('valid');
  expect(errors).toEqual([]);
});
