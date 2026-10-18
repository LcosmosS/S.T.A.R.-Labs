# Collaboration-readiness assessment — 2026-10-18

## Judgment and scope

The repository provides concrete targets for bounded, critical collaboration.
It does not provide evidence for a general scientific-validation or
execution-ready release. The largest remaining gaps concern independent
scientific review, provenance reconstruction and externally controlled authority.

The review inventoried the complete tracked tree at
`d69868e3c1d9ae70944deb239369e53a9ecc1e5b`, read the full governing Charter PDF,
canonical CSV control tables, active package/readiness/provenance documentation,
SciServer policies and tests, web metadata/asset consumers, and CI definitions.
It inspected GitHub PR/issue state and baseline workflow results. The machine
record [BASELINE.json](BASELINE.json) identifies the inspected inputs and tree
counts. Comprehensive surface coverage is not a line-by-line correctness audit
of every script, proof, notebook, recovered source or binary.

## Evidence and actionable findings

| Priority / area | Evidence at the audited baseline | Consequence and disposition |
| --- | --- | --- |
| P1 / onboarding | `Contributing.md` says Python 3.10+, points Codespaces to S.T.A.R.-Program, executes a legacy cosmology notebook, refers to absent `scripts/run_all_notebooks.sh` and `AUTHORS.md`, recommends unavailable Discussions, and contains `doi={TBD}` | Corrected contributor guide uses Python 3.12+, Issues, task-scoped checks, explicit governance and versioned citations. No historical notebook is run for onboarding. |
| P1 / status discovery | Root README says all corresponding experiments are planned, calls merged #84 a proposal and says the Aladin list is empty; canonical flags, #84's merge and the #95 receipt disagree | Corrected live-facing README: 16 planned/two preregistered, A01 execution only, one display-only admission. Historical packages and canonical assessment text are preserved. |
| P1 / independence | A01 package records a primary transaction; M1/A03 archives and automated checks do not establish external proof review or investigator-B reproduction | Tasks C02–C05 require exact revisions, identities, complete reports and preserved failures; no independent endorsement is invented. |
| P1 / CasJobs authority | #112 is merged as the baseline commit; `trusted_approvers.json` has activation false and no keys; catalog remote/per-query submission flags false | Offline tests can review implementation behavior. An independent operator, externally anchored runtime trust and post-merge source binding remain human/security tasks C01. Local receipts and a modifiable checkout are insufficient authority. |
| P1 / historical SDSS membership | Recovered TOP 200000 SQL has no ORDER BY; the preserved 18-column export has unresolved original job/context/export binding | Task C06 must separate query-defined population checks from exact historical membership. A deterministic replacement would be a different dataset. No live query/upload is made here. |
| P1 / survey/SFR/TDA | Publisher identity is distinct from scientific selection, association, targets, leakage and matched nulls; 37 quarantine records remain active | C06–C08 require specific source and methodological reviews. Do not infer scientific readiness from verified source bytes or a display receipt. |
| P2 / visual references | README branding forces mutable `blob/main` images; banner/social asset hashes match their dated provenance and caveats | Use branch-relative references, descriptive captions and provenance links; preserve the accurate images. The README banner and runtime social card are distinct assets. |
| P2 / citation and reuse | Root has no CITATION.cff; archives have distinct intended meanings; third-party sources have their own terms | Added software citation metadata and a use-to-artifact citation guide. No invented DOI, release date, archive title/authorship, blanket data license or automatic co-authorship. |
| P2 / security contact | `SECURITY.md` contains the malformed string `security@ LcosmosS@pm.me`; private reporting availability and inbox ownership/delivery are not established by this audit | Maintainer must confirm a usable private channel before recruiting vulnerability reports (C10). No address or response SLA is fabricated. Public collaboration issues must contain no exploit details. |
| P2 / dependency alerts | GitHub reports six open medium-severity Dependabot alerts: four JupyterLab records in frozen historical code-log requirements and two pytest records in the A03 frozen/reference requirements | These are distinct from the web npm audit. C03/C09 must triage the reproduction environment before execution; preserve the archived pins and propose any safer successor environment with explicit deviations in a separate review. This audit does not establish active runtime exposure or dismiss the alerts. |
| P2 / reproducibility environment | Python scientific pins, optional Sage/SciServer tools, three pinned submodules and selective LFS inputs have different requirements; most Python dependencies use ranges in project metadata | C09 asks for independently tested environment receipts. A normal clone or pointer digest does not prove hydration or an identical environment. No general dependency upgrade is bundled here. |
| P2 / CI trust and operation | Workflows use version tags for actions and some are path-filtered. The effective active main ruleset requires one approving review, stale-review dismissal and last-push approval, but permits role/integration bypasses; returned rules include CodeQL/code-quality gates and no `required_status_checks` rule | C09 should assess action pinning, bypass authority and required-check coverage separately. These observed settings are not proof that an agent cannot modify runtime trust; green checks do not supply human or scientific approval. |

