import test from "node:test";
import assert from "node:assert/strict";
import { checkFrozenReleases, sha256 } from "./check-frozen-sky-releases.mjs";

const raw=Buffer.from("objid,ra,dec\n1,20,30\n");
const sky=Buffer.from("source_id,ra_deg,dec_deg\nobj:1,20,30\n");
const rawHash=sha256(raw), skyHash=sha256(sky);
function fixture() {
  const receipt=Buffer.from(JSON.stringify({
    decision:"approved_for_display_only",datasetId:"DATA-EXAMPLE",
    sourceSha256:rawHash,coordinateSha256:skyHash,
    reviewerIdentity:"reviewer-needs-independent-identity-verification",
    reviewedCommit:"a".repeat(40),
  }));
  const source={
    datasetId:"DATA-EXAMPLE",qualifiedDatasetId:"REPO-CSV-v0.2:DATA-EXAMPLE",
    provider:"Example Publisher",versionOrRelease:"v1",sourceRows:1,
    sourcePath:"data/intake/source.csv",sourceSha256:rawHash,
    coordinatePath:"web_tool/public/sky/source.csv",coordinateSha256:skyHash,
    selectedIdsSha256:sha256(Buffer.from("obj:1\n")),
    reviewPath:"docs/sky-review.json",reviewSha256:sha256(receipt),
    coordinateRole:"sdss_position",controlledSupportEligible:false,physicalSupportEligible:false,
  };
  const files={
    "data/intake/source.csv":raw,"web_tool/public/sky/source.csv":sky,
    "docs/sky-review.json":receipt,
  };
  return {
    manifest:{schemaVersion:"star-sky-overlay-releases-v1",sources:[source]},
    datasetCSV:"Dataset_ID,Qualified_Dataset_ID,Provenance_Status\nDATA-EXAMPLE,REPO-CSV-v0.2:DATA-EXAMPLE,verified\n",
    provenanceCSV:"Dataset_ID,Provider,Version_or_Release,Source_URL,Acquisition_Date,Original_Format,License_or_Usage,Integrity_Check,Selection_Criteria,Provenance_Status\nDATA-EXAMPLE,Example Publisher,v1,https://example.org,2026-10-08,CSV,CC0,SHA256="+rawHash+",one row,verified\n",
    files,readBytes:async name=>{ if(!(name in files))throw new Error("missing file");return files[name]; },
  };
}
test("empty manifest admits no source and is the required default",async()=>{
  const f=fixture();f.manifest.sources=[];
  assert.deepEqual(await checkFrozenReleases(f),{acceptedDatasetIds:[],count:0});
});
test("complete synthetic display-only hash chain accepted structurally",async()=>{
  assert.deepEqual(await checkFrozenReleases(fixture()),{acceptedDatasetIds:["DATA-EXAMPLE"],count:1});
});
test("unknown provenance rejects even if user supplies expected hash",async()=>{
  const f=fixture();f.datasetCSV=f.datasetCSV.replace("verified\n","unknown\n");
  await assert.rejects(checkFrozenReleases(f),/upstream provenance/);
});
test("tampering with raw source or review receipt fails closed",async()=>{
  const a=fixture();a.files["data/intake/source.csv"]=Buffer.from("tampered");
  await assert.rejects(checkFrozenReleases(a),/digest mismatch/);
  const b=fixture();b.files["docs/sky-review.json"]=Buffer.from("{}");
  await assert.rejects(checkFrozenReleases(b),/digest mismatch/);
});
test("projection is rejected when nonfinite or outside ICRS range",async()=>{
  const f=fixture(),wrong=Buffer.from("source_id,ra_deg,dec_deg\nX,360,30\n");
  f.files["web_tool/public/sky/source.csv"]=wrong;
  f.manifest.sources[0].coordinateSha256=sha256(wrong);
  await assert.rejects(checkFrozenReleases(f),/out-of-range/);
});
test("namespace and admission flags cannot be spoofed",async()=>{
  const a=fixture();a.manifest.sources[0].qualifiedDatasetId="STAR-PDF-v0.2:DATA-EXAMPLE";
  await assert.rejects(checkFrozenReleases(a),/namespace mismatch/);
  const b=fixture();b.manifest.sources[0].controlledSupportEligible=true;
  await assert.rejects(checkFrozenReleases(b),/cannot grant scientific/);
});
