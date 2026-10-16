import { defineConfig, devices } from '@playwright/test';

// PW_CHROME=1 adds the installed Google Chrome as a third browser.
export default defineConfig({
  testDir: 'tests',
  timeout: 180_000,
  reporter: [['list']],
  use: {
    baseURL: 'http://127.0.0.1:4173',
    trace: process.env.CI ? 'retain-on-failure' : 'off',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'npm run preview -- --host 127.0.0.1',
    url: 'http://127.0.0.1:4173',
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    ...(process.env.PW_CHROME ? [{ name: 'chrome', use: { ...devices['Desktop Chrome'], channel: 'chrome' } }] : []),
  ],
});
