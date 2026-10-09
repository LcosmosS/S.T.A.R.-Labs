import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { parsePublishedSkyReleases, verifyPublishedSkyBytes, fetchPublishedSkyTable } from "../src/lib/star/sky-overlay-input.ts";

const hash = b => createHash("sha256").update(b).digest("hex");
function releaseFixture() {
  const bytes = new TextEncoder().encode("source_id,ra_deg,dec_deg\nHI:1,359.999,-1\nHI:2,0.001,1\n");
  const release = {
    datasetId: "DATA-MANGA-HI-ALL", qualifiedDatasetId: "REPO-CSV-v0.2:DATA-MANGA-HI-ALL",
    coordinatePath: "web_tool/public/sky/reviewed.v1.csv", coordinateSha256: hash(bytes),
    selectedIdsSha256: hash(Buffer.from("HI:1\nHI:2\n")),
    sourceSha256: "a".repeat(64), reviewSha256: "b".repeat(64),
    coordinateRole: "hi_centroid", sourceRows: 6632,
    controlledSupportEligible: false, physicalSupportEligible: false,
  };
  return { bytes, release };
}
test("production sky release list is intentionally empty and contains no user-provided scope", () => {
  assert.deepEqual(parsePublishedSkyReleases({schemaVersion: "star-sky-overlay-releases-v1",sources:[]}), []);
});
test("reject spoofed namespace, path traversal, duplicate identifiers or promotion", () => {
  const {release} = releaseFixture();
  const wrap = sources => parsePublishedSkyReleases({schemaVersion:"star-sky-overlay-releases-v1",sources});
  assert.equal(wrap([release]).length, 1);
  assert.throws(() => wrap([{...release, qualifiedDatasetId:"STAR-PDF-v0.2:DATA-MANGA-HI-ALL"}]), /unqualified/);
  assert.throws(() => wrap([{...release, coordinatePath:"web_tool/public/sky/../secret.csv"}]), /Unsafe/);
  assert.throws(() => wrap([release,release]), /duplicated/);
  assert.throws(() => wrap([{...release, controlledSupportEligible:true}]), /promotion/);
});
test("fetch and browser digest verify only committed coordinate bytes and IDs", async () => {
  const {bytes,release} = releaseFixture();
  const approved = parsePublishedSkyReleases({schemaVersion:"star-sky-overlay-releases-v1",sources:[release]})[0];
  const result = await verifyPublishedSkyBytes(approved,bytes);
  assert.equal(result.dataset_id,release.datasetId);
  assert.equal(result.coordinate_role,"hi_centroid");
  assert.deepEqual(result.sources.map(s=>s.source_id),["HI:1","HI:2"]);
  const called = [];
  const remote = await fetchPublishedSkyTable(approved,async (url,init)=>{
    called.push([url,init]);
    return new Response(bytes,{status:200});
  });
  assert.equal(remote.sha256,release.coordinateSha256);
  assert.equal(called[0][0],"/sky/reviewed.v1.csv");
  assert.equal(called[0][1].redirect,"error");
  assert.equal(called[0][1].credentials,"omit");
});
test("reject modified coordinates, forged ID digests, oversized or redirected bytes", async () => {
  const {bytes,release} = releaseFixture();
  const tampered = new TextEncoder().encode("source_id,ra_deg,dec_deg\nHI:1,359.998,-1\nHI:2,0.001,1\n");
  await assert.rejects(verifyPublishedSkyBytes(release,tampered),/SHA-256 mismatch/);
  await assert.rejects(verifyPublishedSkyBytes({...release,selectedIdsSha256:"0".repeat(64)},bytes),/selected-ID chain mismatch/);
  await assert.rejects(verifyPublishedSkyBytes(release,new Uint8Array(1_000_001)),/exceeds/);
  await assert.rejects(fetchPublishedSkyTable(release,async ()=>new Response(null,{status:404})),/unavailable/);
});
