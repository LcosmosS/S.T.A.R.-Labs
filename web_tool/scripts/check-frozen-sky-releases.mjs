#!/usr/bin/env node
/** Conservative, release-time verification of frozen observational sky sources.
 * No approved source is bundled by default; empty list is deliberately valid.
 * This gate verifies committed receipts and bytes, not independent scientific
 * review authenticity or any arithmetic-cosmological hypothesis.
 */
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, posix, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const manifestPath = "web_tool/content/sky-overlay-releases.v1.json";
const HEX = /^[0-9a-f]{64}$/;
const SAFE_ID = /^[A-Za-z0-9_.:-]{1,96}$/;
const NUMBER = /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/;

export function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}
function requireObject(value, name) {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(name + " must be an object");
  return value;
}
function assertHash(value, name) {
  if (typeof value !== "string" || !HEX.test(value)) throw new Error(name + " must be a 64-digit lowercase SHA-256");
}
function safePath(name, prefix) {
  if (typeof name !== "string" || !name.startsWith(prefix) ||
      name.includes("\\") || name.includes("//") ||
      name.split("/").some(v => !v || v === "." || v === "..") ||
      posix.normalize(name) !== name) throw new Error("unsafe/unexpected repository path: " + name);
  return name;
}
function parseCsv(data, name) {
  const rows = [];
  let record = [], value = "", quoted = false;
  data = data.replace(/^\uFEFF/, "");
  for (let i=0; i<data.length; i++) {
    const c = data[i];
    if (c === '"') {
      if (quoted && data[i+1] === '"') {value += '"'; i++;}
      else if (quoted || value.length === 0) quoted = !quoted;
      else throw new Error(name + ": malformed CSV quoting");
    } else if (c === "," && !quoted) {record.push(value); value = "";}
    else if ((c === "\r" || c === "\n") && !quoted) {
      if (c === "\r" && data[i+1] === "\n") i++;
      record.push(value);
      if (record.some(v => v !== "")) rows.push(record);
      record=[]; value="";
    } else value += c;
  }
  if (quoted) throw new Error(name + ": unterminated CSV quote");
  record.push(value);
  if (record.some(v => v !== "")) rows.push(record);
  const header=rows.shift();
  if (!header || new Set(header).size !== header.length) throw new Error(name + ": missing/duplicate columns");
  return rows.map((values, i) => {
    if (values.length !== header.length) throw new Error(name + ": column count mismatch at row " + (i+2));
    return Object.fromEntries(header.map((key,j)=>[key,values[j]]));
  });
}
function one(rows, field, value) {
  const found=rows.filter(r=>r[field]===value);
  if (found.length!==1) throw new Error("Expected exactly one "+field+"="+value+"; found "+found.length);
  return found[0];
}
function parseSkyCSV(buf) {
  if (!Buffer.isBuffer(buf) || buf.length===0 || buf.length>1_000_000) throw new Error("sky CSV must be 1..1000000 bytes");
  const text=new TextDecoder("utf-8",{fatal:true}).decode(buf);
  const lines=text.replace(/^\uFEFF/,"").split(/\r\n|\n|\r/);
  if(lines.at(-1)==="")lines.pop();
  if(lines.shift()!=="source_id,ra_deg,dec_deg")throw new Error("sky CSV must use exactly source_id,ra_deg,dec_deg");
  if(lines.length<1||lines.length>2000)throw new Error("sky CSV source count must be 1..2000");
  const ids=[], seen=new Set();
  for(let i=0;i<lines.length;i++){
    const fields=lines[i].split(",");
    if(fields.length!==3||!SAFE_ID.test(fields[0])||seen.has(fields[0])||
       !NUMBER.test(fields[1])||!NUMBER.test(fields[2])) throw new Error("invalid/duplicate sky row "+(i+2));
    const ra=Number(fields[1]),dec=Number(fields[2]);
    if(!Number.isFinite(ra)||!Number.isFinite(dec)||ra<0||ra>=360||dec< -90||dec>90)throw new Error("out-of-range coordinates on row "+(i+2));
    ids.push(fields[0]);seen.add(fields[0]);
  }
  return ids;
}
function isGitLfsPointer(buf){
  return buf.subarray(0,120).toString("utf8").startsWith("version https://git-lfs.github.com/spec/v1");
}
function mandatory(value, name) {
  if(typeof value!=="string"||!value.trim()||/^(unknown|pending|tbd|none)$/i.test(value.trim())) throw new Error("missing "+name);
}
/** A successful call verifies immutable bytes and checks repo state.
 * The human independence of a review receipt must still be assured by
 * protected-branch review rules outside this function.
 */
