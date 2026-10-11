import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { publicationsFromReadme } from "./repository-publications.mjs";

const readme = readFileSync(new URL("../../README.md", import.meta.url), "utf8");
const snapshot = JSON.parse(readFileSync(new URL("../src/lib/star/registry-snapshot.json", import.meta.url), "utf8"));
test("published packages and their limits are bound to current README bytes", () => {
  assert.deepEqual(snapshot.publications, publicationsFromReadme(readme));
  assert.deepEqual(snapshot.publications.map(p => p.doi), [
    "https://doi.org/10.5281/zenodo.23260882",
    "https://doi.org/10.5281/zenodo.23292229",
    "https://doi.org/10.5281/zenodo.23288785",
  ]);
  assert.equal(snapshot.sources.find(s => s.path === "README.md").sha256, createHash("sha256").update(readme).digest("hex"));
  assert.match(snapshot.publications.find(p => p.id === "M1-INH-E1b").status, /independent mathematical review pending/);
  assert.match(snapshot.publications.find(p => p.id === "EXP-MAP-A01").status, /not established/);
  assert.match(snapshot.publications.find(p => p.id === "EXP-MAP-A03").status, /not independently replicated/);
});

const titles = [
  "M1-INH-E1b — Pre-review package v0.1",
  "EXP-MAP-A01 — Preregistration, activation and reproducibility package v0.1",
  "EXP-MAP-A03 — Published pre-execution verification archive v0.1",
];
const fixture = titles.map((title, index) => `### ${title}\nhttps://doi.org/10.5281/zenodo.${100 + index}\nhttps://github.com/LcosmosS/S.T.A.R.-Labs/releases/tag/package-${index}\n**Scientific status:** status-${index}\n`).join("\n");

test("publication metadata stays within exact heading sections without separators", () => {
  const misleading = `A reference to ### ${titles[0]} appears in prose.\nhttps://doi.org/10.5281/zenodo.999\nhttps://github.com/LcosmosS/S.T.A.R.-Labs/releases/tag/forged\n**Scientific status:** forged\n`;
  const results = publicationsFromReadme(misleading + fixture);
  assert.deepEqual(results.map(p => [p.doi, p.release, p.status]), [
    ["https://doi.org/10.5281/zenodo.100", "https://github.com/LcosmosS/S.T.A.R.-Labs/releases/tag/package-0", "status-0"],
    ["https://doi.org/10.5281/zenodo.101", "https://github.com/LcosmosS/S.T.A.R.-Labs/releases/tag/package-1", "status-1"],
    ["https://doi.org/10.5281/zenodo.102", "https://github.com/LcosmosS/S.T.A.R.-Labs/releases/tag/package-2", "status-2"],
  ]);
  assert.deepEqual(publicationsFromReadme(fixture.replaceAll("\n", "\r\n")), publicationsFromReadme(fixture));
});

test("missing fields cannot be borrowed from following publication or parent sections", () => {
  for (const heading of ["# Next section", "## Next section", "### Next section", "---"]) {
    const broken = fixture.replace("https://doi.org/10.5281/zenodo.100", `${heading}\nhttps://doi.org/10.5281/zenodo.100`);
    assert.throws(() => publicationsFromReadme(broken), /Missing.*M1-INH-E1b/);
  }
  for (const field of ["https://doi.org/10.5281/zenodo.101", "https://github.com/LcosmosS/S.T.A.R.-Labs/releases/tag/package-1", "**Scientific status:** status-1"]) {
    assert.throws(() => publicationsFromReadme(fixture.replace(field, "")), /Missing.*EXP-MAP-A01/);
  }
  assert.throws(() => publicationsFromReadme(fixture.replace(`### ${titles[0]}\n`, `### ${titles[0]} suffix\n`)), /Missing.*M1-INH-E1b/);
  assert.throws(() => publicationsFromReadme(fixture + `\n### ${titles[0]}\n`), /Ambiguous.*M1-INH-E1b/);
});
test("missing publication identities fail rather than leave a stale or invented citation", () => {
  assert.throws(() => publicationsFromReadme(readme.replaceAll("10.5281/zenodo.23292229", "removed")), /Missing.*EXP-MAP-A01/);
  assert.throws(() => publicationsFromReadme(readme.replace("### M1-INH-E1b", "### removed")), /Missing.*M1-INH-E1b/);
});
