#!/usr/bin/env node
/** Build a read-only website snapshot. This never changes a source registry or
 * runs an experiment. --check fails when any included repository byte changes. */
import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const target = resolve(repoRoot, "web_tool/src/lib/star/registry-snapshot.json");
const files = {
  experiments: "registry/experiment_registry_v0.2.csv",
  datasets: "registry/dataset_registry_v0.1.csv",
  provenance: "registry/data_provenance_registry_v0.1.csv",
  parameters: "registry/parameter_registry_v0.1.csv",
  nulls: "registry/null_registry_v0.1.csv",
  claims: "registry/claim_evidence_v0.2.csv",
  spec: "controlled_execution/specs/EXP-MAP-A01.json",
  config: "preregistrations/EXP-MAP-A01/config.json",
  manifest: "preregistrations/EXP-MAP-A01/dataset_manifest.json",
  protocol: "preregistrations/EXP-MAP-A01/protocol.md",
};

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

// Matches src/control/registry.py: sorted keys, compact UTF-8 JSON.
function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

function csv(text, name) {
  const rows = [];
  let row = [];
  let value = "";
  let quoted = false;
  text = text.replace(/^\uFEFF/, "");
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (char === '"') {
      if (quoted && text[i + 1] === '"') { value += '"'; i++; }
      else if (quoted || value.length === 0) quoted = !quoted;
      else throw new Error(`${name}: invalid CSV quotation`);
    } else if (char === "," && !quoted) { row.push(value); value = ""; }
    else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && text[i + 1] === "\n") i++;
      row.push(value);
      if (row.some((cell) => cell !== "")) rows.push(row);
      row = []; value = "";
    } else value += char;
  }
  if (quoted) throw new Error(`${name}: unclosed CSV quotation`);
  row.push(value);
  if (row.some((cell) => cell !== "")) rows.push(row);
  const header = rows.shift();
  if (!header || new Set(header).size !== header.length) throw new Error(`${name}: missing or duplicate CSV headers`);
  return rows.map((cells, i) => {
    if (cells.length !== header.length) throw new Error(`${name}: row ${i + 2} has ${cells.length} columns; expected ${header.length}`);
    return Object.fromEntries(header.map((key, j) => [key, cells[j]]));
  });
}

function one(rows, field, id) {
  const found = rows.filter((row) => row[field] === id);
  if (found.length !== 1) throw new Error(`Expected one ${field}=${id}; found ${found.length}`);
  return found[0];
}

function flag(row, key) {
  if (row[key] !== "true" && row[key] !== "false") throw new Error(`Invalid ${key} flag`);
  return row[key] === "true";
}

async function main() {
  if (process.argv.slice(2).some((arg) => arg !== "--check")) throw new Error("Usage: node scripts/sync-registry.mjs [--check]");
  const bytes = Object.fromEntries(await Promise.all(Object.entries(files).map(async ([key, path]) => [key, await readFile(resolve(repoRoot, path))])));
  const sources = Object.entries(files).map(([key, path]) => ({ path, sha256: sha256(bytes[key]), sizeBytes: bytes[key].length })).sort((a, b) => a.path.localeCompare(b.path));
  const tables = Object.fromEntries(["experiments", "datasets", "provenance", "parameters", "nulls", "claims"].map((key) => [key, csv(bytes[key].toString("utf8"), files[key])]));
  const spec = JSON.parse(bytes.spec.toString("utf8"));
  const config = JSON.parse(bytes.config.toString("utf8"));
  const manifest = JSON.parse(bytes.manifest.toString("utf8"));
  const experiment = one(tables.experiments, "Experiment_ID", "EXP-MAP-A01");
  const records = {
    experiment,
    dataset: one(tables.datasets, "Dataset_ID", experiment.Dataset_ID),
    provenance: one(tables.provenance, "Dataset_ID", experiment.Dataset_ID),
    parameter: one(tables.parameters, "Parameter_Set_ID", experiment.Parameter_Set_ID),
    null: one(tables.nulls, "Null_ID", experiment.Null_ID),
  };
  const recordSha256 = Object.fromEntries(Object.entries(records).map(([key, row]) => [key, sha256(canonical(row))]));
  if (canonical(recordSha256) !== canonical(spec.registry_bindings)) throw new Error("EXP-MAP-A01 controlled spec registry bindings do not match the canonical rows");
  if (canonical(config) !== canonical(spec.config)) throw new Error("EXP-MAP-A01 controlled spec configuration differs from the preregistered file");
  for (const item of spec.config_files) {
    const source = sources.find((entry) => entry.path === item.path);
    if (!source || source.sha256 !== item.sha256) throw new Error(`Preregistration file binding differs: ${item.path}`);
  }
  const snapshot = {
    schemaVersion: 1,
    namespace: "REPO-CSV-v0.2",
    readOnly: true,
    contentSha256: sha256(canonical(sources)),
    sources,
    claims: tables.claims,
    experiments: tables.experiments,
    declaredExecutionEligibleCount: tables.experiments.filter((row) => flag(row, "Controlled_Execution_Eligible")).length,
    candidate: {
      id: "EXP-MAP-A01",
      records,
      recordSha256,
      registryBindingsMatch: true,
      preregistrationFilesMatch: true,
      config,
      manifest,
      datasetInputs: spec.dataset_inputs,
      codeInputs: spec.code_inputs,
      gateState: {
        experimentExecutionEligible: flag(records.experiment, "Controlled_Execution_Eligible"),
        datasetExecutionEligible: flag(records.dataset, "Controlled_Execution_Eligible"),
        controlledSupportEligible: flag(records.experiment, "Controlled_Support_Eligible"),
        physicalSupportEligible: flag(records.experiment, "Physical_Support_Eligible"),
        provenanceStatus: records.provenance.Provenance_Status,
        parameterPreregistrationStatus: records.parameter.Preregistration_Status,
        nullPreregistrationStatus: records.null.Preregistration_Status,
      },
    },
  };
  const output = `${JSON.stringify(snapshot, null, 2)}\n`;
  if (process.argv.includes("--check")) {
    if (await readFile(target, "utf8") !== output) throw new Error("Registry website snapshot is stale. Run npm run registry:sync and review the updated snapshot.");
    console.log(`Registry snapshot matches ${sources.length} canonical source files; bindings verified; declared execution-eligible count: ${snapshot.declaredExecutionEligibleCount}.`);
  } else {
    await writeFile(target, output);
    console.log(`Wrote read-only registry snapshot (${snapshot.contentSha256}). No registry flags or experiments changed.`);
  }
}

main().catch((error) => { console.error(error.message); process.exitCode = 1; });
