# CasJobs SDSS 200k source binding — addendum (2026-10-08)

**Status:** historical acquisition/reconstruction candidate only. Governed by [Research Charter v0.2](../../../../charter/STAR_Research_Charter_v0-2.pdf), especially §§12–13, 15, 17, 28, 30–32, 36–37. This addendum does **not** supersede the frozen provenance audit, grant eligibility, or retroactively preregister any analysis.

## Recovered identity

The existing [CasJobs SQL history](../../code_log/2026-10-08_recovered/queries/4672dd7d2691021d782a24bfb1c02be29b86f2e372192312a379ea729d8e2c5a.txt) ends with the pmqr771 account's `SELECT TOP 200000 ... INTO mydb.MyTable`. It selects **18 columns**, in this order:

```text
objid,ra,dec,u,g,r,i,z,run,rerun,camcol,field,specobjid,class,redshift,plate,mjd,fiberid
```

It joins `PhotoObj p` to `SpecObj s` on `s.bestobjid=p.objid`. Its literal predicates are `p.u BETWEEN 0 AND 19.6` and `g BETWEEN 0 AND 20`. **Do not silently amend the historical SQL** to qualify `g`. The history reports `(200000 Row Table)` and has no `ORDER BY`, `class='GALAXY'` or positive-redshift filter. Therefore STAR and negative-redshift records in the recovered sample are compatible.

The recovered [v0.3 audit](../../docs/provenance_audit_v0.3/local_findings.md) independently recorded an as-found 18-column CSV header. Its archived Windows download-origin sidecar binds the original `MyTable_pmqr771_0.csv` name to `SDSSDR18_200000.csv`.

The original **33,007,497-byte** CSV is **already present** at [the hash-addressed intake path](../../../../data/intake/recovered/2026-10-08/9dca2008683fde4b0f7a90af5de85ee846a30a47f6f6fae3968c83dea06fa5d2.csv), with SHA-256 `9dca2008683fde4b0f7a90af5de85ee846a30a47f6f6fae3968c83dea06fa5d2`. The existing [remote Git LFS proof](recovery_lfs_verification.json) reports an independent download and hash check. **Do not recommit the CSV, fabricate a pointer, or equate a Dropbox content hash with SHA-256.**

## Important exclusions

The two distinct `SELECT TOP 5000000 ... dr18_galaxy_data` executions (293,078 and 293,065 rows) cannot directly generate this CSV: their SELECT lists contain `petroRad_r,clean`, omit `run,rerun,camcol,field`, and restrict galaxy class and redshift.

This narrower TOP-200k query supplies a plausible, header-consistent acquisition path, but an original CasJobs job ID, execution timestamp, source database snapshot and source-job output checksum have not been independently recovered. `TOP 200000` without `ORDER BY` does not reproduce exact object membership on rerun. Use the immutable recovered CSV as historical input; preserve SDSS identifiers as strings or exact integers (not spreadsheet-rounded scientific notation).

## Separate candidate reconstructions (none active)

1. **REC-CASJOBS-SCHEMA-001**: scan entire raw CSV, verify row count/header, ID precision, class/redshift distributions, missingness and query predicates.
2. **REC-SDSS-HI-MATCH-001**: rebuild a spherical, multiplicity-aware SDSS–MaNGA HI match from individually locked original inputs, with rejection logs, tolerance controls and spatial-shift null.
3. **REC-SFR-LEAK-001**: reconstruct a leakage-free SFR baseline with train-only preprocessing and explicit exclusion of target-derived features.

All three are **reconstruction candidates**, not controlled Experiment_IDs. Preserve the existing `EXP-DATA-A01` namespace boundaries and all inactive `EXP-MAP-A01` gates.

Machine-readable source-binding candidate: [JSON](casjobs_sdss18_200k_binding_2026-10-08.json).
