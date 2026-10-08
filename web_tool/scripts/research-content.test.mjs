import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { validate, snapshotOf } from "./sync-research-content.mjs";

const model = JSON.parse(readFileSync(new URL("../content/research-content.v1.json", import.meta.url)));
const copy = () => structuredClone(model);
test("snapshot exactly reproduces reviewed versioned source", () => {
  assert.equal(validate(model), true);
  assert.deepEqual(snapshotOf(model).entries, model.entries);
  const actual = readFileSync(new URL("../src/lib/star/research-content-snapshot.json", import.meta.url), "utf8");
  assert.equal(actual, JSON.stringify(snapshotOf(model), null, 2) + "\n");
});
test("reject scientific support or execution promotion", () => {
  for (const name of ["controlledExecutionEligible", "controlledSupportEligible", "physicalSupportEligible"]) {
    const x = copy(); x.entries[0][name] = true;
    assert.throws(() => validate(x), /cannot grant/);
  }
});
test("reject ID collisions, unsupported status and malformed archival sources", () => {
  const d = copy(); d.entries[1].id = d.entries[0].id; assert.throws(() => validate(d), /Duplicate/);
  const e = copy(); e.entries[1].status = "scientifically_supported"; assert.throws(() => validate(e), /Unknown/);
  const p = copy(); p.entries[0].sourcePath = "../../secrets"; assert.throws(() => validate(p), /Unsafe/);
});
test("reject misleading diagrams and epistemic promotion", () => {
  const d = copy(); d.entries.find(e => e.kind === "diagram").steps = []; assert.throws(() => validate(d), /Diagram/);
  const e = copy(); e.entries.find(e => e.status === "derived_mathematics").epistemic = "H"; assert.throws(() => validate(e), /requires D/);
});
test("CLI check gate succeeds on committed snapshot", () => {
  const r = spawnSync(process.execPath, ["scripts/sync-research-content.mjs", "--check"], { encoding: "utf8" });
  assert.equal(r.status, 0, r.stderr);
});
