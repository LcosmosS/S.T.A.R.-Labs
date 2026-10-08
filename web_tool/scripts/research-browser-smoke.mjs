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
    assert.match(await page.getByRole("status").innerText(), /9 of 9/);
    const links = page.getByRole("link", { name: "View cited repository source" });
    assert.equal(await links.count(), 9);
    for (const url of await links.evaluateAll(nodes => nodes.map(n => n.getAttribute("href")))) {
      assert.match(url, /^https:\/\/github\.com\/LcosmosS\/S\.T\.A\.R\.-Labs\/blob\/main\//);
    }
    await page.getByLabel("Filter research content type").selectOption("diagram");
    await page.getByRole("status").filter({ hasText: /2 of 9/ }).waitFor();
    await page.getByLabel("Filter research content type").selectOption("all");
    await page.getByLabel("Search research content").fill("E1A");
    await page.getByRole("status").filter({ hasText: /1 of 9/ }).waitFor();
    assert.equal(await page.getByRole("link", { name: "View cited repository source" }).count(), 1);
    await page.getByLabel("Search research content").fill("");
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
    assert.equal(overflow, false, "horizontal overflow");
    assert.deepEqual(errors, [], "uncaught errors");
    console.log("PASS /research Chromium", viewport.width + "x" + viewport.height);
    await page.close();
  }
} finally {
  await browser.close();
}
