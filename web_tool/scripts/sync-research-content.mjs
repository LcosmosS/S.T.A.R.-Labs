#!/usr/bin/env node
/** Deterministic, independently versioned educational-content snapshot. */
import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const input = resolve(root, "web_tool/content/research-content.v1.json");
const output = resolve(root, "web_tool/src/lib/star/research-content-snapshot.json");
const STATUSES = new Set(["illustrative_model", "historical_exploratory", "derived_mathematics", "archival_reference"]);
const KINDS = new Set(["projection", "diagram", "formula", "reduction", "notebook"]);

export function validate(model) {
  if (!model || model.schemaVersion !== 1 || model.version !== "2026-10-08.v1" ||
      model.governingCharter !== "charter/STAR_Research_Charter_v0-2.pdf" ||
      !Array.isArray(model.entries) || model.entries.length === 0) throw new Error("Invalid research content model");
  const ids = new Set();
  for (const item of model.entries) {
    if (!/^[A-Z][A-Z0-9-]{3,64}$/.test(item.id) || ids.has(item.id)) throw new Error("Duplicate or invalid research ID");
    ids.add(item.id);
    if (!KINDS.has(item.kind) || !STATUSES.has(item.status) || !["D", "M", "H", "S"].includes(item.epistemic))
      throw new Error("Unknown kind, epistemic category or evidence status");
    if (item.status === "derived_mathematics" && item.epistemic !== "D")
      throw new Error("Mathematical derivation status requires D classification");
    if (item.status === "archival_reference" && item.kind !== "notebook")
      throw new Error("Archive status cannot imply active model or result");
    if (["controlledExecutionEligible", "controlledSupportEligible", "physicalSupportEligible"].some(key => item[key] !== false))
      throw new Error("Research showcase cannot grant scientific support or execution");
    for (const key of ["title", "expression", "description", "caveat"]) {
      if (typeof item[key] !== "string" || !item[key].trim() || item[key].length > 1200) throw new Error("Missing or excessive content text");
    }
    if (typeof item.sourcePath !== "string" || !/^(charter|preregistrations|historical|experiments|web_tool)\//.test(item.sourcePath) ||
        item.sourcePath.includes("..") || item.sourcePath.includes("\\") || item.sourcePath.includes("?") || item.sourcePath.includes("#"))
      throw new Error("Unsafe source path");
    if (!Array.isArray(item.steps) || item.steps.length > 8 || item.steps.some(s => typeof s !== "string" || s.length > 120))
      throw new Error("Invalid diagram steps");
    if (item.kind === "diagram" && item.steps.length < 3)
      throw new Error("Diagram requires labeled steps");
    if (item.kind !== "diagram" && item.steps.length)
      throw new Error("Only diagrams may provide diagram steps");
  }
  return true;
}

export function snapshotOf(model) {
  validate(model);
  return { schemaVersion: 1, version: model.version, governingCharter: model.governingCharter, readOnly: true, entries: model.entries };
}

async function main() {
  if (process.argv.slice(2).some(x => x !== "--check")) throw new Error("Usage: node scripts/sync-research-content.mjs [--check]");
  const model = JSON.parse(await readFile(input, "utf8"));
  const out = JSON.stringify(snapshotOf(model), null, 2) + "\n";
  if (process.argv.includes("--check")) {
    if (await readFile(output, "utf8") !== out) throw new Error("Research content snapshot stale. Run npm run research:sync.");
    console.log("Research content snapshot verified: " + model.entries.length + " classified entries; no physical claims promoted.");
  } else {
    await writeFile(output, out);
    console.log("Wrote read-only research content snapshot.");
  }
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url))
  main().catch(e => { console.error(e.message); process.exitCode = 1; });
