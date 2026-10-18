# S.T.A.R.-Labs collaboration invitation v0.1

**Disposition:** review/invitation package proposed for repository review. No
GitHub Release, tag, DOI, peer review, scientific finding, experiment activation,
operator enrollment or live submission is created by this package.

**Audited source:** [`d69868e3c1d9ae70944deb239369e53a9ecc1e5b`](https://github.com/LcosmosS/S.T.A.R.-Labs/commit/d69868e3c1d9ae70944deb239369e53a9ecc1e5b),
main inspected on **2026-10-18**. This is a dated audit, not a live status feed.
**Authority:** [full Research Charter v0.2 PDF](../../charter/STAR_Research_Charter_v0-2.pdf),
SHA-256 `9a63284900d5349f1d307160929b2542885e4c751439b785369b722d349a5c03`.
This package is an agent-assisted repository assessment, not independent human
scientific review or an attestation of a contributor's identity.

## Invitation

We invite researchers and engineers to challenge specific constructions, verify
source lineage, audit software boundaries and propose reproducible review plans.
The goal is to find errors and determine what the evidence can support, including
negative or inconclusive outcomes. Expertise is needed in arithmetic geometry,
permutation statistics, differential geometry/GR, cohomology, astronomical survey
selection and matching, SFR/ML leakage, TDA, security engineering and research
software/reproducibility.

Start with [findings and limitations](REVIEW.md), choose one [task contract](TASKS.md),
and use the [review report template](REVIEW_REPORT_TEMPLATE.md). Follow
[Contributing.md](../../Contributing.md), the [Code of Conduct](../../CODE_OF_CONDUCT.md)
and [citation guide](CITATION_GUIDE.md). Reply to the public collaboration issue
or open a narrowly scoped issue naming your task, expertise, independence,
proposed deliverable and intended files. The repository's Issues tab is the
public coordination channel; no invitation-only account or credentials are needed
to read this package. A GitHub account is needed to post an issue or PR.

## What is available to review

- A01 has preserved primary arithmetic evidence. Archive inspection is distinct
  from an accountable independent experiment rerun and from physical inference.
- A03 has a frozen pre-execution reference-verification archive. It has no
  controlled-execution authorization at this baseline.
- M1-INH-E1b has a candidate mathematical certificate and a pre-review archive.
  External proof/regularity/invariance review remains a separate task.
- Five P0 parent-theory candidates are registered untested; no terminal search
  exhaustion or universal no-go conclusion is supplied.
- Observational source intake, quarantine and display receipts are inspectable.
  The ALFALFA admission is display-only, not crossmatching or scientific support.
- SciServer has a read-only interface and offline policy/approval verification.
  Its operator trust list is empty, activation is false, and remote submission
  flags are false. This invitation does not call even the existing live read tools.

The baseline has 18 canonical experiments (16 planned, two preregistered), one
execution-eligible experiment (A01), and zero controlled/physical-support-eligible
experiments or claims. See [BASELINE.json](BASELINE.json) for source hashes,
registry observations and the scope of review. Historical assessment text is
preserved even where later activation records supersede its narrative.

## Package integrity and safe first checks

`SHA256SUMS` enumerates this package's files except itself; paths are relative
to the repository root. From a full checkout of the invitation PR or its reviewed
merge revision:

```bash
sha256sum -c release_packages/STAR-collaboration-invitation-v0.1/SHA256SUMS
python scripts/independent_gate_report.py
python scripts/independent_dataset_verification.py --format markdown
git diff --check
```

The census commands inspect local records; do not add `--live-public-sources`
or run experiment entrypoints as part of these first checks. Package checksums
establish byte consistency, not authority, identity, independent replication or
scientific correctness. Compare them with the actual reviewed Git commit.

[VALIDATION.md](VALIDATION.md) records local checks and their limits. Remote CI
must be inspected for the final PR head; subsequent correction commits require
new checks. The PR discussion carries the current head/check URLs without
rewriting a frozen scientific release or asserting a self-referential commit hash.

## Deliberate scope limits

This package adds no claims, results, scientific registry rows or eligibility
transitions. It changes no historical/frozen evidence, preregistrations,
parameters, nulls, executable experiment code, tokens, trust manifests, source
SQL, sky admission records or workflows. Its web snapshot update derives only
from intentional README metadata changes. Existing accurate image bytes are
retained and their references/captions clarified.

An experiment rerun, source acquisition involving authenticated services,
trust enrollment, canary adapter or live execution must be a separately reviewed
scope. In particular, the future operator's private signing key must remain
inaccessible to Codex and MCP. After squash merge, any future grant must bind
the actual reviewed deployment commit, not a superseded feature-branch SHA.

Open PRs [#103](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/103),
[#107](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/107) and
[#108](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/108) were separate candidates
at audit time. This package neither imports them nor certifies their science.
Existing specialist invitations [#82](https://github.com/LcosmosS/S.T.A.R.-Labs/issues/82)
and [#92](https://github.com/LcosmosS/S.T.A.R.-Labs/issues/92) remain the M1 and A03
review threads; the collaboration issue coordinates rather than supersedes them.
