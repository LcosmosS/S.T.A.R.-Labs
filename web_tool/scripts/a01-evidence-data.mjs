#!/usr/bin/env node
/** Read-only derivation of viewer data from the exact PR #104 preservation bytes.
 * This does not execute EXP-MAP-A01, re-fit parameters, or update any registry.
 */
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const PRESERVATION_COMMIT = "f6d8bc8e954d5923ab9fa512ffcc6320d4c4018b";
export const RUN_ID = "20261016T041335361140Z-e60fd05117fc";
export const ARTIFACT_DIRECTORY = `release_packages/EXP-MAP-A01-primary-execution-v0.1/${RUN_ID}`;
export const SOURCE_FILES = Object.freeze({
  "observed_projection.csv": { sha256: "00d9d7fee63aabab80bb96172d694a39a53843741eef665c5d276ed1c37c08bb", sizeBytes: 2812267 },
  "null_statistics.csv": { sha256: "8463993ec291635671e5ac8a9195539c3faa2ba8decaf280b02d086e9a38308f", sizeBytes: 23768 },
  "summary.json": { sha256: "d390949bc9adb222a094c1cf733545f9800d269aa05db7aa50afadc874438981", sizeBytes: 657 },
  "manifest.json": { sha256: "8a85f37958b5a2337fea40b02a69c5a521e5e599a9a13987524e2d40f5608cdb", sizeBytes: 46163 },
});
export const EXPECTED_SUMMARY = Object.freeze({
  alpha: 0.01,
  analysis_rows: 38042,
  decision: "reject_null",
  experiment_id: "EXP-MAP-A01",
  interpretation_limit: "This endpoint tests local rank/elevation coherence against the locked rank-permutation null only; it does not establish ACSC or physical support.",
  isogeny_policy: "curve_number_equals_1_per_isogeny_class",
  neighbor_k: 10,
  null_exceedances: 0,
  null_prng: "splitmix64-fisher-yates-v1",
  null_realizations: 999,
  null_seed: 1729,
  observed_statistic: -114.40183841751903,
  p_value: 0.001,
  protocol_version: "EXP-MAP-A01-prereg-v1",
  source_rows: 64687,
  undirected_edge_count: 221930,
});
export const PAYLOAD_PATH = "web_tool/public/evidence/a01-primary-v1.json";
export const METADATA_PATH = "web_tool/src/lib/star/a01-evidence-metadata.json";
export const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

