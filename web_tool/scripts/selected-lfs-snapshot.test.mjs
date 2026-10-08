import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { project, verify } from "./sync-selected-lfs.mjs";
const input = JSON.parse(readFileSync(new URL("../../registry/recovered_lfs_selection_v0.1.json", import.meta.url)));
const output = readFileSync(new URL("../src/lib/star/recovered-lfs-snapshot.json", import.meta.url),"utf8");
const clone = () => structuredClone(input);
test("archival web snapshot matches versioned source without canonical admission", () => {
  assert.equal(verify(input),true);
  assert.equal(output,JSON.stringify(project(input), null, 2)+"\n");
});
test("reject promoted recovered assets and unverified source identity", () => {
  const a=clone();a.assets[0].physicalSupportEligible=true;assert.throws(()=>verify(a),/cannot be promoted/);
  const b=clone();b.newObjectsUploadedByThisPR=1;assert.throws(()=>verify(b),/reviewed/);
  const c=clone();c.assets[1].sha256="a".repeat(64);assert.throws(()=>verify(c),/metadata/);
  const d=clone();d.assets.push(d.assets[0]);assert.throws(()=>verify(d),/reviewed|metadata/);
});
