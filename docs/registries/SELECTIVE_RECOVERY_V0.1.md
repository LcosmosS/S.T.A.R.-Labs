# Selective recovered-asset intake: v0.1

This is an **evidence-only selection ledger**, not a dataset promotion, new bulk upload, or controlled experiment. The governing source is `charter/STAR_Research_Charter_v0-2.pdf`; frozen audit source files and protocols are not modified.

## Scope

- Two *previously committed* historical SDSS/MaNGA inputs are selected for the matching-reconstruction work. Their committed Git LFS pointer bytes, dataset manifest hashes and sizes, and existing **independent empty-cache download evidence** must all agree.
- Two additional Dropbox candidates are documented without asserting upstream provenance: `/STAR/PhotoObj_pmqr771.csv` (120,891,007 bytes; new LFS candidate) and `/STAR/Stellar_Mass2_Table_cleaned.csv` (646,455 bytes; named in the historical SFR report). Dropbox metadata is not a SHA-256 digest.
- No remote LFS upload for these *new* candidates occurred in this PR. **Do not commit a pointer for them** or assume a filename match proves a dataset identity.
- No recovered notebook, pickle, or model is executed. No historical scientific evidence is reclassified.

## Independent upload gate (for a future dedicated intake PR)

1. Establish release, source/query, selection criteria, acquisition time, license and exact byte digest.
2. Inspect schema, PII/secrets, record counts, identifiers and duplication; distinguish raw data from derived targets or train-set products.
3. Check `git check-attr filter -- <target>` reports `lfs`; stage *real bytes* with a trusted Git LFS client, not a handcrafted pointer.
4. Push all required LFS object blobs with the actual LFS batch protocol before publishing the corresponding Git commit.
5. Clone or download with a **fresh LFS cache** and independently hash the hydrated bytes; verify checksum, size and manifest linkage.
6. Add a new versioned registry candidate overlay, only after the proof exists. Keep all execution/support gates false pending prospective validation.

The current GitHub Git-object connector cannot perform Git LFS batch upload or independent hydrated download, and the local environment cannot resolve github.com. Therefore no new LFS objects are represented as committed here. See `registry/recovered_asset_selection_v0.1.json` for machine-readable status.

Verification: `python tools/validate_selective_lfs.py`; this runs read-only, fails on fabricated/mismatched LFS pointers, and does not hydrate assets. Recovered files remain in their established locations.
