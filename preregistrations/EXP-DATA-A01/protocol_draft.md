# EXP-DATA-A01 — prospective crossmatch design; NOT YET PREREGISTERED

**Canonical current status: planned.** Qualified identity is `REPO-CSV-v0.2:EXP-DATA-A01`; do **not** alias it to `STAR-PDF-v0.2:EXP-DATA-A01`. This document supplements, but does not change, `experiments/reconstruction_candidates/2026-10-03/EXP-DATA-A01_rebuild.md`.

## Proposed research question

Can a deterministic, spherical and ambiguity-controlled SDSS–MaNGA-HI crossmatch reproduce a high-purity source association under preregistered chance-association controls, and reject the known corrupted 1,495-row legacy match without deleting it?

## Candidate protocol (cannot be locked yet)

- Independent inputs: recovered `SDSSDR18_200000.csv` and `mangaHIall.fits`, already real Git LFS objects, but their *upstream source-to-canonical DATA-SDSS18-200K/DATA-MANGA-HI-ALL lineage* is still pending scientific acceptance.
- Geometry: ICRS angular separation from unit-vector dot-products or `SkyCoord.separation`, RA wrap and poles supported.
- Candidate search primary radius `2 arcsec`; sensitivity only `1,3 arcsec`. Explicitly distinguish one-to-many matches and coordinate duplicates; no arbitrary first-match policy.
- Prospective null: repeated fixed-angle coordinate shifts *large relative to the match radius* but within a justified survey footprint, with exposure/mask handling, and false-association uncertainty. **Shift magnitudes, mask logic, repeat count, and unique-match policy remain unselected**; this is not a registered null.
- Proposed output: accepted pairs, rejected/ambiguous pairs, proper ID crosswalk, arcsecond separations, shift-null summary, locked manifests, independently reproduced angular computations.

## Blocking gates before canonical preregistration

1. Resolve intended source catalog release, matching epoch/frame, stable identifiers, CSV precision and prior CasJobs `TOP 200000` lack of `ORDER BY`; verify full 18-column CSV byte/row-level schema. A researcher-provided sample is not a full-file audit.
2. Define fixed one-to-one-versus-ambiguous policy, coverage and spatial mask, shift null and uncertainty budget **without examining reconstructed match yields**.
3. Freeze exact `PAR-MATCH-001` and `NULL-MATCH-001` via an explicit validator-approved lifecycle transition; verify no namespace alias.
4. Implement independent spherical test vectors (RA 359.999/0.001, poles, ties, duplicates) and a second matching implementation; keep quarantine inputs excluded by default.

**Current flags:** execution=false, controlled support=false, physical support=false. No actual reconstructed match or measured false-positive rate is asserted. Crossmatch methods reference: Pineau et al., *A&A* (2014), DOI 10.1051/0004-6361/201220021.
