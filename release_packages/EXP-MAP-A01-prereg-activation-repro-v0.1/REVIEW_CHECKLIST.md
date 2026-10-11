# Independent A01 package review checklist

- [ ] Confirm governing Charter v0.2 PDF hash and applicable §§12–15, 17, 28–31.
- [ ] Verify original preregistration protocol/config/manifest and source sha from their canonical repository files; no retuning or copied competing protocol.
- [ ] Verify A01 mode/preregistered status, Claim/Dataset/Parameter/Null registry identities and exact active SHA-256 bindings against the source-locked controlled spec.
- [ ] Verify **independently pinned SHA-256** of the exact reviewed A01/A03 execution specs, the frozen A01 protocol, config, source manifest and charter; reject colluding changes to a spec and its internal SHA list.
- [ ] Verify the **full A03 experiment-row SHA-256**, not only eligibility flags, against the frozen A03 spec and independent reference digest.
- [ ] Confirm CI runs `--verify-github-approval`, verifies actual PR #78 final-head review and merge and PR #87 compatibility merge, and marks offline-only receipts as externally **unverified**.
- [ ] Verify PR #78 final-head off-author human approval and successful source-locked A01 CI; examine the historical reversal PRs #64/#77.
- [ ] Verify PR #87's A01/A03 reversible one-bit shared-dataset compatibility, and confirm A03 normal execution remains blocked.
- [ ] Confirm the verified ecdata source is exactly 64,687 rows, 2,146,401 bytes; cohort 38,042 curve-number-1 class representatives; no post-hoc exclusions.
- [ ] Confirm k=10, no elevation in neighbor graph, immutable mapping constants, seed 1729, B=999, alpha .01, one-sided p, and all result file names.
- [ ] Confirm package CI produces a **read-only** new receipt without running either experiment or writing canonical state.
- [ ] Confirm original and investigator-B manifests, sidecars, actual output hashes and all null values are **not** represented as already existing in this package.
- [ ] Confirm controlled and physical support flags remain false; a positive arithmetic signal is not cosmological, SFR, BSD or physical evidence.
- [ ] Record reviewer identity, exact PR commit, checked source hashes, unresolved concerns, and an explicit approval/nonapproval decision. Review of documentation is not a result-support promotion.

**Outcome:** This package is eligible for ordinary code/documentation review when all source checks pass. No authorless or bot-only review upgrades it to scientific support. Any future hypothesis/statistical change requires a new prospective protocol rather than overwriting the frozen A01 version.
