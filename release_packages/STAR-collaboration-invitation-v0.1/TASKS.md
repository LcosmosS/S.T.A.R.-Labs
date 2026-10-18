# Expertise and independent verification task contracts

These are review requests, not scientific registry IDs or execution grants.
Task IDs C01–C10 belong only to this invitation. All paths below resolve from
the audited repository root. Use [the report template](REVIEW_REPORT_TEMPLATE.md)
and cite the exact revision reviewed. A later changed PR head requires renewed
review of the relevant differences. An off-author reviewer must disclose their
relationship, implementation history and assistance; a second agent or a
self-test is not independent human review.

## C01 — Security and independently controlled authorization (priority 1)

**Expertise:** application security, Ed25519 verification, filesystem/runtime
trust and reproducible deployment. **Target:** `integrations/sciserver/approval_policy.py`,
`approval_protocol.md`, `query_policy.py`, `receipts.py`, `trusted_approvers.json`,
`query_catalog.json`, and `tests/integrations/` at the actual reviewed commit.
PR #112 merged as `d69868e3c1d9ae70944deb239369e53a9ecc1e5b`.

**Work:** audit canonical signed bytes, rejection of substituted trust inputs,
run/plan/SQL/catalog/destination/source binding, expiration/replay and receipt
limitations. Evaluate the trusted-runtime threat model: a writable checkout or
unanchored local receipt must not allow an agent to substitute trust. Review
post-squash source binding explicitly. Offline tests may be run in a fresh
environment with `pytest` and `cryptography>=42,<47`:

```bash
python -m pytest -q tests/integrations/test_sciserver_approval.py tests/integrations/test_sciserver_policy.py
```

**Deliver:** a threat-model and findings report with exact code SHA, trust-file
hash, tested adversarial cases and unresolved runtime assumptions. Separately,
an accountable operator must establish their identity and generate/hold a real
private key on a device/account inaccessible to Codex/MCP. An independently
verified public-key fingerprint/identity and externally anchored trust manifest
belong in a **different** enrollment PR. Do not send private keys to this repo,
Codex or MCP. Test-generated disposable keys are not operator identities.

**Acceptance/stop:** complete offline report with reproducible rejection cases;
no security certification from tests alone. Trust enrollment, `activation_enabled`,
remote submission flags and live adapter changes are out of this task. A future
live grant must bind the actual reviewed deployment commit, not #112's old head
`170c4d280d6c12c0c34345305ca6c8d6aa3dc2c3`. After any later merge, reassess the new
commit and trust anchor before signing. First live TOP 10 execution still needs
separate explicit authorization. The deterministic 200K probe stays blocked.

## C02 — A01 archive verification and independent reproduction plan (priority 1)

**Expertise:** reproducible numerical research, arithmetic data, permutation
statistics. **Target:** `release_packages/EXP-MAP-A01-primary-execution-v0.1/`,
`preregistrations/EXP-MAP-A01/`, `controlled_execution/specs/EXP-MAP-A01.json`,
`src/experiments/exp_map_a01.py`, `src/control/execution.py`.

**Work:** independently inspect the original archive and all eight members,
including both logs, against the verifier and raw source Git objects. Run only
the read-only verifier first:

```bash
python release_packages/EXP-MAP-A01-primary-execution-v0.1/verify_package.py
```

Record the archive hash, exact source commit
`1b0f2d7853608bfbab79cf2dc04b002f1f193eb2`, protocol `EXP-MAP-A01-prereg-v1`,
qualified `REPO-CSV-v0.2:EXP-MAP-A01`, `CLAIM-ACSC-001`, `DATA-ARITHMETIC`,
`PAR-MAP-001` and `NULL-MAP-001`. Distinguish the 64,687 source rows from
38,042 analysis representatives. Inspect the saved T, all 999 null rows and
`p=(1+exceedances)/(999+1)` without claiming to regenerate them.

**Deliver:** archive-inspection receipt and a separate prospective investigator-B
rerun plan specifying independent environment/operator, source reconstruction,
cohort, graph, PRNG/null agreement criteria, transaction preflight and a fresh
write-once reproduction manifest linked to the primary manifest.

**Acceptance/stop:** report exactly what was rechecked and what remains only
recorded by the original runner. This invitation does not run the experiment.
A later separately reviewed rerun must preserve all outcomes and deviations;
passing an archive check is not replication. No cosmological, BSD or physical
ACSC conclusion follows from this arithmetic endpoint. No protocol retuning.

## C03 — A03 pre-execution reference review (priority 1)

**Expertise:** arithmetic geometry, exact rational invariants, conditional
randomization tests, independent numerical implementation. **Target:**
`release_packages/EXP-MAP-A03-preexecution-verification-v0.1/`,
`research/independent_review/2026-10-16/`, `preregistrations/EXP-MAP-A03/`.

