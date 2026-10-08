#!/usr/bin/env node
/** Chromium verify → reject mismatch → Aladin overlay with mocked CDS SDK.
 * The mock avoids network-dependent scientific/browser checks; the real SDK
 * still needs a separate non-CI integration check for third-party availability.
 */
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { chromium } from "playwright";

const origin = process.argv[2];
if (!/^https?:\/\/127\.0\.0\.1:8081$/.test(origin ?? "")) {
  console.error("Usage: node scripts/sky-browser-smoke.mjs http://127.0.0.1:8081");
  process.exit(2);
}
const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-dev-shm-usage"] });
try {
  for (const viewport of [{ width: 1280, height: 800 }, { width: 390, height: 844 }]) {
    const page = await browser.newPage({ viewport });
    const errors = [];
    page.on("pageerror", (e) => errors.push(String(e)));
    await page.addInitScript(() => {
      const state = { sources: [], options: null, survey: null, counts: 0 };
      window.__starSkySmoke = state;
      window.A = {
        init: Promise.resolve(),
        aladin: (_, options) => {
          state.options = options;
          return {
            addCatalog: () => {},
            setImageSurvey: (survey) => { state.survey = survey; },
          };
        },
        catalog: () => ({
          addSources: (sources) => { state.sources = sources; state.counts++; },
          removeAll: () => { state.sources = []; },
        }),
        source: (ra, dec, data) => ({ ra, dec, data }),
      };
    });
    const response = await page.goto(origin + "/projection", { waitUntil: "domcontentloaded", timeout: 40000 });
    assert.equal(response?.status(), 200);
    await page.getByRole("heading", { name: "Observed sky · Aladin Lite" }).waitFor();
    assert.equal(await page.locator("#star-aladin-sky-viewport").count(), 0, "No sources before hash verified");
    const source = "source_id,ra_deg,dec_deg\nTEST:1,359.999,-1\nTEST:2,0.001,1\n";
    const buffer = Buffer.from(source);
    const sha = createHash("sha256").update(buffer).digest("hex");
    await page.getByLabel("Frozen local coordinate CSV").setInputFiles({ name: "frozen.csv", mimeType: "text/csv", buffer });
    await page.getByLabel("Expected SHA-256").fill("0".repeat(64));
    await page.getByRole("button", { name: "Verify bytes and display on sky" }).click();
    await page.getByRole("status").filter({ hasText: /SHA-256 mismatch/ }).waitFor();
    assert.equal(await page.locator("#star-aladin-sky-viewport").count(), 0);
    await page.getByLabel("Expected SHA-256").fill(sha);
    await page.getByRole("button", { name: "Verify bytes and display on sky" }).click();
    await page.getByRole("status").filter({ hasText: /SHA-256 verified locally for 2/ }).waitFor();
    await page.waitForFunction(() => window.__starSkySmoke?.sources.length === 2, { timeout: 15000 });
    const result = await page.evaluate(() => window.__starSkySmoke);
    assert.deepEqual(result.sources.map((p) => p.data.source_id), ["TEST:1", "TEST:2"]);
    assert.equal(result.options.cooFrame, "ICRS");
    assert.equal(result.options.survey, "P/DSS2/color");
    await page.getByLabel("Background sky survey").selectOption("P/SDSS9/color");
    await page.waitForFunction(() => window.__starSkySmoke?.survey === "P/SDSS9/color");
    await page.getByLabel("Show verified coordinate overlay").uncheck();
    await page.waitForFunction(() => window.__starSkySmoke?.sources.length === 0);
    await page.getByLabel("Show verified coordinate overlay").check();
    await page.waitForFunction(() => window.__starSkySmoke?.sources.length === 2);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1), false, "horizontal overflow");
    assert.deepEqual(errors, [], "uncaught client errors");
    console.log("PASS local hashed Aladin overlay", viewport.width, viewport.height);
    await page.close();
  }
} finally {
  await browser.close();
}