## Current control state

At this baseline, the experiment registry has 18 rows: 16 planned and two
preregistered (A01/A03). A01 alone has execution eligibility. All 18 experiment,
all eight claim and all 46 dataset controlled/physical-support flags are false.
There are nine non-quarantined datasets plus 37 quarantine rows; five of the
nine have recorded verified provenance and four unknown. These are observed
registry declarations, not fresh verification of every source. P0 contains
five `REGISTERED_UNTESTED` candidates. No terminal outcome is assigned here.

An intentional historical tension remains: A01's canonical assessment text
still describes pending activation although its explicit flag and the separate
#78 decision permit execution. Earlier dated packets and frozen A03 release
text also describe their earlier pre-activation/pre-publication state. The
invitation explains these layers without rewriting bytes that protocols or
manifests bind. Namespace collisions remain governed by
[the namespace record](../../docs/registries/NAMESPACE.md).

The full Charter distinguishes D/E/M/P/H/C/T/S categories, success levels,
software validation and empirical/physical support. Its §§10–19, 28–31 and
36–37 require calibrated nulls, reproducibility and preservation of failures.
The [negative-results protocol](../../docs/registries/NEGATIVE_RESULTS_PUBLICATION_PROTOCOL_v0.1.md)
separates a valid non-rejection, valid replication failure and mathematical
obstruction from missing inputs or an ineligible protocol. The invitation
creates no new theorem, experiment endpoint or physical interpretation.

## What this review cannot independently establish

- Authentic execution history, operator identity or independent authorship from
  hashes, GitHub accounts, pasted transcripts or repository assertions alone.
- An independent A01 rerun: the archive verifier inspects saved bytes, formulas
  and bindings; it does not reconstruct the source cohort, graph or permutations.
- Full-domain mathematical correctness, gauge consistency, physical inequivalence,
  regularity or external proof acceptance for M1, ECC, RTCH, ACSC or P0.
- Original unordered SDSS membership/job identity; independent reacquisition and
  license/selection validation of every survey, LFS object, recovered program or
  inaccessible original cloud document. Only the single admitted ALFALFA source
  was hydrated for the local web gate; this is not a fresh publisher acquisition.
- Human signing-device isolation, independently verified trust-anchor ownership,
  deployment immutability or one-time authorization consumption in a future live
  adapter. No production key is generated, accessed or enrolled.
- Complete repository security, actual enforcement/bypass behavior of the observed GitHub rules, vulnerability
  inbox delivery, external resource uptime, Binder/architecture-service operation,
  production deployment revision, live sky imagery or durable save/load parity.
- Zenodo deposit metadata or archive bytes: the repository records four DOI
  identifiers, but resolver access failed during this review. The citation guide
  labels them repository-recorded and requires independent deposit checks.
- Scientific-support eligibility, physical ACSC/ECC/RTCH/BSD/cosmology/SFR claims,
  or a new display admission from any of these software/documentation checks.

## Recommended order

1. Review this package's scope, source hashes, contributor/citation accuracy and
   public issue. Confirm private reporting and third-party attribution contacts.
2. Assign accountable reviewers to C01 and the independent source/package tasks.
   Keep operator public-key enrollment in a distinct reviewed PR; the private
   key stays outside Codex/MCP access.
3. Complete specialist mathematical and methods reviews with counterexamples,
   exclusions, uncertainty and negative findings preserved.
4. Propose any actual reproduction as its own bounded plan with exact code,
   inputs, environment, expected agreement and applicable authorization. This
   invitation executes none of those experiments.
5. Consider a canary adapter only after trust enrollment and independent trust
   anchoring. Review its actual deployment commit after squash merge and obtain
   explicit authorization for its first live TOP 10 execution. No 200K job,
   historical source replacement or automatic scientific promotion follows.
