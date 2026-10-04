# Provenance Audit v0.3 remediation completion

Audit date: 2026-10-03. All scientific originals and prior history are preserved. The remediation copied artifacts rather than deleting or replacing scientific source files. No new controlled result or independent replication was performed.

## Complete change inventories

- [remediation_files_v0.3.csv](remediation_files_v0.3.csv): every changed/copied file (13391), action and canonical Git-blob SHA256. Self-inventory file hashes are omitted to avoid circular hashes.
- [remediation_directories_v0.3.csv](remediation_directories_v0.3.csv): every newly versioned directory (33).
- [remediation_status_changes_v0.3.csv](remediation_status_changes_v0.3.csv): every changed registry status/assessment/eligibility value (2203).
- [Code-log triage](../../historical/r&d/code_log_triage/2026-10-03/): every copied code-log artifact, origin/review status and scoped superseded arithmetic decisions.

## Ordered changes

1. Ingested all 329 supplied audit file members and verified all four critical PDFs and 328 supplied checksums.
2. Quarantined 37 copies: two failed matches, seven projection artifacts/manifests, and 28 RTCH synthetic artifacts. All 29 prior supplied hashes match; eight figures have newly observed hashes.
3. Preserved registry namespaces and baseline definitions; applied the authoritative 51 claim, 25 experiment and 51 crosswalk assessments. Added explicit quarantine source records and eligibility guards.
4. Added three reconstruction candidate protocols with evidence, null, lineage and acceptance gates.
5. Preserved the entire available OneDrive code-log folder and recorded pending review and scoped superseded benchmark arithmetic. The correction source's integer-certification limitation remains explicit.
6. Added the seven-point main README summary and the complete byte-identical canonical audit package at the versioned path.

## Files by group

- `.gitattributes`: 1 file change.
- `.github/`: 1 file change.
- `README.md`: 1 file change.
- `charter/`: 1 file change.
- `docs/`: 6 file changes.
- `experiments/`: 3 file changes.
- `historical/r&d/code_log/2026-10-03/`: 12633 file changes.
- `historical/r&d/code_log_triage/2026-10-03/`: 13 file changes.
- `historical/r&d/docs/provenance_audit/`: 331 file changes.
- `historical/r&d/docs/provenance_audit_v0.3/`: 333 file changes.
- `historical/r&d/quarantine/2026-10-03_audit/`: 52 file changes.
- `registry/`: 14 file changes.
- `scripts/`: 1 file change.
- `tests/`: 1 file change.

## Verification and missing sources

The [final verification](REMEDIATION_VERIFICATION_v0.3.json) includes registry, code-log and published-byte checks. The [quarantine verification](../../historical/r&d/quarantine/2026-10-03_audit/step1_verification.json) retains the initial copy diagnostics. Missing named sources remain recorded in the applicable `MISSING.md`; no replacement historical artifact was invented. The canonical supplied package itself is complete.
