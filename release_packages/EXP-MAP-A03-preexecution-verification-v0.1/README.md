# EXP-MAP-A03 — pre-execution verification review package v0.1

**Disposition:** candidate for independent review and eventual archival release. **Not** an execution activation, independent replication, scientific finding, or published GitHub Release. Governing authority: [frozen Charter PDF](frozen/STAR_Research_Charter_v0-2.pdf).

## Exact identity and provenance

- Experiment: `EXP-MAP-A03`; claim: `CLAIM-ACSC-002`; dataset: `DATA-ARITHMETIC`; parameter: `PAR-MAP-003`; null: `NULL-MAP-003`.
- Frozen scientific design: `EXP-MAP-A03-prereg-v1`, as preserved in the [configuration](frozen/config.json), [protocol](frozen/protocol.md), [dataset manifest](frozen/dataset_manifest.json), and [execution spec](frozen/controlled_execution_spec.json).
- This archive reproduces the exact verified PR #86 head [`ded6317a20d78fbb9c451b8ef54eb87cc09d8242`](https://github.com/LcosmosS/S.T.A.R.-Labs/commit/ded6317a20d78fbb9c451b8ef54eb87cc09d8242) byte-for-byte for every source item listed in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json).
- The reviewed source entered `main` through [PR #86](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/86). The v0.1 archive is **not** an assertion that later live code is identical.
- CI evidence for that exact PR head: [successful reference-verification run](https://github.com/LcosmosS/S.T.A.R.-Labs/actions/runs/38085559993), [temporary JSON artifact](https://github.com/LcosmosS/S.T.A.R.-Labs/actions/runs/38085559993/artifacts/11682142104). The archive contains a historical **local** receipt, not a copied CI receipt.
- A later [PR #87](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/87) amended the active A03 verifier for shared-dataset compatibility. It is a **distinct implementation revision**, excluded from this frozen PR #86 review target. Do not substitute the latest live verifier for the archived one.

## Contents

- [Reference verifier](verify_a03.py), [reference tests](test_a03_reference_verification.py), and [pinned requirements](requirements.txt) — exact copies from the verification commit; these must be executed **from a full repository checkout at that commit**, not as independently importable scripts inside this directory.
- [Verification report](A03_PREEXECUTION_VERIFICATION.md) and [historical local JSON receipt](local_verification_2026-10-10.json) — unmodified author-produced evidence.
- `frozen/` — copy of the approved-for-review protocol/config/spec/manifest and original Charter PDF from the same commit.
- [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) — origin paths, Git blob identities, SHA-256 digests, PR/CI references and exclusions.
- [SHA256SUMS](SHA256SUMS) — checksum manifest for all non-self-referential package files.
- [REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md) — independent referee acceptance questions and explicit no-promotion rule.

## Independent reproduction (NOT the experiment)

1. Obtain a full repository clone with Git history at commit `ded6317a20d78fbb9c451b8ef54eb87cc09d8242`; hydrate only the pinned ecdata artifact `allcurves.00000-09999` from upstream commit `25cec5ecfec8b9f016eb1631ac633194c2bed39f`; compare SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`. Do not use a subsequently modified `main` branch.
2. At that checkout, install exact package pins using `python -m pip install -r research/independent_review/2026-10-16/requirements.txt`.
3. Run the original, guarded verifier: `python -c 'import runpy; runpy.run_path("research/independent_review/2026-10-16/verify_a03.py",run_name="__main__")' --output /tmp/a03-review-new-receipt.json`.
4. Run `python -m pytest -q tests/test_a03_reference_verification.py tests/test_exp_map_a03_candidate.py tests/test_exp_map_a03_safety.py`; collect all pass/fail output and environment hashes.
5. On this review-package PR checkout, run `python scripts/validate_a03_preexecution_release.py --verify-origin`. This verifies archived byte digests and their original immutable Git blobs without executing a scientific experiment.

The source cohort checks previously reported 64,687 rows, 38,042 representatives, 106 exact `j=0` exclusions and 37,936 accepted curves. Graph and null comparisons use **40-row synthetic fixtures**, never the observed full-cohort endpoint or the registered 999-null analysis. Treat the archived local receipt's older verifier digest as **historical**; it is not a digest of the post-docstring PR #86 verifier. Independent investigators must generate new receipts.

## Release and review gates

This directory is a **candidate archival package**, not a GitHub tag, published Zenodo DOI, or scientific status transition. Review the final pull-request SHA, verify every file against SHA256SUMS and SOURCE_MANIFEST.json, retain the CI artifact before its expiration, record independent negative findings, and obtain an accountable off-author review before tagging/publishing a version-specific GitHub release or Zenodo deposit.

The locked A03 inference settings remain `k=10`, `seed=4103`, `B=999`, `alpha=0.005`, one-sided greater. This review archive **does not execute** that inference. No eligibility or support flag is changed, and successful archive CI must not be used as execution approval. A01/A03 shared-dataset activation is a separate governance question.
