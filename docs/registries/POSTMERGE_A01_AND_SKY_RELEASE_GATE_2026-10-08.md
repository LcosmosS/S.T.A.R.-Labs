# Post-merge A01 and observational-display gate — 2026-10-08

**Controlling document:** charter/STAR_Research_Charter_v0-2.pdf, especially sections 12–17, 28–32, and 36–37. This is a dated evidence assessment, not independent approval or a change to frozen preregistration.

## A01 activation governance discrepancy

PR [#64](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/64) merged at 2026-10-09 01:27:20 UTC. It advanced Controlled_Execution_Eligible for REPO-CSV-v0.2:EXP-MAP-A01 and REPO-CSV-v0.2:DATA-ARITHMETIC to true, without promoting controlled or physical support. Its own activation decision required formal independent human approval on the exact final diff *before* merging, but documented that approval was outstanding. The GitHub pull-review history retrieved for this assessment contains only COMMENTED reviews by the author and CodeRabbit, not an independent APPROVED review.

**Discrepancy:** successful source-locked ecdata preflight and CI demonstrate computational readiness, but do not satisfy the separately stated independent scientific/governance approval condition. This unresolved authorization gate must not be erased by rewriting the original review docket, backfilling approval, or claiming that the merge constituted independent signoff.

**Containment recommendation:** do not perform the original A01 controlled run or independent rerun until an off-author reviewer inspects the exact merged diff, ecdata source binding, unchanged parameter/null/seed/endpoint, registry hash synchronization and final-head preflight and records an accountable disposition. A separate governance PR must decide whether execution eligibility should be restored to false pending that review. No eligibility transition is made by this document.

The original 999-draw controlled experiment and investigator-B independent rerun remain distinct Issue [#67](https://github.com/LcosmosS/S.T.A.R.-Labs/issues/67) milestones. No controlled result is implied by preflight.

## Observational source versus display release

- **DATA-MANGA-HI-ALL:** publisher source provenance was recorded as verified by merged [PR #74](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/74). The SDSS H I-MaNGA DR3 source FITS is 1,584,000 bytes; its recorded publisher/recovery/LFS SHA-256 is 0f51e1852f7103bd9af9699213a7548a7e6b9969ab1256ec86df04352ddec8f5. This is previously documented byte evidence, not a new binary download performed in this PR. Row selection, positional-role review, matching, null models and derived sky release remain separate.
- **DATA-SDSS18-200K:** the historical recovered 33,007,497-byte CSV already has a recorded genuine Git LFS upload and independent-download receipt. The CasJobs 18-column source binding is plausible but the original job identity/output membership is not independently resolved. Source provenance remains unknown.
- **Pipe3D, PhotoObj and other Dropbox CSVs:** presence or filename identity does not establish original publisher byte identity or executable canonical status. No new raw LFS binary is uploaded.
- **Aladin display:** web_tool/content/sky-overlay-releases.v1.json currently contains an empty source list. No astronomical overlay may be offered until an independently reviewed sky-coordinate derivative and full hash chain has been admitted.

## Integrity contract and capacity boundary

This PR adds no binary LFS objects, raw observational data, fake LFS pointers, registry provenance flips or support/physical eligibility changes. The connected GitHub text-file endpoint cannot upload and verify binary Git LFS objects. Future additions require actual git lfs push, clean-cache independent git lfs pull, matching SHA-256 and byte size, plus publisher rights and acquisition review.

The ALADIN Lite component uses only build-validated manifest releases. It does not accept arbitrary local files or manually entered expected hashes for an approved release. The browser additionally checks the exact served coordinate SHA-256, selected-ID digest, size and schema before plotting; verified display bytes are not a controlled experiment or physical evidence. Empty admission means disabled selection and no markers.

## Next highest-leverage milestone

Obtain a formally recorded off-author, exact-revision A01 activation decision; resolve whether present execution eligibility must be rolled back, then proceed only through Issue #67. The next astronomical-data milestone is a separate reviewed FITS-to-sky transformation release with pinned coordinate role, row IDs and immutable hashes.

Negative and unresolved outcomes remain in the audit history.
