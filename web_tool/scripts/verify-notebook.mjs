import assert from "node:assert/strict";
import { checkedUrl } from "./browser-guard.mjs";
import { captureSnapshotState, DEMO_VERSION } from "../src/lib/star/snapshots.ts";

const origin = checkedUrl(process.argv[2] || "http://127.0.0.1:8080");
const state = captureSnapshotState({
  lambdaQ: 1, alphaPhi: 0.22, alphaA: 0.12, betaQ: 0.35, lambdaScale: 1,
  topologyOn: true, conformalOn: true, freezeY: false, windingU: 1, windingV: 1,
  beta: 0.48, gamma: 0.22, pressure: 0, z: 1.23, selectedLabel: "37.a1",
  mappingFamily: "ptd", provenance: "synthetic", showFilaments: true, colorMode: "rank", rankLift: false,
});
async function request(path, body) {
  const response = await fetch(new URL(path, origin), body === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
  return { status: response.status, body: await response.json() };
}
const health = await request("/api/health");
assert.equal(health.status, 200);
assert.equal(health.body.storage, "neon"); assert.equal(health.body.durable, true);
const payload = { demoVersion: DEMO_VERSION, state };
const first = await request("/api/snapshots", payload);
assert.ok([200, 201].includes(first.status), JSON.stringify(first.body));
const saved = first.body.snapshot;
assert.deepEqual(saved.state, state);
assert.match(saved.checksum, /^[a-f0-9]{64}$/);
const loaded = await request(`/api/snapshots/${saved.id}`);
assert.equal(loaded.status, 200); assert.deepEqual(loaded.body.snapshot, saved);
const duplicate = await request("/api/snapshots", payload);
assert.equal(duplicate.status, 200); assert.equal(duplicate.body.snapshot.id, saved.id);
const invalid = await request("/api/snapshots", { ...payload, state: { ...state, Controlled_Execution_Eligible: true } });
assert.equal(invalid.status, 400);
const wrongVersion = await request("/api/snapshots", { ...payload, demoVersion: "EXP-MAP-A01" });
assert.equal(wrongVersion.status, 400);
assert.equal((await request("/api/snapshots", "x".repeat(5000))).status, 413);
assert.equal((await request("/api/snapshots/not-a-uuid")).status, 400);
assert.equal((await request("/api/snapshots/00000000-0000-4000-8000-000000000000")).status, 404);
const list = await request("/api/snapshots");
assert.equal(list.status, 200); assert.equal(list.body.durable, true);
assert.ok(list.body.snapshots.length <= 20);
assert.ok(list.body.snapshots.some((item) => item.id === saved.id));
console.log(JSON.stringify({ ok: true, storage: "neon", durable: true, snapshotId: saved.id,
  verified: ["schema readiness", "save", "load", "deduplication", "bounded list", "input gates", "body limit", "missing IDs"] }));
