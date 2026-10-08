# DATA-A01 and CTRL-A02 — fixture-only source integrity and leakage gates

The connected Dropbox `/STAR/` folder contains the named SDSS/MaNGA/Pipe3D files; this review captures **size and Dropbox revision metadata only**, not raw bytes, SHA-256, release/lineage or executed match/model results. See `data/provenance/star_source_receipts_v0.1.json`. Duplicated names in `/STAR/Documents/STAR/` have **not** been proven byte-identical. No file content or LFS pointer is committed here.

### Evidence from Dropbox text extraction (not raw bytes)

`mangaHIall.csv` exposes 34 columns and 6,632 extracted data rows. Its positional fields are **`OBJRA` and `OBJDEC`**, not generic `ra/dec`; all examined coordinate pairs were in degree bounds. The table has 6,442 unique `PLATEIFU` values (190 extra occurrences) and 6,358 unique `MANGAID` values (274 extra occurrences). These multiplicities mean a naive ID-only 1:1 join or silent `drop_duplicates` is scientifically unacceptable. Confirm repeat-observation semantics and use a prospective ambiguity policy.

`filtered_Pipe3D.csv` exposes 16 columns and 10,081 extracted rows, including `log_SFR_Ha` as target; **it has no MANGAID, PLATEIFU, SDSS objid, or RA/Dec**. It is insufficient to establish a group-disjoint split or source-level SDSS/MaNGA linkage. Resolve the original Pipe3D file's stable galaxy IDs and raw target lineage before even locking `EXP-CTRL-A02`. The extracted CSV text is one character longer than Dropbox-reported file bytes, so extraction is **not** a canonical raw-byte hash basis.

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


### 2026-10-08 additional Dropbox source receipts: Zone.Identifier and divergent SQL histories

The independent source-recovery pass found **25 specific `Zone.Identifier` sidecars** in the connected Dropbox folder `/star_provenance_r&d/`, the synced directory identified locally as `C:\\Users\\pmqr7\\Dropbox\\star_provenance_r&d`. Their observed HostUrl/referrer or redacted CDS XMatch job IDs are transcribed in `data/provenance/zone_identifier_receipts_v0.1.json`. Those strings indicate historical acquisition endpoints, **not cryptographic binding to the current files**. No raw CSV/FITS source digest or upstream survey acceptance has been inferred; registry provenance and execution flags remain unchanged.

Four meaningful *filename-to-download-basename candidates* are now explicit:
- `SDSSDR18_200000.csv` -> `MyTable_pmqr771_0.csv` in the recorded CasJobs HostUrl.
- `GZ2.csv` -> `MyTable_pmqr771.csv`; **collision warning:** `MyTable_pmqr771.csv` has its own sidecar pointing to the same basename, without proof the CSV contents match.
- `SDSSDR18_G2.csv` -> `SDSSDR18_G2_pmqr771.csv` in the recorded CasJobs HostUrl.
- `Flux.csv` -> `Flux_Bigsby.csv` in the recorded CasJobs HostUrl.

Direct-origin hints with version paths include `mangaHIall.fits` under **SDSS DR17 H I v2_0_1**, `SDSS17Pipe3D_v3_1_1.fits` under **DR17 MANGA_PIPE3D v3_1_1/3.1.1**, `GEMA_2.0.2.fits` under **DR17 MANGA_GEMA 2.0.2**, and GAMA DR3 `MagPhys v06`, `StellarMasses v20`, `EnvironmentMeasures v05` and `GeometricEnvironments v01`. These are plausible upstream acquisition paths only; independently verify raw bytes, release documentation, source selection, licensing and any conversion to derived CSV before provenance promotion.

The `CDS_XMATCH` receipts contain historic `jobId` values but **sessionId tokens have deliberately not been copied** to the repository. The `VizieR_TAP` receipts contain asynchronous job-result URLs; these do not prove specific ADQL parameters, source table or crossmatch radius without the saved job request. `V147sdss12.csv` is specifically ambiguous because its referrer included `II/356/xmmom41s`; do not silently rewrite its source table.

The two Dropbox SQL histories are **not the same content**: `/STAR/CasJobs SQL History.txt` contains the terminal `SELECT TOP 200000 ... INTO mydb.MyTable` query, while `/star_provenance_r&d/CasJobs SQL History.txt` is missing that terminal query. The latter is also available as a separate 17,285-byte conversation attachment, but matching filename/size does not prove its bytes equal either Dropbox copy. The `TOP 200000` query is an exact schema/sample-compatible generating candidate for the 18-column SDSS working CSV; its CasJobs output basename agrees with the sidecar. It has **no ORDER BY**, class GALAXY criterion, or positive-redshift restriction. Job-level export association, original release identity and raw-byte equality remain **unverified**. The two different `TOP 5000000` GALAXY-filtered history queries generated different recorded row counts (~293,078 and ~293,065), and cannot be substituted for the 18-column export.

**Admission checklist:** preserve both historical SQL copies and sidecars unchanged; bind exact SQL job ID + original export filename + raw file SHA-256 + release + schema and selection; verify any renaming with actual file comparison; validate survey coordinate roles, duplicates, match uncertainty and sky footprint; obtain an independent astronomy review before separate versioned registry changes. This is an observational-data gate and has no effect on #64/A01 arithmetic activation.
