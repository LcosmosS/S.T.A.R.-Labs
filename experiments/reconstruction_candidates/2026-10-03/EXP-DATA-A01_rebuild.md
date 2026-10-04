# EXP-DATA-A01 — spherical cross-match reconstruction

Date: 2026-10-03. Status: reconstruction candidate; no rebuilt match or controlled result is claimed.
Namespace: `STAR-PDF-v0.2:EXP-DATA-A01`. Repository IDs must be interpreted through `docs/registries/NAMESPACE.md`.

## Goal and evidence

Rebuild SDSS/HI integration using true spherical angular distance, explicit keyed joins, duplicate control, tolerance sensitivity, and locked input/code hashes. Audit findings E-LCL-001 and E-LCL-002 and `historical/r&d/docs/provenance_audit_v0.3/local_match_checks.json` govern the starting assessment. The inspected 1,495-row tables associate every row with one MaNGA ID; all recomputed separations exceed the declared two-arcsecond tolerance. This rejects those associations, not the underlying catalogs or the general matching hypothesis.

The quarantined originals remain in `historical/r&d/quarantine/2026-10-03_audit/sdss_hi_match/`. They must never be a default controlled-analysis input.

## Reconstruction protocol

1. Acquire and lock each upstream release/query, acquisition date, coordinate frame, epoch, angular units, object-key semantics, row count and SHA256. Preserve source licenses and catalog documentation. An identifier rename is not an identity crosswalk.
2. Validate RA/declination bounds, missing values and units. Compute great-circle distance using spherical coordinates, including RA wrap and poles. Preserve original coordinates, source IDs, match coordinates and separation in arcseconds.
3. Define one-to-one/one-to-many policy, nearest-neighbor ambiguity, tie handling and maximum radius before matching. Validate keyed joins separately from coordinate matching; record all unmatched and rejected associations.
4. Pre-register a tolerance family such as 1, 2 and 3 arcseconds. Report counts, separation distributions, duplicate multiplicities, source-density dependence and estimated false matches using coordinate-shift or suitable spatial null controls.
5. Verify every accepted row satisfies its declared radius. Keep a rejection table, uniqueness diagnostics and deterministic counterexamples. Include round-trip and RA-wrap/pole fixtures.
6. Pin the implementation commit, environment, parameter file and seeds. Save input/output hashes, split IDs where used, join diagnostics and a working-directory-independent run manifest.

## Acceptance gate

All accepted rows must meet the chosen spherical tolerance, duplicate/ambiguity policy and source-key checks. An independent implementation must agree within declared numerical tolerance. Data lineage and false-match uncertainty must be documented before downstream controlled use. The old artifact's failed associations remain negative/diagnostic provenance even if a rebuild succeeds.

## Deliverables

Versioned clean match table, rejected/ambiguous match tables, tolerance report, exact source/code/environment manifest, meaningful matching tests and a registry status decision. No cosmological inference follows from successful catalog joining alone.
