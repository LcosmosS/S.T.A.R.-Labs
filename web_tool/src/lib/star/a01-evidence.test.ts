import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { a01EvidenceMetadata, buildNullHistogram, filterEvidencePoints, loadA01Evidence, sampleEvidencePoints, validateEvidenceData, verifyAndParseEvidencePayload } from "./a01-evidence.ts";

const payloadBytes = readFileSync(new URL("../../../public/evidence/a01-primary-v1.json", import.meta.url));
const raw = JSON.parse(payloadBytes.toString("utf8"));
const buffer = (bytes: Uint8Array): ArrayBuffer => Uint8Array.from(bytes).buffer;

test("browser model verifies SHA-256 before parsing and returns immutable exact-coordinate data", async () => {
  const data = await verifyAndParseEvidencePayload(buffer(payloadBytes));
  assert.equal(data.points.length, 38042);
  assert.equal(data.nullStatistics.length, 999);
  assert.equal(data.summary.observed_statistic, -114.40183841751903);
  assert.equal(data.summary.null_exceedances, 0);
  assert.equal(data.summary.p_value, 0.001);
  assert.equal(data.summary.alpha, 0.01);
  assert.equal(typeof data.points[0].delta, "string");
  assert.ok(Object.isFrozen(data));
  assert.ok(Object.isFrozen(data.points));
  assert.ok(Object.isFrozen(data.points[0]));
  assert.ok(Object.isFrozen(data.summary));
  assert.ok(Object.isFrozen(a01EvidenceMetadata.payload));
  await assert.rejects(verifyAndParseEvidencePayload(buffer(payloadBytes.subarray(0, -1))), /byte length/);
  const tampered = Buffer.from(payloadBytes);
  tampered[100] ^= 1;
  await assert.rejects(verifyAndParseEvidencePayload(buffer(tampered)), /SHA-256 mismatch/);
});

test("browser shape checks fail closed on malformed points, summary or null distribution", () => {
  for (const modify of [
    (data: typeof raw) => { data.schemaVersion = 2; },
    (data: typeof raw) => { data.points.pop(); },
    (data: typeof raw) => { data.points[0].delta = -161051; },
    (data: typeof raw) => { data.points[0].longitude = 0; },
    (data: typeof raw) => { data.points[0].label = "11a2"; },
    (data: typeof raw) => { data.points[0].rank = -1; },
    (data: typeof raw) => { data.points[0].elevation = 1; },
    (data: typeof raw) => { data.points[1] = data.points[0]; },
    (data: typeof raw) => { data.summary.p_value = 0; },
    (data: typeof raw) => { data.summary.alpha = 0.05; },
    (data: typeof raw) => { data.nullStatistics[0] = NaN; },
    (data: typeof raw) => { data.nullStatistics[0] = data.summary.observed_statistic; },
    (data: typeof raw) => { data.nullStatistics.pop(); },
  ]) {
    const changed = structuredClone(raw);
    modify(changed);
    assert.throws(() => validateEvidenceData(changed));
  }
});

test("loader rejects HTTP failures and forwards cancellation to its immutable static fetch", async () => {
  const originalFetch = globalThis.fetch;
  const controller = new AbortController();
  let receivedSignal: AbortSignal | null | undefined;
  try {
    globalThis.fetch = async (url, init) => {
      assert.equal(url, "/evidence/a01-primary-v1.json");
      receivedSignal = init?.signal;
      return new Response("unavailable", { status: 404 });
    };
    await assert.rejects(loadA01Evidence({ signal: controller.signal }), /HTTP 404/);
    assert.equal(receivedSignal, controller.signal);
    globalThis.fetch = async () => new Response(buffer(payloadBytes), { status: 200 });
    assert.equal((await loadA01Evidence()).runId, a01EvidenceMetadata.runId);
    globalThis.fetch = async () => new Response(buffer(payloadBytes.subarray(0, -1)), { status: 200 });
    await assert.rejects(loadA01Evidence(), /byte length mismatch/);
  } finally { globalThis.fetch = originalFetch; }
});

test("rank filtering and deterministic rendering samples preserve all locked evidence", () => {
  const data = validateEvidenceData(structuredClone(raw));
  const before = JSON.stringify(data.summary);
  assert.equal(filterEvidencePoints(data.points, "all"), data.points);
  for (const [rank, count] of Object.entries(a01EvidenceMetadata.rankCounts)) assert.equal(filterEvidencePoints(data.points, Number(rank)).length, count);
  const sample = sampleEvidencePoints(data.points, 6000);
  assert.equal(sample.length, 6000);
  assert.deepEqual(sample, sampleEvidencePoints(data.points, 6000));
  assert.equal(new Set(sample.map((point) => point.label)).size, 6000);
  assert.equal(sample[0], data.points[0]);
  assert.equal(sample.at(-1), data.points[Math.floor(5999 * data.points.length / 6000)]);
  assert.equal(sampleEvidencePoints(data.points, 100000), data.points);
  assert.equal(sampleEvidencePoints(filterEvidencePoints(data.points, 3), 6000).length, 1);
  assert.deepEqual(sampleEvidencePoints([], 6000), []);
  assert.throws(() => sampleEvidencePoints(data.points, 0));
  assert.throws(() => sampleEvidencePoints(data.points, 1.5));
  assert.throws(() => filterEvidencePoints(data.points, -1));
  assert.equal(data.points.length, 38042);
  assert.equal(data.nullStatistics.length, 999);
  assert.equal(JSON.stringify(data.summary), before);
});

test("null histogram includes all 999 stored realizations and handles edge values", () => {
  const data = validateEvidenceData(structuredClone(raw));
  const histogram = buildNullHistogram(data.nullStatistics);
  assert.equal(histogram.bins.length, 24);
  assert.equal(histogram.bins.reduce((sum, bin) => sum + bin.count, 0), 999);
  assert.equal(histogram.min, a01EvidenceMetadata.ranges.nullStatistic[0]);
  assert.equal(histogram.max, a01EvidenceMetadata.ranges.nullStatistic[1]);
  assert.ok(data.summary.observed_statistic > histogram.max);
  assert.deepEqual(buildNullHistogram([0, 1, 2], 2).bins.map((bin) => bin.count), [1, 2]);
  assert.equal(buildNullHistogram([1, 1], 2).bins.reduce((sum, bin) => sum + bin.count, 0), 2);
  for (const [values, bins] of [[[], 2], [[NaN], 2], [[1], 0], [[1], 201]] as [number[], number][]) assert.throws(() => buildNullHistogram(values, bins));
});
