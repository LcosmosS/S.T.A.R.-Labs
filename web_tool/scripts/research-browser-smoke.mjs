#!/usr/bin/env node
/** Real Chromium checks for research catalog display and its evidence gating. */
import assert from "node:assert/strict";
import { chromium } from "playwright";

const origin = process.argv[2];
if (!/^https?:\/\/127\.0\.0\.1:8081$/.test(origin ?? "")) {
  console.error("Usage: node scripts/research-browser-smoke.mjs http://127.0.0.1:8081");
  process.exit(2);
}
const browser = await chromium.launch({ headless: true, args: ["--no-sandbox", "--disable-dev-shm-usage"] });
try {
  for (const viewport of [{ width: 1280, height: 800 }, { width: 390, height: 844 }]) {
    const page = await browser.newPage({ viewport });
    const errors = [];
    page.on("pageerror", e => errors.push(String(e)));
    page.on("console", e => { if (e.type() === "error") errors.push(e.text()); });
    const response = await page.goto(origin + "/research", { waitUntil: "domcontentloaded", timeout: 40000 });
    assert.equal(response?.status(), 200, "research page HTTP");
    await page.getByRole("heading", { name: "Research constructs and source artifacts" }).waitFor();
    // SSR content can appear before React installs interactive event handlers.
    // The page's useEffect-driven marker distinguishes actual hydration.
    await page.locator('[data-research-hydrated="true"]').waitFor({ timeout: 20000 });
    assert.match(await page.getByRole("status").innerText(), /12 of 12/);
    const links = page.getByRole("link", { name: "View cited repository source" });
    assert.equal(await links.count(), 12);
    for (const url of await links.evaluateAll(nodes => nodes.map(n => n.getAttribute("href")))) {
      assert.match(url, /^https:\/\/github\.com\/LcosmosS\/S\.T\.A\.R\.-Labs\/blob\/main\//);
    }
    await page.getByLabel("Filter research content type").selectOption("diagram");
    await page.getByRole("status").filter({ hasText: /2 of 12/ }).waitFor();
    await page.getByLabel("Filter research content type").selectOption("all");
    await page.getByLabel("Search research content").fill("E1A");
    await page.getByRole("status").filter({ hasText: /1 of 12/ }).waitFor();
    assert.equal(await page.getByRole("link", { name: "View cited repository source" }).count(), 1);
    await page.getByLabel("Search research content").fill("");
    await page.getByRole("heading", { name: "Finite positive bin-count series cannot vanish at s=1" }).waitFor();
    await page.getByRole("heading", { name: "Historical five-fold SFR metric — unreplicated" }).waitFor();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
    assert.equal(overflow, false, "horizontal overflow");
    assert.deepEqual(errors, [], "uncaught errors");
    console.log("PASS /research Chromium", viewport.width + "x" + viewport.height);
    await page.close();
  }
} finally {
  await browser.close();
}