**Work:** verify SHA256SUMS and SOURCE_MANIFEST against frozen verifier revision
`ded6317a20d78fbb9c451b8ef54eb87cc09d8242`, pinned ecdata commit
`25cec5ecfec8b9f016eb1631ac633194c2bed39f` and source-file hash
`259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`.
Follow the frozen package's checkout/environment instructions; its copied
verifier is not a standalone latest-main script. Review the 106 exact j=0
exclusions, 37,936 accepted representatives, conductor-decile null and synthetic
40-row reference checks. Distinguish later #87 compatibility code from #86.

**Deliver:** discrepancy/acceptance report and, if the reviewer elects to run
reference software, a new pre-execution reference receipt with logs, exact
revision and independent method. Coordinate with existing issue #92.

**Acceptance/stop:** no full-cohort observed endpoint or 999-null inference,
no A03 transaction, activation or promotion. Old pre-publication text is
historical; do not modify the frozen archive to update its publication status.

## C04 — M1 and ACSC mathematical review (priority 1)

**Expertise:** exact GR tensor calculus, Szekeres–Szafron geometry, differential
invariants, regularity and mathematical proof review. **Target:**
`preregistrations/M1-INH-E1/`, `release_packages/M1-INH-E1b-pre-review-v0.1/`,
`docs/monographs/acsc/2026-10-11/` and its correction ledger.

**Work:** review E1a versus E1b conventions and sign dictionary, full-domain
Einstein-dust solution validity, branch assumptions and regularity; evaluate
whether identical complete elliptic evolution data coexist with physically
inequivalent inhomogeneity. Explain any arbitrary-diffeomorphism/gauge gaps.
Review conditional lemmas and unsupported interpretations in the revised ACSC
manuscript against its ledger and original historical source. Symbolic checks
and sampled residuals must be labeled separately from a proof.

**Deliver:** assumption-by-assumption proof report, counterexamples or missing
lemmas, exact source/certificate hashes and a narrowly bounded conclusion.
Coordinate with issue #82. Propose any additional executable proof work as its
own scoped plan rather than executing historical programs automatically.

**Acceptance/stop:** do not infer a universal no-go theorem, E1c observable
insufficiency, P0 terminal status, physical correspondence or external peer review
from the E1b certificate or a software rerun.

## C05 — ECC/RTCH consistency and closed P0 search (priority 1)

**Expertise:** de Rham/cochain cohomology, bundles/gauge theory, variational
physics, stability and GR recovery. **Target:** `research/gates/ECC_RTCH_RECOVERY.md`,
`preregistrations/P0-ANSATZ-001/`, `registry/theory_*_registry_v0.1.csv` and the
full Charter §§25–27.

**Work:** distinguish exact and closed forms, space cohomology from the class
of a specific field, and globally defined potentials from nontrivial transition
data. Review whether any proposed ECC successor has independently defined
fields, nonzero periods/class and consistent gauge/kinetic terms. For RTCH,
require one frozen action, units, boundary terms, stress tensor, sign dictionary,
conservation, stability and a regular standard-physics limit before fitting.
For P0, assess only the five registered representatives under fixed admission
and failure rules; do not choose a representative because it yields ellipticity.

**Deliver:** separate proof-obligation sheets for ECC, RTCH and each P0 candidate,
including positive/negative controls, counterexamples, missing definitions and
what would be needed before a new prospective protocol.

