import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, rmSync, statSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import ignore from "ignore";
import { ARTIFACT_DIRECTORY, SOURCE_FILES, PAYLOAD_PATH, METADATA_PATH, EXPECTED_SUMMARY, PRESERVATION_COMMIT, generateArtifactsFromSources, parseProjectionCSV, parseNullCSV, readPinnedSources, sha256, validateManifest, validateSummary } from "./a01-evidence-data.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const sources = await readPinnedSources(root);
const generated = generateArtifactsFromSources(sources);
const script = "web_tool/scripts/a01-evidence-data.mjs";
const sourcePaths = Object.keys(SOURCE_FILES).map((name) => `${ARTIFACT_DIRECTORY}/${name}`);
const observedLines = sources["observed_projection.csv"].toString("utf8").split("\n");
const onePoint = `${observedLines[0]}\n${observedLines[1]}\n`;

function isolatedFixture(callback, filter = () => true) {
  const tempParent = realpathSync(tmpdir());
  const fixture = mkdtempSync(join(tempParent, "star-a01-evidence-"));
  try {
    for (const path of [script, PAYLOAD_PATH, METADATA_PATH, ...sourcePaths]) {
      if (!filter(path)) continue;
      const destination = join(fixture, path);
      mkdirSync(dirname(destination), { recursive: true });
      copyFileSync(join(root, path), destination);
    }
    return callback(fixture);
  } finally {
    assert.equal(dirname(fixture), tempParent);
    assert.match(basename(fixture), /^star-a01-evidence-/);
    rmSync(fixture, { recursive: true, force: true });
  }
}
function runCheck(fixture) {
  return spawnSync(process.execPath, [join(fixture, script), "--check"], { cwd: join(fixture, "web_tool"), encoding: "utf8" });
}

test("viewer artifact bytes reproduce deterministically from the exact preserved PR #104 sources", () => {
  assert.equal(PRESERVATION_COMMIT, "f6d8bc8e954d5923ab9fa512ffcc6320d4c4018b");
  for (const [name, expected] of Object.entries(SOURCE_FILES)) {
    assert.equal(sha256(sources[name]), expected.sha256, name);
    assert.equal(sources[name].length, expected.sizeBytes, name);
  }
  const second = generateArtifactsFromSources(sources);
  assert.ok(generated.payloadBytes.equals(second.payloadBytes));
  assert.ok(generated.metadataBytes.equals(second.metadataBytes));
  assert.ok(readFileSync(join(root, PAYLOAD_PATH)).equals(generated.payloadBytes));
  assert.ok(readFileSync(join(root, METADATA_PATH)).equals(generated.metadataBytes));
  assert.equal(generated.metadata.payload.sha256, "98d3c4b9d668f2800c0b0665c20a245d9658841cc8140e6edef54a742bf53575");
  assert.equal(sha256(generated.payloadBytes), generated.metadata.payload.sha256);
  assert.equal(generated.payloadBytes.length, generated.metadata.payload.sizeBytes);
  assert.equal(generated.payload.points.length, 38042);
  assert.equal(generated.payload.nullStatistics.length, 999);
  assert.deepEqual(generated.payload.summary, EXPECTED_SUMMARY);
  assert.deepEqual(generated.metadata.rankCounts, { 0: 16450, 1: 19622, 2: 1969, 3: 1 });
  assert.equal(generated.metadata.ranges.longitude[1], 422.1547250129328);
  assert.equal(generated.metadata.coordinates.skyLocations, false);
  assert.equal(generated.metadata.interpretation.independentReplication, false);
  assert.equal(generated.metadata.interpretation.controlledSupportEligible, false);
  assert.equal(generated.metadata.interpretation.physicalSupportEligible, false);
  assert.equal(generated.metadata.interpretation.eligibilityPromotion, false);
  for (const source of generated.metadata.sources) assert.ok(source.url.includes(`/blob/${PRESERVATION_COMMIT}/`));
});

test("every source file is independently byte-pinned, including the manifest", () => {
  for (const name of Object.keys(SOURCE_FILES)) {
    const changed = { ...sources, [name]: Buffer.from(sources[name]) };
    changed[name][0] ^= 1;
    assert.throws(() => generateArtifactsFromSources(changed), /Pinned source hash\/size mismatch/);
    assert.throws(() => generateArtifactsFromSources({ ...sources, [name]: undefined }), /Pinned source hash\/size mismatch/);
  }
});

test("projection parser preserves exact discriminant text and does not clip arithmetic coordinates at 360", () => {
  const points = generated.payload.points;
  assert.ok(points.some((point) => BigInt(point.delta) > BigInt(Number.MAX_SAFE_INTEGER) || BigInt(point.delta) < -BigInt(Number.MAX_SAFE_INTEGER)));
  assert.ok(points.every((point) => typeof point.delta === "string"));
  const beyond360 = points.find((point) => point.longitude > 360);
  assert.ok(beyond360);
  const line = observedLines.find((row) => row.startsWith(`${beyond360.label},`));
  assert.deepEqual(parseProjectionCSV(`${observedLines[0]}\n${line}\n`, 1)[0], beyond360);
});

