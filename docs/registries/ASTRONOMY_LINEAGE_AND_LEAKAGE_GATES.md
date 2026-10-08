# DATA-A01 and CTRL-A02 — fixture-only source integrity and leakage gates

The connected Dropbox `/STAR/` folder contains the named SDSS/MaNGA/Pipe3D files; this review captures **size and Dropbox revision metadata only**, not raw bytes, SHA-256, release/lineage or executed match/model results. See `data/provenance/star_source_receipts_v0.1.json`. Duplicated names in `/STAR/Documents/STAR/` have **not** been proven byte-identical. No file content or LFS pointer is committed here.

### Observational constraints
- The recovered `SELECT TOP 200000` without `ORDER BY` cannot fix a survey sample's ordering, and supplied rows show `class=STAR` / negative redshift. A galaxy-only science target requires an explicit prospective `class='GALAXY'`, positive-z and quality selection; the original raw file remains unmodified.
- The historical 1,495-row SDSS/HI merge violated a nominal two-arcsecond separation. It remains immutable negative evidence.
- A source resolver must establish the actual CasJobs execution/export, release, original RA/Dec precision, plate/MJD/fiber versus MaNGA identifier and astrometric epoch for both catalogs.
- Fixture-only `src/data/spherical_match_candidate.py` computes stable spherical separations (RA wrapping and poles), enumerates all candidates within a *proposed* 2-arcsecond radius, rejects ambiguous bipartite associations rather than silently taking the first. It **does not implement a chance-match null**; footprint geometry, coordinate-shift magnitudes, mask handling and multiplicity acceptance are unresolved and EXP-DATA-A01 stays planned.

### SFR controls
- The historical `log_SFR_Ha_raw` alias must not predict `log_SFR_Ha`; leakage aliases, target derivatives and shared group IDs are fail-closed in fixture code.
- Any imputer/scaler must be **fitted only on training folds**. No full-catalog transform, supervised feature selection, sky-window optimization or target-proxy input before splitting.
- A synthetic Ridge pipeline is **not** a scientific SFR baseline or measured score. `DATA-PROVENANCE-ALL` is unverified; `PAR-LEAK-001/NULL-LEAK-001` remain unregistered. Independent MaNGA/Pipe3D release/provenance, target derivation, model baseline and group/sky split must be frozen before CTRL-A02, then SFR-A01.

No controlled experiment or empirical data processing is authorized by this PR. Negative evidence remains preserved; canonical registries, LFS objects, support and physical claims remain unchanged.