**Acceptance/stop:** all five candidates are registered untested here; no
fabricated signatures or terminal dispositions. No historical ECC result is
rehabilitated, no replacement theory is silently imported, no cosmological
fit/inference is run, and no registry flags or frozen protocols change. An open
ECC proposal/reproduction PR (#103/#108 at audit time) is a separate review target,
not accepted theory or independently authenticated proof.

## C06 — Survey source lineage and astronomical association (priority 1)

**Expertise:** SDSS/CasJobs, MaNGA/Pipe3D, H I astronomy, spherical geometry and
survey selection. **Target:** `verification/datasets/`, `data/provenance/`,
`research/acquisition/vizier_alfalfa100/`, observational lineage documentation,
canonical dataset/provenance tables and quarantine receipts.

**Work:** inspect publisher/version, schema, column meaning/units, raw-byte and
semantic checks, selection, joins, coordinate roles and uncertainties. The
historical unordered TOP 200000 export cannot be recreated by assuming a fresh
query has identical membership. Separate population membership, source-job
identity and deterministic successor selection. Review false-match controls,
mask/footprint, multiplicity, redshift and positional-error model requirements.

**Deliver:** dataset-specific receipt with independent source/version/license
checks, actual payload hashes, missing evidence, mismatches and prospective
reconstruction steps. Static census is safe without service calls:

```bash
python scripts/independent_dataset_verification.py --format markdown
```

**Acceptance/stop:** no authenticated CasJobs query, ID upload, MyDB write,
200K probe, inferential matching or frozen-source replacement in this invitation.
A public-source reacquisition is a distinct declared verification activity;
serialization differences must be preserved and reported, not relabeled a hash
match. The ALFALFA display receipt does not validate scientific associations.

## C07 — SFR and learning leakage audit (priority 2)

**Expertise:** astronomical SFR measurement, causal/data leakage review,
grouped predictive evaluation and calibrated uncertainty. **Target:**
`src/quality/sfr_leakage_gate.py`, SFR reconstruction candidates under
`experiments/reconstruction_candidates/2026-10-03/`, registered SFR rows and
`web_tool/content/historical-sfr-report-context.v1.md`.

**Work:** trace targets/units, source table/column and calibration, row/group
identity, repeated objects, feature ancestry and target-derived leakage. Define
prospective group-disjoint splits, baseline models, arithmetic ablations,
selection-matched permutations, uncertainty and out-of-sample decision rules.
Treat historical fitted scores and pickled models as inert audit material.

**Deliver:** feature/target lineage table, specific leakage counterexamples and
a proposed frozen validation design with failure criteria and unresolved inputs.

**Acceptance/stop:** no fitting, deserialization of recovered models, science
execution or promotion. A successful software leakage fixture is not an SFR
result or physical ACSC evidence.

## C08 — TDA and statistical design audit (priority 2)

**Expertise:** persistent homology, geometric statistics, sampling/selection
nulls and multiple comparisons. **Target:** `src/tda/`, `src/acsc/tda_pipeline.py`,
`src/acsc/alt_mappings.py`, `research/gates/EXP-TOPO-A01/` and Charter §§8–19.

**Work:** inspect normalization, sampling, metric/filtration, persistence
conventions, resolution/noise controls, uncertainty, power and alternative
mappings. Explain whether candidate thresholds are calibrated under appropriate
nulls. Keep A01's locked global-rank-permutation result distinct from proposed
conditional or survey-selection nulls. Betti descriptors do not automatically
identify astronomical filaments or physical categories.

**Deliver:** methods review and prospective controls/acceptance matrix with exact
relevant IDs, data dependencies and unresolved assumptions.

**Acceptance/stop:** do not recompute registered endpoints, tune thresholds to
saved outcomes, run historical pipelines, or describe an unactivated topology
candidate as preregistered inference.

## C09 — Software, provenance and web reproducibility (priority 2)

**Expertise:** Python/Sage packaging, CI security, Git LFS/submodules,
React/browser accessibility and reproducible artifacts. **Target:**
`pyproject.toml`, `requirements.txt`, `docker/`, `.github/workflows/`,
`web_tool/README.md`, image lineage and registry/research/sky check scripts.

**Work:** reproduce task-relevant checks in a clean environment; inspect exact
wheel imports, pinned gitlinks, selective fresh-cache LFS hydration and real
payload hashes. Review action immutability, required checks and off-author review
enforcement without modifying policy. Review branch-local image references,
alt/caption scope, snapshot freshness, desktop/mobile rendering and asset hashes.
Check final PR-head CI separately from local checks. Any authenticated deployment
inspection must be scoped separately; no deploy or database migration is requested.

**Deliver:** environment and command receipt, complete outcomes/skips, artifact
hashes and source-to-output mapping. Distinguish local browser rendering,
production-build rendering, hosted deployment parity, live external imagery and
durable storage verification. Do not invoke live SciServer tools for a smoke test.

**Acceptance/stop:** no rewrite of locked bytes or canonical flags, blanket
execution of archived code/notebooks, deployment, database write or automatic
scientific endorsement. Missing data/dependencies remain explicit blockers.

## C10 — Research governance, attribution and private reporting (priority 2)

**Expertise:** research data stewardship, scientific authorship/citation and
repository maintenance. **Target:** full Charter, namespace/correction/negative
result policies, `CITATION.cff`, [citation guide](CITATION_GUIDE.md), `LICENSE`,
`SECURITY.md`, Code of Conduct and this invitation.

**Work:** verify archive-specific DOI metadata/versions, authors, title, deposited
files and licensing directly at the publisher; do not treat DOI badges as byte
verification. Check upstream source acknowledgments and redistribution terms.
Confirm a usable private vulnerability-report channel: the baseline security
policy contains an ambiguous malformed address and this audit did not test its
delivery or private-reporting availability. Agree reviewer credit and conflict
handling without promising authorship or claiming endorsement.

**Deliver:** citation/rights discrepancy ledger and a maintainer-confirmed
private contact/reporting correction in its own reviewable change if needed.

**Acceptance/stop:** no invented DOI, mailbox, reviewer signature, institutional
partnership, peer review, author consent or acceptance promise. A software MIT
license does not relicense all upstream scientific data and publications.
