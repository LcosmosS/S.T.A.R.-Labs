import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { publicationsFromReadme } from "./repository-publications.mjs";

const readme = readFileSync(new URL("../../README.md", import.meta.url), "utf8");
const snapshot = JSON.parse(readFileSync(new URL("../src/lib/star/registry-snapshot.json", import.meta.url), "utf8"));
test("published packages and their limits are bound to current README bytes", () => {
  assert.deepEqual(snapshot.publications, publicationsFromReadme(readme));
  assert.equal(snapshot.sources.find(s => s.path === "README.md").sha256, createHash("sha256").update(readme).digest("hex"));
  assert.match(snapshot.publications.find(p => p.id === "M1-INH-E1b").status, /independent mathematical review pending/);
  assert.match(snapshot.publications.find(p => p.id === "EXP-MAP-A01").status, /not established/);
  assert.match(snapshot.publications.find(p => p.id === "EXP-MAP-A03").status, /not independently replicated/);
});
test("missing publication identities fail rather than leave a stale or invented citation", () => {
  assert.throws(() => publicationsFromReadme(readme.replaceAll("10.5281/zenodo.23292229", "removed")), /Missing.*EXP-MAP-A01/);
  assert.throws(() => publicationsFromReadme(readme.replace("### M1-INH-E1b", "### removed")), /Missing.*M1-INH-E1b/);
});
