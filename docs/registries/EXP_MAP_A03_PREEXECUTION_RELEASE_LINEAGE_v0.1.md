# EXP-MAP-A03 v0.1 — post-publication DOI and source lineage

**Record type:** post-publication citation and discovery metadata; not part of the
frozen, SHA-256-locked scientific review package. Governing authority:
[`charter/STAR_Research_Charter_v0-2.pdf`](../../charter/STAR_Research_Charter_v0-2.pdf).

## Persistent identities

| Item | Pinned identity |
| --- | --- |
| Experiment | `EXP-MAP-A03` |
| Claim / dataset / parameter / null | `CLAIM-ACSC-002` / `DATA-ARITHMETIC` / `PAR-MAP-003` / `NULL-MAP-003` |
| Version-specific Zenodo DOI | [10.5281/zenodo.23288785](https://doi.org/10.5281/zenodo.23288785) |
| GitHub release | [`EXP-MAP-A03-preexecution-verification-v0.1`](https://github.com/LcosmosS/S.T.A.R.-Labs/releases/tag/EXP-MAP-A03-preexecution-verification-v0.1) |
| Release-tag commit | [`b291699163c4d57ec39b11bc09503ad00a42a7a2`](https://github.com/LcosmosS/S.T.A.R.-Labs/commit/b291699163c4d57ec39b11bc09503ad00a42a7a2) |
| Archive assembly / review | [PR #89](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/89) (merged) |
| Frozen verified implementation | [`ded6317a20d78fbb9c451b8ef54eb87cc09d8242`](https://github.com/LcosmosS/S.T.A.R.-Labs/commit/ded6317a20d78fbb9c451b8ef54eb87cc09d8242), [PR #86](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/86) |
| Source and hash manifest | [`SOURCE_MANIFEST.json`](../../release_packages/EXP-MAP-A03-preexecution-verification-v0.1/SOURCE_MANIFEST.json), [`SHA256SUMS`](../../release_packages/EXP-MAP-A03-preexecution-verification-v0.1/SHA256SUMS) |
| Human-review checklist | [`REVIEW_CHECKLIST.md`](../../release_packages/EXP-MAP-A03-preexecution-verification-v0.1/REVIEW_CHECKLIST.md) |
| CI reference-verification result | [run 38085559993](https://github.com/LcosmosS/S.T.A.R.-Labs/actions/runs/38085559993) |
| Historical CI artifact link (temporary) | [artifact 11682142104](https://github.com/LcosmosS/S.T.A.R.-Labs/actions/runs/38085559993/artifacts/11682142104) |

The version-specific DOI above was supplied by the release maintainer as a
**published Zenodo DOI**. The GitHub release/tag/commit were checked directly
against the repository. The Zenodo API record and deposited file inventory could
not be independently retrieved during this documentation update; **do not infer
byte-for-byte equivalence of the Zenodo deposit and tagged GitHub tree from their
cross-links alone**. An independent archivist should download the deposit,
record file-level SHA-256s and compare the archived package with the
`SHA256SUMS` and `SOURCE_MANIFEST.json` records.

## What the public archive does — and does not — establish

This is a versioned archive of **pre-execution reference verification** for the
frozen `EXP-MAP-A03-prereg-v1` MCJ arithmetic mapping. Reference checks on
the pinned ecdata publisher artifact reported 64,687 source rows, 38,042
isogeny-class representatives, 106 exact `j=0` exclusions and 37,936 accepted
curves. Graph and permutation comparisons were made on **synthetic fixtures**.

The registered 37,936-row observed endpoint, 999-permutation null, p-value,
scientific decision, and any cosmological test **were not executed** by this
package. The archived verification receipt and exact source content are
associated with the **PR #86 implementation**, not a later live implementation
changed for shared A01/A03 dataset compatibility. An older local receipt is
historical evidence for an earlier verifier SHA; it is **not** mislabeled as the
PR #86 CI receipt, which is a separate temporary artifact.

The publication date of the GitHub release is **2026-10-10**. PR #89's
package-local README and manifests were intentionally written *before*
publication and therefore call the package a candidate. Those are immutable
review-state descriptions at the time of package assembly; this file records
the later publication event. **Do not edit** the tagged package README,
`SOURCE_MANIFEST.json`, or `SHA256SUMS` merely to update the release status:
the manifest includes hashes for these documents.

## Citation and verification

**Citable DOI:** https://doi.org/10.5281/zenodo.23288785

**GitHub source release:**
https://github.com/LcosmosS/S.T.A.R.-Labs/releases/tag/EXP-MAP-A03-preexecution-verification-v0.1

For an independently verifiable lineage, record (1) the Zenodo record metadata
and downloadable file hashes, (2) the GitHub immutable tag SHA, (3) package
SHA-256 results, (4) the frozen origin Git blob checks, and (5) an independently
produced verification receipt and off-author scoped review. Verify exact Zenodo
creator/title metadata before preparing a formal bibliography entry.

A DOI provides persistence and citation, **not scientific authorization**.
The governing Charter's independent-review, preregistration, controlled
execution, replication, and support gates remain separate. In particular,
**neither PR #89 publication nor Zenodo issuance activates A03 or A01**.
