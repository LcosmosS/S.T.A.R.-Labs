import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtemp, mkdir, readFile, writeFile, stat, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { filterSkyAssets } from "./filter-deployed-sky-assets.mjs";
import { parsePublishedSkyReleases, verifyPublishedSkyBytes, fetchPublishedSkyTable } from "../src/lib/star/sky-overlay-input.ts";

const root=resolve(dirname(fileURLToPath(import.meta.url)),"../..");
const original=join(root,"data/derived/vizier/alfalfa100/2026-10-09-cds-corrected-2019/alfalfa100_hi_centroids_display_2000.csv");
const published=join(root,"web_tool/public/sky/alfalfa100-hi-centroids-v1.csv");
const manifestPath=join(root,"web_tool/content/sky-overlay-releases.v1.json");
const receiptPath=join(root,"docs/registries/ALFALFA_HI_CENTROID_SKY_V1_REVIEW_RECEIPT.json");
const hash=bytes=>createHash("sha256").update(bytes).digest("hex");
const expectedSky="ddf040c5954bc9ae2c19415d46071443cd6a3f209069e095fd2b4bbe7b8fadf9";
const expectedIds="7b5de4187e24df2c0c1936164ecd1ade0ae5c4ee15d2ff64847499fd7e7c6221";
const getManifest=async()=>JSON.parse(await readFile(manifestPath,"utf8"));

test("current ALFALFA sources[0] is display-only with a bound approved receipt",async()=>{
  const m=await getManifest();
  assert.equal(m.sources.length,1);
  assert.deepEqual(m.reviewCandidates,[]);
  const release=m.sources[0];
  assert.equal(release.datasetId,"DATA-VIZIER-ALFALFA100");
  assert.equal(release.qualifiedDatasetId,"REPO-CSV-v0.2:DATA-VIZIER-ALFALFA100");
  assert.equal(release.coordinateRole,"hi_centroid");
  assert.equal(release.reviewStatus,"approved_display_only");
  assert.equal(release.controlledSupportEligible,false);
  assert.equal(release.physicalSupportEligible,false);
  assert.equal(release.coordinateSha256,expectedSky);
  assert.equal(release.selectedIdsSha256,expectedIds);
  const review=await readFile(receiptPath);
  assert.equal(hash(review),release.reviewSha256);
  const receipt=JSON.parse(review.toString("utf8"));
  assert.equal(receipt.decision,"approved_for_display_only");
  assert.equal(receipt.datasetId,release.datasetId);
  assert.equal(receipt.coordinateRole,"hi_centroid");
  assert.equal(receipt.displayRows,2000);
  assert.ok(receipt.reviewerIdentity&&receipt.reviewedCommit);
  assert.equal(parsePublishedSkyReleases(m).length,1);
});

test("admitted ALFALFA source equals original frozen 2,000 HI centroid rows",async()=>{
  const [raw,web,m]=await Promise.all([readFile(original),readFile(published),getManifest()]);
  assert.equal(hash(raw),expectedSky);
  assert.deepEqual(web,raw);
  const release=parsePublishedSkyReleases(m)[0];
  assert.equal(release.coordinatePath,"web_tool/public/sky/alfalfa100-hi-centroids-v1.csv");
  const table=await verifyPublishedSkyBytes(release,new Uint8Array(web));
  assert.equal(table.sources.length,2000);
  assert.equal(table.coordinate_role,"hi_centroid");
  assert.ok(table.sources.every(r=>r.source_id.startsWith("AGC-")));
  const actual=await fetchPublishedSkyTable(release,async(url,opts)=>{
    assert.equal(url,"/sky/alfalfa100-hi-centroids-v1.csv");
    assert.equal(opts.redirect,"error");
    assert.equal(opts.credentials,"omit");
    return new Response(web,{status:200});
  });
  assert.equal(actual.sources.length,2000);
  const altered=Buffer.from(web);
  altered[altered.length-2]=altered[altered.length-2]===48?49:48;
  await assert.rejects(verifyPublishedSkyBytes(release,new Uint8Array(altered)),/SHA-256 mismatch/);
  await assert.rejects(verifyPublishedSkyBytes({...release,selectedIdsSha256:"0".repeat(64)},new Uint8Array(web)),/selected-ID chain mismatch/);
});

test("independent pending-review fixture remains inadmissible",async()=>{
  const release=(await getManifest()).sources[0];
  const pending={...release,reviewStatus:"pending_off_author_display_approval",reviewSha256:"0".repeat(64)};
  const fixture={schemaVersion:"star-sky-overlay-releases-v1",sources:[],reviewCandidates:[pending]};
  assert.deepEqual(parsePublishedSkyReleases(fixture),[]);
  const tmp=await mkdtemp(join(tmpdir(),"alfalfa-pending-"));
  try {
    const source=join(tmp,"public"),stage=join(tmp,"stage");
    await mkdir(join(source,"sky"),{recursive:true});
    await writeFile(join(source,"sky","alfalfa.csv"),"pending only");
    const r=await filterSkyAssets(source,stage,fixture);
    assert.equal(r.approved,0);
    assert.equal(r.excluded,1);
    await assert.rejects(stat(join(stage,"sky","alfalfa.csv")),{code:"ENOENT"});
    assert.equal(await readFile(join(source,"sky","alfalfa.csv"),"utf8"),"pending only");
  } finally {await rm(tmp,{recursive:true,force:true});}
});

test("build stage copies only approved sky assets without modifying tracked sources",async()=>{
  const tmp=await mkdtemp(join(tmpdir(),"alfalfa-public-stage-"));
  try {
    const source=join(tmp,"public"),stage=join(tmp,"stage");
    await mkdir(join(source,"sky"),{recursive:true});
    await writeFile(join(source,"favicon.svg"),"<svg/>");
    await writeFile(join(source,"sky","approved.csv"),"frozen");
    await writeFile(join(source,"sky","unreviewed.csv"),"candidate");
    const fixture={schemaVersion:"star-sky-overlay-releases-v1",sources:[
      {coordinatePath:"web_tool/public/sky/approved.csv"},
    ]};
    const r=await filterSkyAssets(source,stage,fixture);
    assert.equal(r.approved,1);
    assert.equal(r.excluded,1);
    assert.equal(await readFile(join(stage,"sky","approved.csv"),"utf8"),"frozen");
    assert.equal(await readFile(join(stage,"favicon.svg"),"utf8"),"<svg/>");
    await assert.rejects(stat(join(stage,"sky","unreviewed.csv")),{code:"ENOENT"});
    assert.equal(await readFile(join(source,"sky","unreviewed.csv"),"utf8"),"candidate");
    assert.equal(await readFile(join(source,"sky","approved.csv"),"utf8"),"frozen");
    await writeFile(join(stage,"sky","stale.csv"),"generated cache");
    await filterSkyAssets(source,stage,fixture);
    await assert.rejects(stat(join(stage,"sky","stale.csv")),{code:"ENOENT"});
    await assert.rejects(filterSkyAssets(source,source,fixture),/outside the tracked public source/);
    await assert.rejects(filterSkyAssets(source,join(source,"nested"),fixture),/outside the tracked public source/);
    await assert.rejects(filterSkyAssets(source,join(tmp,"invalid"),{
      schemaVersion:fixture.schemaVersion,
      sources:[{coordinatePath:"web_tool/public/sky/../forbidden.csv"}],
    }),/unsafe/);
  } finally {await rm(tmp,{recursive:true,force:true});}
});