test("projection parser fails on wrong schema, duplicate class, unsafe fields and formula drift", () => {
  const cells = observedLines[1].split(",");
  const changed = (index, text) => `${observedLines[0]}\n${cells.map((cell, i) => i === index ? text : cell).join(",")}\n`;
  for (const text of [
    onePoint.replace("longitude,latitude", "ra,dec"),
    onePoint.replaceAll("\n", "\r\n"),
    onePoint.trimEnd(),
    changed(0, "11a2"), changed(1, "11b"), changed(2, "12"),
    changed(3, "0"), changed(3, "-1.2"), changed(3, "1e20"),
    changed(4, "NaN"), changed(4, "-1"), changed(5, "0"),
    changed(6, "62"), changed(7, "NaN"), changed(8, "200"),
    changed(3, '"-161051"'), changed(3, " 161051"),
  ]) assert.throws(() => parseProjectionCSV(text, 1));
  assert.throws(() => parseProjectionCSV(`${observedLines[0]}\n${observedLines[1]}\n${observedLines[1]}\n`, 2), /Duplicate/);
  assert.throws(() => parseProjectionCSV(onePoint, 38042), /observed rows/);
});

test("null parser rejects missing, duplicate, shuffled and non-finite realizations", () => {
  assert.deepEqual(parseNullCSV("realization,statistic\n1,-117.5\n", 1), [-117.5]);
  for (const text of [
    "realization,value\n1,-117.5\n", "realization,statistic\n2,-117.5\n",
    "realization,statistic\n1,NaN\n", "realization,statistic\n1,Infinity\n",
    "realization,statistic\n1,1\n", "realization,statistic\n1,\n",
  ]) assert.throws(() => parseNullCSV(text, 1));
  assert.throws(() => parseNullCSV("realization,statistic\n1,-117\n1,-118\n", 2), /sequence/);
  assert.throws(() => parseNullCSV("realization,statistic\n1,-117\n", 999), /999/);
});

test("summary and manifest checks reject altered inference, output hashes, pins and support promotion", () => {
  const { summary, nullStatistics, points } = generated.payload;
  for (const patch of [{ p_value: 0 }, { alpha: 0.05 }, { observed_statistic: 0 }, { decision: "support_acsc" }, { null_seed: 1 }]) assert.throws(() => validateSummary({ ...summary, ...patch }, nullStatistics, points));
  assert.throws(() => validateSummary(summary, [summary.observed_statistic, ...nullStatistics.slice(1)], points), /exceedance/);
  const manifest = JSON.parse(sources["manifest.json"]);
  for (const mutate of [
    (m) => { m.outputs.artifacts[0].sha256 = "0".repeat(64); },
    (m) => { m.outputs.artifacts[0].size_bytes += 1; },
    (m) => { m.outputs.missing_expected_paths.push("summary.json"); },
    (m) => { m.execution.config.projection.clip = true; },
    (m) => { m.execution.config.null.seed = 42; },
    (m) => { m.execution.config.endpoint.k = 20; },
    (m) => { m.registry.records.experiment.Physical_Support_Eligible = "true"; },
    (m) => { m.registry.records.dataset.Controlled_Support_Eligible = "true"; },
    (m) => { m.support_promotion.automatic = true; },
    (m) => { m.post_run_integrity.passed = false; },
  ]) {
    const changed = structuredClone(manifest);
    mutate(changed);
    assert.throws(() => validateManifest(changed));
  }
});

test("--check is read-only and rejects stale output instead of repairing it", () => isolatedFixture((fixture) => {
  const paths = [PAYLOAD_PATH, METADATA_PATH, ...sourcePaths];
  const before = paths.map((path) => [path, sha256(readFileSync(join(fixture, path))), statSync(join(fixture, path)).mtimeMs]);
  const clean = runCheck(fixture);
  assert.ifError(clean.error);
  assert.equal(clean.status, 0, `${clean.stdout}${clean.stderr}`);
  assert.match(clean.stdout, /38042 points, 999 nulls/);
  for (const [path, hash, modified] of before) {
    assert.equal(sha256(readFileSync(join(fixture, path))), hash);
    assert.equal(statSync(join(fixture, path)).mtimeMs, modified);
  }
  const corrupted = Buffer.from(readFileSync(join(fixture, PAYLOAD_PATH)));
  corrupted[20] ^= 1;
  writeFileSync(join(fixture, PAYLOAD_PATH), corrupted);
  const failed = runCheck(fixture);
  assert.equal(failed.status, 1);
  assert.match(failed.stderr, /Stale generated A01 viewer artifact/);
  assert.ok(readFileSync(join(fixture, PAYLOAD_PATH)).equals(corrupted));
}));

test("A01 check passes using only the four canonical inputs retained by Vercel", () => {
  const deploymentFilter = ignore().add(readFileSync(join(root, ".vercelignore"), "utf8"));
  isolatedFixture((fixture) => {
    const result = runCheck(fixture);
    assert.ifError(result.error);
    assert.equal(result.status, 0, `Filtered A01 deployment check failed:\n${result.stdout}${result.stderr}`);
  }, (path) => !deploymentFilter.ignores(path));
});