export async function checkFrozenReleases({manifest, datasetCSV, provenanceCSV, readBytes}) {
  requireObject(manifest,"release manifest");
  if(manifest.schemaVersion!=="star-sky-overlay-releases-v1"||!Array.isArray(manifest.sources))
    throw new Error("unsupported release schema or missing sources");
  if(manifest.sources.length>32)throw new Error("too many released dataset scopes");
  const datasets=parseCsv(datasetCSV,"dataset registry"), provenance=parseCsv(provenanceCSV,"provenance registry");
  const accepted=new Set();
  for(const item of manifest.sources){
    requireObject(item,"source");
    const {datasetId,qualifiedDatasetId,sourceSha256,sourcePath,coordinateSha256,
      coordinatePath,selectedIdsSha256,reviewSha256,reviewPath,coordinateRole,
      versionOrRelease,provider,sourceRows}=item;
    mandatory(datasetId,"datasetId");mandatory(qualifiedDatasetId,"qualifiedDatasetId");
    if(accepted.has(datasetId))throw new Error("duplicate released dataset id");
    accepted.add(datasetId);
    [sourceSha256,coordinateSha256,selectedIdsSha256,reviewSha256].forEach((v,i)=>assertHash(v,["source","coordinates","selected IDs","review"][i]+" sha256"));
    if(!["sdss_position","hi_centroid","optical_counterpart"].includes(coordinateRole))
      throw new Error("invalid coordinate role");
    if(!Number.isInteger(sourceRows)||sourceRows<1)throw new Error("sourceRows must be a positive reviewed count");
    mandatory(versionOrRelease,"release");mandatory(provider,"provider");
    const dataset=one(datasets,"Dataset_ID",datasetId);
    const prov=one(provenance,"Dataset_ID",datasetId);
    if(qualifiedDatasetId!==dataset.Qualified_Dataset_ID || !qualifiedDatasetId.startsWith("REPO-CSV-v0.2:"))
      throw new Error("namespace mismatch");
    if(dataset.Provenance_Status!=="verified"||prov.Provenance_Status!=="verified")
      throw new Error("upstream provenance not independently admitted in both registries");
    if(prov.Provider!==provider||prov.Version_or_Release!==versionOrRelease)
      throw new Error("publisher/release differs from canonical provenance");
    for (const key of ["Source_URL","Acquisition_Date","Original_Format","License_or_Usage","Integrity_Check","Selection_Criteria"])
      mandatory(prov[key],key);
    if(!prov.Integrity_Check.toLowerCase().includes(sourceSha256))
      throw new Error("canonical provenance integrity check does not bind raw SHA256");
    safePath(sourcePath,"data/");safePath(coordinatePath,"web_tool/public/sky/");
    safePath(reviewPath,"docs/");
    const [raw,sky,reviewBytes]=await Promise.all([readBytes(sourcePath),readBytes(coordinatePath),readBytes(reviewPath)]);
    if(isGitLfsPointer(raw)||isGitLfsPointer(sky))throw new Error("unhydrated Git LFS pointer, not scientific bytes");
    if(sha256(raw)!==sourceSha256||sha256(sky)!==coordinateSha256||
       sha256(reviewBytes)!==reviewSha256)throw new Error("frozen source, sky or review digest mismatch");
    const ids=parseSkyCSV(sky);
    if(sha256(Buffer.from(ids.join("\n")+"\n","utf8"))!==selectedIdsSha256)
      throw new Error("selected IDs SHA256 mismatch");
    const review=JSON.parse(new TextDecoder("utf-8",{fatal:true}).decode(reviewBytes));
    if(review.decision!=="approved_for_display_only"||review.datasetId!==datasetId||
       review.sourceSha256!==sourceSha256||review.coordinateSha256!==coordinateSha256||
       !review.reviewerIdentity||!review.reviewedCommit)
      throw new Error("missing or mismatched reviewed sky release decision");
    if(item.controlledSupportEligible===true||item.physicalSupportEligible===true)
      throw new Error("sky display manifest cannot grant scientific or physical support");
  }
  return {acceptedDatasetIds:[...accepted].sort(), count:accepted.size};
}
async function main(){
  if(process.argv.length!==2)throw new Error("Usage: node scripts/check-frozen-sky-releases.mjs");
  const load=async name=>readFile(resolve(repoRoot,name));
  const manifest=JSON.parse((await load(manifestPath)).toString("utf8"));
  const result=await checkFrozenReleases({
    manifest,
    datasetCSV:(await load("registry/dataset_registry_v0.1.csv")).toString("utf8"),
    provenanceCSV:(await load("registry/data_provenance_registry_v0.1.csv")).toString("utf8"),
    readBytes:load,
  });
  console.log("Frozen sky release check:",result.count,"independently source-reviewed scopes admitted; display-only.");
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))
  main().catch(err=>{console.error("Sky release rejected:",err.message);process.exitCode=1;});
