import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtemp, mkdir, readFile, writeFile, stat } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { filterSkyAssets } from "./filter-deployed-sky-assets.mjs";
import { parsePublishedSkyReleases, verifyPublishedSkyBytes } from "../src/lib/star/sky-overlay-input.ts";

const root=resolve(dirname(fileURLToPath(import.meta.url)),"../..");
const original=join(root,"data/derived/vizier/alfalfa100/2026-10-09-cds-corrected-2019/alfalfa100_hi_centroids_display_2000.csv");
const published=join(root,"web_tool/public/sky/alfalfa100-hi-centroids-v1.csv");
const manifestPath=join(root,"web_tool/content/sky-overlay-releases.v1.json");
const hash=bytes=>createHash("sha256").update(bytes).digest("hex");
const expectedSky="ddf040c5954bc9ae2c19415d46071443cd6a3f209069e095fd2b4bbe7b8fadf9";
const expectedIds="7b5de4187e24df2c0c1936164ecd1ade0ae5c4ee15d2ff64847499fd7e7c6221";

test("one ALFALFA review candidate cannot become an admitted release without review",async()=>{
  const m=JSON.parse(await readFile(manifestPath,"utf8"));
  assert.equal(m.reviewCandidates.length,1);
  assert.equal(m.reviewCandidates[0].datasetId,"DATA-VIZIER-ALFALFA100");
  assert.equal(m.reviewCandidates[0].reviewStatus,"pending_off_author_display_approval");
  assert.deepEqual(parsePublishedSkyReleases(m),[]);
});
test("real published candidate is exactly the frozen 2000 H I-centroid rows",async()=>{
  const [raw,web]=await Promise.all([readFile(original),readFile(published)]);
  assert.equal(hash(raw),expectedSky);
  assert.deepEqual(web,raw);
  const m=JSON.parse(await readFile(manifestPath,"utf8"));
  const candidate=m.reviewCandidates[0];
  assert.equal(candidate.coordinateSha256,expectedSky);
  assert.equal(candidate.selectedIdsSha256,expectedIds);
  // This positive browser test validates prospective rendering only; not approval.
  const reviewedFixture={...candidate,reviewSha256:"a".repeat(64)};
  const publishedRelease=parsePublishedSkyReleases({schemaVersion:m.schemaVersion,sources:[reviewedFixture]})[0];
  const table=await verifyPublishedSkyBytes(publishedRelease,new Uint8Array(web));
  assert.equal(table.sources.length,2000);
  assert.equal(table.coordinate_role,"hi_centroid");
  assert.ok(table.sources.every(r=>r.source_id.startsWith("AGC-")));
  const altered=Buffer.from(web);
  altered[altered.length-2]=altered[altered.length-2]===48?49:48;
  await assert.rejects(verifyPublishedSkyBytes(publishedRelease,new Uint8Array(altered)),/SHA-256 mismatch/);
  await assert.rejects(verifyPublishedSkyBytes({...publishedRelease,selectedIdsSha256:"0".repeat(64)},new Uint8Array(web)),/selected-ID chain mismatch/);
});
test("deploy filter removes a staged but unapproved CSV",async t=>{
  const tmp=await mkdtemp(join(tmpdir(),"alfalfa-filter-"));
  t.after(async()=>{const {rm}=await import("node:fs/promises");await rm(tmp,{recursive:true,force:true});});
  const publicSky=join(tmp,"sky");await mkdir(publicSky);
  await writeFile(join(publicSky,"alfalfa.csv"),"staged only");
  const rejected=await filterSkyAssets(publicSky,{schemaVersion:"star-sky-overlay-releases-v1",sources:[]});
  assert.deepEqual(rejected,{approved:0,removed:1});
  await assert.rejects(stat(join(publicSky,"alfalfa.csv")),{code:"ENOENT"});
});
test("deploy filter retains exactly approved files and rejects traversal",async t=>{
  const tmp=await mkdtemp(join(tmpdir(),"alfalfa-filter-"));
  t.after(async()=>{const {rm}=await import("node:fs/promises");await rm(tmp,{recursive:true,force:true});});
  const publicSky=join(tmp,"sky");await mkdir(publicSky);
  await writeFile(join(publicSky,"approved.csv"),"frozen");
  await writeFile(join(publicSky,"unreviewed.csv"),"candidate");
  assert.deepEqual(await filterSkyAssets(publicSky,{
    schemaVersion:"star-sky-overlay-releases-v1",
    sources:[{coordinatePath:"web_tool/public/sky/approved.csv"}],
  }),{approved:1,removed:1});
  assert.equal(await readFile(join(publicSky,"approved.csv"),"utf8"),"frozen");
  await assert.rejects(filterSkyAssets(publicSky,{
    schemaVersion:"star-sky-overlay-releases-v1",
    sources:[{coordinatePath:"web_tool/public/sky/../forbidden.csv"}],
  }),/unsafe/);
});
