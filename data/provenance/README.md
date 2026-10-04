# Provenance capture review

The scheduled Google Docs workflow creates a **staging artifact**, not a verified
dataset and not controlled evidence.

For each capture proposed for persistent use:

1. Download the workflow artifact before its retention period expires.
2. Extract it so `google_docs_manifest.csv` and `raw/` are direct children
   of a directory named `provenance_capture/`.
3. Run `python scripts/validate_provenance_capture.py provenance_capture`.
4. Review document identity, source/release semantics, license/usage terms, and
   whether the captured text is the intended source revision.
5. Preserve the reviewed raw artifact in an approved immutable location and
   record its SHA256.
6. Update `registry/data_provenance_registry_v0.1.csv` through a reviewed pull
   request with source identity, release/version, acquisition date/method,
   transformation history, integrity check, and evidence status.
7. Set `Provenance_Status=verified` only when the registry's verified-evidence
   requirements are actually satisfied.

CI capture never auto-promotes provenance, dataset eligibility, experiment
eligibility, controlled support, or physical support.
