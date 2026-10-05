import { test } from "node:test";
import assert from "node:assert/strict";
import { captureSnapshotState, DEMO_VERSION, snapshotInputSchema } from "./snapshots.ts";
const state = {
  lambdaQ: 1, alphaPhi: 0.22, alphaA: 0.12, betaQ: 0.35, lambdaScale: 1,
  topologyOn: true, conformalOn: true, freezeY: false, windingU: 1, windingV: 1,
  beta: 0.48, gamma: 0.22, pressure: 0, z: 0, selectedLabel: "37.a1",
  mappingFamily: "acsc", provenance: "all", showFilaments: true, colorMode: "rank", rankLift: false,
};
test("capture excludes store methods and evidence fields", () => {
  assert.deepEqual(captureSnapshotState({ ...state, set() {}, executionEligible: true }), state);
});
test("public persistence only accepts bounded settings for the current illustrative version", () => {
  assert.equal(snapshotInputSchema.safeParse({ demoVersion: DEMO_VERSION, state }).success, true);
  for (const altered of [
    { ...state, personalNote: "must not persist" }, { ...state, beta: Infinity },
    { ...state, lambdaScale: 0 }, { ...state, windingU: 1.1 },
    { ...state, z: 9 }, { ...state, provenance: "lmfdb" },
    { ...state, selectedLabel: "<script>" }, { ...state, selectedLabel: "1.zzz1" }, { ...state, controlledSupportEligible: true },
    { ...state, provenance: "synthetic", selectedLabel: "37.a1" },
  ]) assert.equal(snapshotInputSchema.safeParse({ demoVersion: DEMO_VERSION, state: altered }).success, false);
  assert.equal(snapshotInputSchema.safeParse({ demoVersion: "EXP-MAP-A01", state }).success, false);
});
test("capture resolves the visible fixture when the filter excludes an old selection", () => {
  const saved = captureSnapshotState({ ...state, provenance: "synthetic" });
  assert.notEqual(saved.selectedLabel, "37.a1");
  assert.equal(snapshotInputSchema.safeParse({ demoVersion: DEMO_VERSION, state: saved }).success, true);
});
