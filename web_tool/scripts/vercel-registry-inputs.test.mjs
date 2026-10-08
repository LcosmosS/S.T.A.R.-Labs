import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import ignore from "ignore";

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const snapshotPath = "web_tool/src/lib/star/registry-snapshot.json";
const syncPath = "web_tool/scripts/sync-registry.mjs";
const snapshot = JSON.parse(readFileSync(join(repoRoot, snapshotPath), "utf8"));
const deploymentFilter = ignore().add(readFileSync(join(repoRoot, ".vercelignore"), "utf8"));

test("registry check passes with only inputs retained by the Vercel deployment filter", () => {
  const tempParent = realpathSync(tmpdir());
  const fixture = mkdtempSync(join(tempParent, "star-vercel-registry-"));
  try {
    // Run the actual build-time check in an isolated tree, so an unfiltered
    // checkout cannot hide a required input excluded from deployment.
    for (const path of [syncPath, snapshotPath, ...snapshot.sources.map((source) => source.path)]) {
      if (deploymentFilter.ignores(path)) continue;
      const destination = join(fixture, path);
      mkdirSync(dirname(destination), { recursive: true });
      copyFileSync(join(repoRoot, path), destination);
    }
    const result = spawnSync(process.execPath, [join(fixture, syncPath), "--check"], {
      cwd: join(fixture, "web_tool"),
      encoding: "utf8",
    });
    assert.ifError(result.error);
    assert.equal(result.status, 0, `Filtered deployment registry check failed:\n${result.stdout}${result.stderr}`);
    assert.match(result.stdout, /Registry snapshot matches \d+ canonical source files/);
  } finally {
    // Only remove this test's generated directory under the resolved temp root.
    assert.equal(dirname(fixture), tempParent);
    assert.match(basename(fixture), /^star-vercel-registry-/);
    rmSync(fixture, { recursive: true, force: true });
  }
});

test("deployment excludes historical code, scientific payloads and local secrets", () => {
  for (const path of [
    "historical/r&d/code_log/example.py",
    "historical/r&d/docs/recovered_corpus_audit_2026-10-08/source_manifest.json",
    "data/quarantine/2026-10-03_audit/example.csv",
    "data/intake/recovered/2026-10-08/example.fits",
    "web_tool/.env.local",
    "web_tool/node_modules/example/index.js",
  ]) {
    assert.equal(deploymentFilter.ignores(path), true, `Unexpected deployment inclusion: ${path}`);
  }
});
