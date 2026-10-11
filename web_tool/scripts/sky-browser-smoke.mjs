#!/usr/bin/env node
/** Browser verifies ALFALFA same-origin bytes before passing 2,000 positions
 * to the Aladin Lite marker API. The real external Aladin script is replaced
 * with a deterministic spy: tests verify API inputs, not rendered sky imagery.
 */
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const origin=process.argv[2];
if (!/^https?:\/\/127\.0\.0\.1:8081$/.test(origin??"")) {
  console.error("Usage: node scripts/sky-browser-smoke.mjs http://127.0.0.1:8081");
  process.exit(2);
}
const ALADIN="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.1/aladin.js";
const ASSET="/sky/alfalfa100-hi-centroids-v1.csv";
const aladinSpy=`
window.__starAladinAudit = { sourceCalls: [], added: 0 };
window.A = {
  init: Promise.resolve(),
  aladin: () => ({ addCatalog: () => {}, setImageSurvey: () => {} }),
  catalog: () => ({
    addSources: rows => { window.__starAladinAudit.added = rows.length; },
    removeAll: () => { window.__starAladinAudit.added = 0; }
  }),
  source: (ra,dec,data) => {
    window.__starAladinAudit.sourceCalls.push({ra,dec,id:data.source_id});
    return {ra,dec,data};
  }
};
`;
const browser=await chromium.launch({headless:true,args:["--no-sandbox","--disable-dev-shm-usage"]});
try {
  for(const viewport of [{width:1280,height:800},{width:390,height:844}]){
    const page=await browser.newPage({viewport});
    const errors=[],skyRequests=[];
    page.on("pageerror",e=>errors.push(String(e)));
    page.on("request",req=>{if(req.url().endsWith(ASSET))skyRequests.push(req.url());});
    await page.route(ALADIN,route=>route.fulfill({status:200,contentType:"application/javascript",headers:{"access-control-allow-origin":"*"},body:aladinSpy}));
    const response=await page.goto(origin+"/projection",{waitUntil:"domcontentloaded",timeout:40000});
    assert.equal(response?.status(),200);
    await page.getByRole("heading",{name:"Observed sky · Aladin Lite"}).waitFor();
    await page.locator('[data-sky-hydrated="true"]').waitFor({timeout:20000});
    const selector=page.getByLabel("CI-admitted sky dataset");
    assert.equal(await selector.isDisabled(),false,"Reviewed release should be selectable");
    const choices=await selector.locator("option").allTextContents();
    assert.equal(choices.length,1);
    assert.match(choices[0],/DATA-VIZIER-ALFALFA100.*hi_centroid/);
    await page.getByRole("button",{name:"Load CI-verified sky dataset"}).click();
    await page.getByRole("status").filter({hasText:/coordinates and selected IDs verified/}).waitFor({timeout:30000});
    await page.waitForFunction(()=>window.__starAladinAudit?.added===2000,{timeout:25000});
    const audit=await page.evaluate(()=>window.__starAladinAudit);
    assert.equal(audit.sourceCalls.length,2000);
    assert.equal(audit.added,2000);
    assert.ok(audit.sourceCalls.every(x=>x.id.startsWith("AGC-")));
    assert.deepEqual(skyRequests,[origin+ASSET],"Fetch only same-origin reviewed release");
    assert.equal(await page.locator("#star-aladin-sky-viewport").count(),1);
    assert.equal(await page.getByText(/2000 positions/).count(),1);
    assert.equal(await page.getByLabel("Expected SHA-256").count(),0);
    assert.equal(await page.getByLabel("Frozen local coordinate CSV").count(),0);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth+1),false);
    assert.deepEqual(errors,[],"No uncaught client errors");
    console.log("PASS 2,000 byte-verified Aladin marker inputs",viewport.width,viewport.height);
    await page.close();
  }
  // Browser negative path: modified served asset must not reach Aladin.
  const page=await browser.newPage();
  const bytes=await readFile(fileURLToPath(new URL("../public/sky/alfalfa100-hi-centroids-v1.csv",import.meta.url)));
  const altered=Buffer.from(bytes);
  altered[altered.length-2]=altered[altered.length-2]===48?49:48;
  await page.route("**"+ASSET,route=>route.fulfill({status:200,contentType:"text/csv",body:altered}));
  await page.route(ALADIN,route=>route.fulfill({status:200,contentType:"application/javascript",headers:{"access-control-allow-origin":"*"},body:aladinSpy}));
  await page.goto(origin+"/projection",{waitUntil:"domcontentloaded",timeout:40000});
  await page.locator('[data-sky-hydrated="true"]').waitFor({timeout:20000});
  await page.getByRole("button",{name:"Load CI-verified sky dataset"}).click();
  await page.getByRole("status").filter({hasText:/SHA-256 mismatch/}).waitFor({timeout:30000});
  assert.equal(await page.locator("#star-aladin-sky-viewport").count(),0);
  const callCount=await page.evaluate(()=>window.__starAladinAudit?.sourceCalls.length??0);
  assert.equal(callCount,0,"No tampered markers may be supplied to Aladin");
  console.log("PASS browser tampering rejection");
  await page.close();
} finally {await browser.close();}
