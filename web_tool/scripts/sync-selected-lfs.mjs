#!/usr/bin/env node
/** Fail-closed standalone web snapshot of already uploaded LFS source SELECTION, never canonical admission. */
import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const source = resolve(root, "registry/recovered_lfs_selection_v0.1.json");
const target = resolve(root, "web_tool/src/lib/star/recovered-lfs-snapshot.json");
export function verify(record) {
  if (record.schemaVersion !== "0.1" || record.newObjectsUploadedByThisPR !== 0 ||
      record.selectionStatus !== "reuse_prior_independently_verified_lfs_objects_no_new_uploads" ||
      !Array.isArray(record.assets) || record.assets.length !== 5) throw new Error("Not a reviewed archival selection");
  const paths = new Set();
  for (const a of record.assets) {
    if (typeof a.path !== "string" ||
        !/^data\/intake\/recovered\/2026-10-08\/[0-9a-f]{64}\.(csv|fits)$/.test(a.path) ||
        paths.has(a.path) || !/^[a-f0-9]{64}$/.test(a.sha256) ||
        a.path.split("/").at(-1).split(".")[0] !== a.sha256 ||
        !Number.isSafeInteger(a.bytes) || a.bytes <= 0) throw new Error("Invalid archival LFS metadata");
    paths.add(a.path);
    if (["controlledExecutionEligible","controlledSupportEligible","physicalSupportEligible"].some(k => a[k] !== false))
      throw new Error("Recovered asset cannot be promoted by website");
  }
  return true;
}
export function project(record) {
  verify(record);
  return { schemaVersion: 1, selectionStatus: record.selectionStatus, sourcePath: "registry/recovered_lfs_selection_v0.1.json", readOnly: true, assets: record.assets };
}
async function main() {
  if (process.argv.slice(2).some(s => s !== "--check")) throw Error("Usage: node sync-selected-lfs.mjs [--check]");
  const obj = JSON.parse(await readFile(source, "utf8"));
  const expected = JSON.stringify(project(obj), null, 2) + "\n";
  if (process.argv.includes("--check")) {
    if (expected !== await readFile(target, "utf8")) throw Error("Recovered LFS web snapshot stale");
    console.log("Recovered archival LFS selection snapshot verified; 5 ineligible assets.");
  } else {
    await writeFile(target, expected);
    console.log("Wrote recovered archival LFS selection snapshot.");
  }
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url))
  main().catch(e => { console.error(e.message); process.exitCode = 1; });
