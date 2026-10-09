# Prospective VizieR acquisition: ALFALFA α.100

**Do not add these templates as operational registry rows.** `dataset_registry_v0.1.csv` is audit-pinned (45 datasets) and historical controls are immutable. Proposed new identity: `REPO-CSV-v0.2:DATA-VIZIER-ALFALFA100`; it is not currently registered. A future, reviewed registry *version bump* and linked provenance row must happen before selecting it as a canonical source or enabling its sky overlay.

## Original, independently named source

- VizieR: [J/ApJ/861/49/table2](https://vizier.cds.unistra.fr/viz-bin/VizieR-3?-source=J%2FApJ%2F861%2F49%2Ftable2).
- Source: Haynes et al. (2018), *The Arecibo Legacy Fast ALFA Survey: The ALFALFA Extragalactic HI Source Catalog*, DOI 10.3847/1538-4357/aac956.
- CDS catalogue DOI: 10.26093/cds/vizier.18610049. Table2 is the corrected **August 2019** ALFALFA extragalactic HI catalogue, **31,502 rows according to VizieR** (count before any user filtering).
- Essential exact VizieR fields: `AGC` (catalogue ID), `RAJ2000` and `DEJ2000` (HI centroid **sexagesimal** coordinates), `RAO` and `DEO` (associated *optical* counterpart **sexagesimal** coordinates, nullable), `Vhel` (km/s), `W50` (km/s), `e_W50`, `HIflux` and `e_HIflux` (Jy km/s), `SNR`, `rms` (mJy), `Dist` (Mpc), `logMHI`, and `HI` source class. Missingness is valid scientific information; do not map absent optical counterparts to the radio centroid.

## Frozen acquisition receipt, BEFORE joins or hypothesis testing

1. Via VizieR, export the **complete** table2 to VOTable/FITS or TSV; pin exact query URL/request bytes, response date, mirror, original bytes SHA-256, content length, response headers, publisher catalogue DOI, corrected August 2019 table designation, license and raw field metadata/units. Prefer VOTable for explicit column units/coordinates. Record `expected_source_rows=31502` but **abort rather than truncate** if a provider limit/filter yields fewer rows. An API row-limit default must be disabled deliberately.
2. Validate raw schema, full row count, stable `AGC` duplicate count, NULL markers, coordinate degree/hour conversions, frame/epoch, optical missingness, quality-code distributions. Preserve *raw export* unchanged and hashed; create a **separate derived** `source_id,ra_deg,dec_deg` CSV for sky preview. Use `AGC` for source IDs **only after duplicate-ID audit**. Freeze the derived file's SHA-256, converter source SHA and source/derived row mappings in a manifest.
3. Explicitly label derived coordinate role: choose `optical_counterpart` for SDSS positional assessment using nullable `RAO/DEO`, and `HI_centroid` for separate telescope beam/uncertainty assessment with `RAJ2000/DEJ2000`. **Do not apply an arbitrary 2-arcsecond null to HI centroid positions**: ALFALFA's radio beam and position uncertainties differ from optical imaging. Choose match uncertainty, selection, angular geometry, velocity agreement and one-to-many policy *prospectively*, after footprint and error characterization but before looking at associations.
4. Freeze a survey-mask-aware shifted-position/random-control protocol for false-association rates; compare optical counterparts to SDSS and assess redshift/velocity compatibility separately. Record unmatched sources and multiplicity. A visual Aladin inspection cannot certify an association or justify parameter tuning.
5. Register the immutable source and derived identity *separately* through a reviewed, versioned dataset/provenance/crosswalk transition; leave execution/support/physical flags false. Do not relabel the historical `DATA-MANGA-HI-ALL` working set or `DATA-SDSS18-200K` as ALFALFA.

## Pending canonical-registry row templates

See `dataset_registry_row.template.csv` (14 **existing** columns) and `data_provenance_registry_row.template.csv` (21 **existing** columns). `PENDING_SHA256`, `PENDING_DATE`, `PENDING_LICENSE`, and `PENDING_ACQUISITION_RECORD` are explicit blockers and MUST NEVER be imported to operational registries or used for eligibility. Derive stable manifest object paths as `data/intake/vizier/alfalfa100/<frozen_acquisition_id>/`, with a manifest of original and derived hashes, parent ID, schema, calibration context, and software versions; raw VOTable/FITS payloads need correctly uploaded, verified LFS objects if they cross repository file-size policies. Never forge LFS pointers.

## Sky-view use

STARMAP's separate Aladin panel accepts **already-listed** dataset scope IDs `DATA-SDSS18-200K` and `DATA-MANGA-HI-ALL` only, and requires an exact user-declared SHA-256 matching a local, normalized ICRS coordinate CSV. This is a local byte verification, **not** canonical provenance acceptance. The new ALFALFA candidate cannot be selected there until reviewed registry integration adds its scope, manifest and gate tests. No VizieR data were downloaded, no coordinate subset was fabricated, and no matches or astrophysical results were produced.

Cite [VizieR corrected ALFALFA table2](https://vizier.cds.unistra.fr/viz-bin/VizieR-3?-source=J%2FApJ%2F861%2F49%2Ftable2), CDS DOI [10.26093/cds/vizier.18610049](https://doi.org/10.26093/cds/vizier.18610049), and Haynes et al. [2018](https://doi.org/10.3847/1538-4357/aac956).