function csvRows(text, header) {
  if (typeof text !== "string" || text.includes("\r") || !text.endsWith("\n")) throw new Error("Expected exact LF-terminated CSV");
  const rows = text.slice(0, -1).split("\n");
  if (rows.shift() !== header) throw new Error("Unexpected CSV header or column order");
  return rows.map((line) => {
    const cells = line.split(",");
    if (cells.length !== header.split(",").length || cells.some((cell) => !cell || cell.trim() !== cell || /["\r]/.test(cell))) throw new Error("Malformed CSV row");
    return cells;
  });
}
function integer(text, name, minimum = 0) {
  if (!/^(0|[1-9]\d*)$/.test(text) || !Number.isSafeInteger(Number(text)) || Number(text) < minimum) throw new Error(`Invalid ${name}`);
  return Number(text);
}
function finite(text, name) {
  if (!/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:e[+-]?\d+)?$/i.test(text) || !Number.isFinite(Number(text))) throw new Error(`Invalid ${name}`);
  return Number(text);
}
function near(actual, expected, name) {
  if (Math.abs(actual - expected) > 1e-10) throw new Error(`Projection formula mismatch: ${name}`);
}

export function parseProjectionCSV(text, expectedRows = EXPECTED_SUMMARY.analysis_rows) {
  const rows = csvRows(text, "label,isogeny_class,conductor,delta,rank,torsion_order,longitude,latitude,elevation");
  if (rows.length !== expectedRows) throw new Error(`Expected ${expectedRows} observed rows`);
  const labels = new Set();
  const classes = new Set();
  return rows.map(([label, isogeny_class, conductorText, delta, rankText, torsionText, lonText, latText, elevationText]) => {
    if (!/^[1-9]\d*[a-z]+1$/.test(label) || !/^[1-9]\d*[a-z]+$/.test(isogeny_class) || label !== `${isogeny_class}1`) throw new Error("Invalid curve-number-1 identity");
    if (labels.has(label) || classes.has(isogeny_class)) throw new Error("Duplicate curve label or isogeny class");
    labels.add(label); classes.add(isogeny_class);
    const conductor = integer(conductorText, "conductor", 1);
    if (conductor < 11 || conductor > 9999) throw new Error("Conductor outside the locked source range");
    if (Number(label.match(/^\d+/)?.[0]) !== conductor) throw new Error("Conductor/identity mismatch");
    // Discriminants are exact integers, including values beyond Number.MAX_SAFE_INTEGER.
    if (!/^-?[1-9]\d*$/.test(delta)) throw new Error("Invalid exact discriminant string");
    const deltaInteger = BigInt(delta);
    const magnitude = Number(deltaInteger < 0n ? -deltaInteger : deltaInteger);
    if (!Number.isFinite(magnitude)) throw new Error("Discriminant magnitude is not finite");
    const rank = integer(rankText, "rank");
    const torsion_order = integer(torsionText, "torsion order", 1);
    const longitude = finite(lonText, "longitude");
    const latitude = finite(latText, "latitude");
    const elevation = finite(elevationText, "elevation");
    near(longitude, 360 * Math.log(magnitude) / Math.log(1e30), "longitude");
    near(latitude, 180 * Math.log(conductor) / Math.log(1e9), "latitude");
    near(elevation, 200 * rank, "elevation");
    return { label, isogeny_class, conductor, delta, rank, torsion_order, longitude, latitude, elevation };
  });
}

export function parseNullCSV(text, expectedRows = EXPECTED_SUMMARY.null_realizations) {
  const rows = csvRows(text, "realization,statistic");
  if (rows.length !== expectedRows) throw new Error(`Expected ${expectedRows} null realizations`);
  return rows.map(([id, statistic], index) => {
    if (integer(id, "realization", 1) !== index + 1) throw new Error("Null realization sequence must be 1 through B with no omissions");
    const value = finite(statistic, "null statistic");
    if (value > 0) throw new Error("Negative absolute-difference statistic must be non-positive");
    return value;
  });
}

export function validateSummary(summary, nullStatistics, points) {
  assert.deepEqual(summary, EXPECTED_SUMMARY, "Summary differs from the pinned primary execution");
  if (points.length !== summary.analysis_rows || nullStatistics.length !== summary.null_realizations) throw new Error("Summary row count mismatch");
  const exceedances = nullStatistics.filter((value) => value >= summary.observed_statistic).length;
  if (exceedances !== summary.null_exceedances || summary.p_value !== (1 + exceedances) / (nullStatistics.length + 1)) throw new Error("Summary exceedance / one-sided p-value mismatch");
  if (!(summary.p_value <= summary.alpha) || summary.decision !== "reject_null") throw new Error("Summary decision mismatch");
}

export function validateManifest(manifest) {
  if (manifest.schema_version !== "1.0" || manifest.experiment_id !== "EXP-MAP-A01" || manifest.run_id !== RUN_ID || manifest.null_id !== "NULL-MAP-001" || manifest.parameter_set_id !== "PAR-MAP-001") throw new Error("Manifest identity mismatch");
  if (manifest.mode !== "primary" || manifest.transaction_status !== "completed" || manifest.exit_status !== 0 || manifest.runner_exit_status !== 0 || manifest.git?.dirty !== false || manifest.post_run_integrity?.passed !== true || manifest.post_run_integrity?.failures?.length !== 0) throw new Error("Manifest does not record a clean completed primary run");
  if (manifest.git.sha !== "1b0f2d7853608bfbab79cf2dc04b002f1f193eb2" || manifest.support_promotion?.automatic !== false) throw new Error("Execution source/promotion mismatch");
  assert.deepEqual(manifest.outputs?.missing_expected_paths, []);
  assert.deepEqual([...manifest.outputs.expected_paths].sort(), ["null_statistics.csv", "observed_projection.csv", "summary.json"]);
  if (manifest.outputs.artifacts.length !== 3) throw new Error("Unexpected manifest output count");
  for (const name of ["observed_projection.csv", "null_statistics.csv", "summary.json"]) {
    const artifacts = manifest.outputs.artifacts.filter((item) => item.path === name);
    if (artifacts.length !== 1 || artifacts[0].sha256 !== SOURCE_FILES[name].sha256 || artifacts[0].size_bytes !== SOURCE_FILES[name].sizeBytes) throw new Error(`Manifest output hash/size mismatch: ${name}`);
  }
  const config = manifest.execution?.config;
  assert.deepEqual(config?.projection, { clip: false, conductor_max: "1e9", delta_max: "1e30", latitude_scale_degrees: 180, logarithm: "natural", longitude_scale_degrees: 360, rank_scale: 200, regulator_used: false });
  assert.deepEqual(config?.inference, { alpha: 0.01, multiple_testing: "none_single_endpoint", p_value: "(1 + count(T_null >= T_obs)) / (B + 1)", sidedness: "one-sided" });
  if (config?.endpoint?.k !== 10 || config.endpoint.statistic !== "negative_mean_absolute_elevation_difference" || config.endpoint.direction !== "greater_or_equal_is_more_extreme" || config.endpoint.tie_break !== "cremona_label_ascii" || config.null?.realizations !== 999 || config.null.seed !== 1729 || config.null.prng !== "splitmix64-fisher-yates-v1" || config.input?.analysis_rows !== 38042 || config.input.source_rows !== 64687 || config.input.selection !== "curve_number_equals_1_per_isogeny_class") throw new Error("Pinned parameter mismatch");
  for (const record of [manifest.registry?.records?.dataset, manifest.registry?.records?.experiment]) {
    if (record?.Controlled_Support_Eligible !== "false" || record?.Physical_Support_Eligible !== "false") throw new Error("Manifest support eligibility must remain false");
  }
}

export function generateArtifactsFromSources(sources) {
  for (const [name, expected] of Object.entries(SOURCE_FILES)) {
    const bytes = sources[name];
    if (!Buffer.isBuffer(bytes) || bytes.length !== expected.sizeBytes || sha256(bytes) !== expected.sha256) throw new Error(`Pinned source hash/size mismatch: ${name}`);
  }
  const points = parseProjectionCSV(sources["observed_projection.csv"].toString("utf8"));
  const nullStatistics = parseNullCSV(sources["null_statistics.csv"].toString("utf8"));
  const summary = JSON.parse(sources["summary.json"].toString("utf8"));
  const manifest = JSON.parse(sources["manifest.json"].toString("utf8"));
  validateSummary(summary, nullStatistics, points);
  validateManifest(manifest);
  const payload = { schemaVersion: 1, experimentId: "EXP-MAP-A01", runId: RUN_ID, points, nullStatistics, summary };
  const payloadBytes = Buffer.from(`${JSON.stringify(payload)}\n`);
  const repository = "https://github.com/LcosmosS/S.T.A.R.-Labs";
  const preserved = `${repository}/blob/${PRESERVATION_COMMIT}`;
  const rankCounts = Object.fromEntries([...new Set(points.map((point) => point.rank))].sort((a, b) => a - b).map((rank) => [rank, points.filter((point) => point.rank === rank).length]));
  const range = (values) => [Math.min(...values), Math.max(...values)];
  const metadata = {
    schemaVersion: 1, experimentId: "EXP-MAP-A01", runId: RUN_ID,
    protocolVersion: summary.protocol_version, nullId: "NULL-MAP-001", parameterSetId: "PAR-MAP-001", datasetId: "DATA-ARITHMETIC",
    artifactDirectory: ARTIFACT_DIRECTORY, preservationCommit: PRESERVATION_COMMIT, executionCommit: manifest.git.sha,
    sourceCommit: "25cec5ecfec8b9f016eb1631ac633194c2bed39f", sourceSha256: "259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968",
    sourceRows: summary.source_rows, analysisRows: points.length, nullRealizations: nullStatistics.length,
    observedStatistic: summary.observed_statistic, nullExceedances: summary.null_exceedances, pValue: summary.p_value, alpha: summary.alpha,
    payload: { url: "/evidence/a01-primary-v1.json", sha256: sha256(payloadBytes), sizeBytes: payloadBytes.length },
    sources: Object.entries(SOURCE_FILES).map(([name, identity]) => ({ name, path: `${ARTIFACT_DIRECTORY}/${name}`, ...identity, url: `${preserved}/${ARTIFACT_DIRECTORY}/${name}`, rawUrl: `https://raw.githubusercontent.com/LcosmosS/S.T.A.R.-Labs/${PRESERVATION_COMMIT}/${ARTIFACT_DIRECTORY}/${name}` })),
    links: { pullRequest: `${repository}/pull/104`, preservationCommit: `${repository}/commit/${PRESERVATION_COMMIT}`, executionCommit: `${repository}/commit/${manifest.git.sha}`, upstream: "https://github.com/JohnCremona/ecdata/tree/25cec5ecfec8b9f016eb1631ac633194c2bed39f", protocol: `${preserved}/preregistrations/EXP-MAP-A01/protocol.md`, package: `${preserved}/release_packages/EXP-MAP-A01-primary-execution-v0.1/README.md` },
    coordinates: { longitude: "360 × ln(|Δ|) / ln(10^30)", latitude: "180 × ln(N) / ln(10^9)", elevation: "200 × r", units: "arithmetic coordinate degrees; elevation in rank × 200", skyLocations: false },
    pinnedParameters: { neighborK: 10, rankScale: 200, seed: 1729, realizations: 999, prng: "splitmix64-fisher-yates-v1", pValueFormula: "(1 + count(T_null >= T_obs)) / (B + 1)", sidedness: "one-sided", normalization: "fixed constants 10^30 and 10^9; natural logarithms", clipping: false },
    interpretation: { scope: "Rejects only the locked arithmetic rank-permutation NULL-MAP-001 at alpha = 0.01.", limits: ["Arithmetic coordinates are not observed sky locations.", "The release records one primary execution; no independent replication is established.", "This result does not establish ACSC or physical support.", "Viewer filtering and deterministic sampling change rendering only, never the locked statistic, null distribution, p-value, parameters, or registry eligibility."], independentReplication: false, controlledSupportEligible: false, physicalSupportEligible: false, eligibilityPromotion: false },
    rankCounts,
    ranges: { longitude: range(points.map((point) => point.longitude)), latitude: range(points.map((point) => point.latitude)), elevation: range(points.map((point) => point.elevation)), nullStatistic: range(nullStatistics) },
  };
  return { payload, metadata, payloadBytes, metadataBytes: Buffer.from(`${JSON.stringify(metadata, null, 2)}\n`) };
}

export async function readPinnedSources(root) {
  return Object.fromEntries(await Promise.all(Object.keys(SOURCE_FILES).map(async (name) => [name, await readFile(resolve(root, ARTIFACT_DIRECTORY, name))])));
}

export async function syncA01Evidence({ root = resolve(dirname(fileURLToPath(import.meta.url)), "../.."), check = false } = {}) {
  const artifacts = generateArtifactsFromSources(await readPinnedSources(root));
  for (const [relative, bytes] of [[PAYLOAD_PATH, artifacts.payloadBytes], [METADATA_PATH, artifacts.metadataBytes]]) {
    const path = resolve(root, relative);
    if (check) {
      let current;
      try { current = await readFile(path); } catch { throw new Error(`Missing generated A01 viewer artifact: ${relative}`); }
      if (!current.equals(bytes)) throw new Error(`Stale generated A01 viewer artifact: ${relative}; run npm run evidence:sync`);
    } else {
      await mkdir(dirname(path), { recursive: true });
      await writeFile(path, bytes);
    }
  }
  return artifacts.metadata;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  if (args.some((arg) => arg !== "--check") || args.length > 1) throw new Error("Usage: node scripts/a01-evidence-data.mjs [--check]");
  syncA01Evidence({ check: args.includes("--check") }).then((metadata) => {
    console.log(`A01 viewer artifacts ${args.includes("--check") ? "verified" : "generated"}: ${metadata.analysisRows} points, ${metadata.nullRealizations} nulls; SHA-256 ${metadata.payload.sha256}`);
  }).catch((error) => { console.error(error.message); process.exitCode = 1; });
}
