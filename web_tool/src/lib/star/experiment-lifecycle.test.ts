import test from "node:test";
import assert from "node:assert/strict";
import snapshot from "./registry-snapshot.json" with { type: "json" };
import { getPreregisteredEntries, isPreregisteredStatus } from "./experiment-lifecycle.ts";

test("preregistered status is not conflated with planned or eligibility", () => {
  for (const s of ["preregistered", "preregistered_closed", "PREREGISTERED"])
    assert.equal(isPreregisteredStatus(s), true);
  for (const s of ["planned", "preregisteredness", "executed", "controlled", ""])
    assert.equal(isPreregisteredStatus(s), false);
});

test("all current preregistered experiments and theory protocols are discovered from the snapshot", () => {
  const entries = getPreregisteredEntries(snapshot);
  assert.deepEqual(entries.map((entry) => entry.id), [
    "EXP-MAP-A01", "EXP-MAP-A03", "M1-INH-E1", "P0-ANSATZ-001",
  ]);
  assert.equal(entries.find((entry) => entry.id === "M1-INH-E1")?.status, "preregistered");
  assert.equal(entries.find((entry) => entry.id === "M1-INH-E1")?.protocolPath, "preregistrations/M1-INH-E1/protocol.md");
  const source = snapshot.preregistrations.find((entry) => entry.id === "M1-INH-E1");
  assert.deepEqual(source?.stages.map(stage => stage.status), ["planned","planned","planned"]);
  assert.equal(source?.gateState.controlledExecutionEligible, false);
  assert.equal(source?.gateState.controlledSupportEligible, false);
  assert.equal(source?.gateState.physicalSupportEligible, false);
});

test("new approved preregistrations appear automatically; planned ones do not", () => {
  const entries = getPreregisteredEntries({
    experiments: [
      {Experiment_ID:"EXP-NEW", Status:"preregistered"},
      {Experiment_ID:"EXP-NOT-YET", Status:"planned"},
    ],
    preregistrations: [
      {id:"M1-NEW",record:{Status:"preregistered_closed"},protocolPath:"preregistrations/M1-NEW/protocol.md"},
      {id:"M1-PLANNED",record:{Status:"planned"},protocolPath:"preregistrations/M1-PLANNED/protocol.md"},
    ],
  });
  assert.deepEqual(entries.map((entry) => entry.id), ["EXP-NEW", "M1-NEW"]);
});
