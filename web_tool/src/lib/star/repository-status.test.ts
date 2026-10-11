import test from "node:test";
import assert from "node:assert/strict";
import { executionSummary, matchingSkyRelease, unresolvedPlaceholders } from "./repository-status.ts";

test("execution presentation requires both current flags and still requires preflight", () => {
  const eligible = executionSummary({ experimentExecutionEligible: true, datasetExecutionEligible: true });
  assert.match(eligible, /Execution eligibility is recorded for the experiment and dataset/);
  assert.match(eligible, /preflight is still required/);
  assert.doesNotMatch(eligible, /blocked/);
  for (const [experimentExecutionEligible, datasetExecutionEligible] of [[false, false], [true, false], [false, true]]) {
    assert.match(executionSummary({ experimentExecutionEligible, datasetExecutionEligible }), /blocked/);
  }
});

test("reserved placeholders stop carrying the unresolved label when the canonical record changes", () => {
  const row = { Dataset_ID: "DATA-PHYS-CONSTRAINTS", Status: "planned", Provenance_Status: "unknown" };
  assert.deepEqual(unresolvedPlaceholders([row]), [row.Dataset_ID]);
  assert.deepEqual(unresolvedPlaceholders([{ ...row, Provenance_Status: "verified" }]), []);
  assert.deepEqual(unresolvedPlaceholders([{ ...row, Status: "locked" }]), []);
});
test("an admitted ID does not supersede a different candidate source, derivative, ID chain or role", () => {
  const release = { datasetId: "DATA-VIZIER-ALFALFA100", sourceSha256: "source", coordinateSha256: "coords", selectedIdsSha256: "ids", coordinateRole: "hi_centroid" };
  assert.equal(matchingSkyRelease({ ...release }, [release]), release);
  assert.equal(matchingSkyRelease(release, []), undefined);
  for (const key of Object.keys(release)) {
    assert.equal(matchingSkyRelease({ ...release, [key]: "changed" }, [release]), undefined);
  }
});
