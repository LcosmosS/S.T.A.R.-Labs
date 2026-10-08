import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {spawnSync} from "node:child_process";
const source=JSON.parse(readFileSync("content/research-content-v0.1.json","utf8"));
const snapshot=JSON.parse(readFileSync("src/lib/star/research-content-snapshot.json","utf8"));
test("source and published research snapshot agree",()=>{
  assert.equal(snapshot.readOnly,true);
  assert.deepEqual(snapshot.model,source);
  const r=spawnSync(process.execPath,["scripts/sync-research-content.mjs","--check"],{encoding:"utf8"});
  assert.equal(r.status,0,r.stderr);
});
test("no historical metric or notebook is promoted",()=>{
  assert.equal(source.externalSource.committed,false);
  for(const x of source.items){assert.ok(["model_exploratory","derived_conditional","historical_unreplicated","archive_only"].includes(x.status));assert.ok(x.caveat&&x.source);}
  assert.equal(source.items.find(x=>x.kind==="reported_result").status,"historical_unreplicated");
  assert.equal(source.items.find(x=>x.kind==="notebook").status,"archive_only");
});
test("nonnegative nonzero occupancies cannot vanish at s=1",()=>{
  const a=[0,4,2,0];const L1=a.reduce((s,c,i)=>s+c/(i+1),0);
  assert.ok(L1>0);
  assert.match(source.items.find(x=>x.id==="WEB-POS-001").caveat,/no zero at s=1/);
});
