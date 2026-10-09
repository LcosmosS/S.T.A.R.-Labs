#!/usr/bin/env node
/** Default releases are empty: no raw or user-declared coordinates can plot.
 * Positive display/rejection chains are tested in sky-published-release.test.mjs.
 */
import assert from "node:assert/strict";
import { chromium } from "playwright";
const origin=process.argv[2];
if (!/^https?:\/\/127\.0\.0\.1:8081$/.test(origin ?? "")) {
  console.error("Usage: node scripts/sky-browser-smoke.mjs http://127.0.0.1:8081");
  process.exit(2);
}
const browser=await chromium.launch({headless:true,args:["--no-sandbox","--disable-dev-shm-usage"]});
try {
  for(const viewport of [{width:1280,height:800},{width:390,height:844}]){
    const page=await browser.newPage({viewport});
    const errors=[];
    page.on("pageerror",e=>errors.push(String(e)));
    const response=await page.goto(origin+"/projection",{waitUntil:"domcontentloaded",timeout:40000});
    assert.equal(response?.status(),200);
    await page.getByRole("heading",{name:"Observed sky · Aladin Lite"}).waitFor();
    await page.locator('[data-sky-hydrated="true"]').waitFor({timeout:20000});
    const selector=page.getByLabel("CI-admitted sky dataset");
    assert.equal(await selector.isDisabled(),true,"No source passes the release gate");
    assert.equal(await selector.locator("option").allTextContents().then(x=>x.join("")),"No approved sky releases");
    assert.equal(await page.getByRole("button",{name:"Load CI-verified sky dataset"}).isDisabled(),true);
    await page.getByRole("status").filter({hasText:/No CI-admitted observational sky releases/}).waitFor();
    assert.equal(await page.locator("#star-aladin-sky-viewport").count(),0);
    assert.equal(await page.getByLabel("Expected SHA-256").count(),0,"Never accept a user-asserted checksum");
    assert.equal(await page.getByLabel("Frozen local coordinate CSV").count(),0,"No unapproved local file");
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth+1),false);
    assert.deepEqual(errors,[],"No uncaught client errors");
    console.log("PASS fail-closed CI sky selector",viewport.width,viewport.height);
    await page.close();
  }
} finally {await browser.close();}
