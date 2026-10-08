// @ts-check
const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  timeout: 30_000,
  retries: process.env.CI ? 1 : 0,
  reporter: [["list"], ["html", { open: "never", outputFolder: "test-report" }]],
  use: { trace: "retain-on-failure", screenshot: "only-on-failure" },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"], viewport: { width: 1300, height: 900 } } },
    { name: "phone", use: { ...devices["Pixel 7"] }, testMatch: /apps\.spec\.js/ },
    { name: "ipad", use: { ...devices["iPad (gen 7) landscape"], browserName: "chromium" }, testMatch: /apps\.spec\.js/ }
  ]
});
