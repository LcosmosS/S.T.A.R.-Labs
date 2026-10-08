#!/usr/bin/env node
// Run against a built or development preview: node scripts/research-browser-smoke.mjs http://127.0.0.1:8081
import {chromium} from "playwright";
import {checkedUrl} from "./browser-guard.mjs";
if(!process.argv[2])throw Error("Provide an accessible preview URL");
const target=new URL("/registry",checkedUrl(process.argv[2])).href;
const browser=await chromium.launch({headless:true,args:["--no-sandbox","--disable-dev-shm-usage"]});
try{
 for(const viewport of [{width:1280,height:800},{width:390,height:844}]){
  const page=await browser.newPage({viewport});
  const errors=[];page.on("pageerror",e=>errors.push(e.message));
  page.on("console",m=>{if(m.type()==="error")errors.push(m.text());});
  const res=await page.goto(target,{waitUntil:"domcontentloaded",timeout:45000});
  await page.getByRole("heading",{name:"Curated research constructions"}).waitFor();
  await page.getByText("Historical five-fold SFR MSE").waitFor();
  const cards=await page.locator("[data-research-entry]").count();
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth+1);
  if(res?.status()!==200||cards!==10||overflow||errors.length)throw Error(JSON.stringify({viewport,cards,overflow,errors,status:res?.status()}));
  console.log(JSON.stringify({viewport,cards,overflow,consoleErrors:errors.length,status:res.status()}));
  await page.close();
 }
} finally {await browser.close();}
