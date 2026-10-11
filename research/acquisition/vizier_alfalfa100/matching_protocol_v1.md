# ALFALFA alpha.100 display and matching protocol v1

**Protocol state:** preregistered for source preservation and display-candidate review. No cross-match, claim test, or support transition is authorized by this protocol.

**Source lock:** corrected August 2019 VizieR `J/ApJ/861/49/table2`, catalogue DOI `10.26093/cds/vizier.18610049`, article DOI `10.3847/1538-4357/aac956`. The complete 31,502-row VOTable response and the contemporaneous VizieR ReadMe are immutable inputs. Any provider, row-count, schema, or byte change creates a new acquisition identity.

## Coordinate role and geometry

- The display candidate uses `RAJ2000` and `DEJ2000`, the H I centroid coordinates identified by VizieR as the main J2000 equatorial coordinates. Sexagesimal right ascension is converted to degrees by `15 * (hours + minutes/60 + seconds/3600)`; signed declination uses `sign * (degrees + minutes/60 + seconds/3600)`.
- `RAO` and `DEO` are nullable coordinates of an associated optical counterpart. They are audited for paired missingness but are never substituted for a missing H I centroid and are not used by the display candidate.
- Any future angular comparison must use a true unit-sphere great-circle separation computed with the stable `atan2(|u x v|, u dot v)` form. Planar RA/Dec distance, row-order pairing, and a fixed two-arcsecond H I tolerance are forbidden.

## Identity and multiplicity

- `AGC` is the source identifier. Acquisition fails on a blank or duplicated AGC identifier; rows are never silently deduplicated.
- A future external-catalogue match must retain zero, one, or many candidate counterparts per AGC until its declared decision rule is applied. The output must report unmatched sources, ambiguous sources, candidates per source, and the selected-candidate rule.
- Position alone cannot select an optical counterpart when multiple candidates survive. The future protocol must also bind the external release, footprint, velocity/redshift compatibility rule, and tie-breaking rule before associations are inspected.

## Positional uncertainty

- Table 2 does not provide per-row astrometric uncertainty columns. Consequently, this protocol authorizes display of the catalogued H I centroids but **blocks inferential cross-matching**.
- A later matching version must freeze a cited ALFALFA positional-error model or source-level uncertainty product, the comparison catalogue uncertainty, and a numerical acceptance rule before calculating associations. It may not estimate a favorable tolerance from the observed matches.
- Rows lacking the required uncertainty inputs remain unmatched/uncertain; they are not assigned a typical value or dropped without a reported count.

## Selection and display derivation

- The canonical source population is every one of the 31,502 rows. Missing optical coordinates and both H I quality codes are preserved.
- The full derived H I-centroid table contains exactly `source_id,ra_deg,dec_deg` for all source rows in VizieR order and has its own SHA-256.
- The bounded web-display candidate contains 2,000 rows selected without using position, velocity, flux, mass, quality code, or any proposed outcome. Rank every AGC by `SHA256("ALFALFA-A100-DISPLAY-v1\\0" + AGC)` and retain the 2,000 lexicographically smallest digests. Emit retained rows in original VizieR order. Freeze both the CSV SHA-256 and the newline-delimited selected-ID SHA-256.
- The 2,000-row display subset is an interface sample only. It is ineligible for population inference and cannot replace the 31,502-row canonical source.

## Null and selection-function policy

- The display has no scientific null and no association statistic. Visual alignment in Aladin is not evidence.
- A future association experiment must preregister a survey-mask-aware null before opening match results. The minimum null family is longitude/RA rotation within the valid joint footprint, with wrap-around, fixed declination, preserved source count, and the same matching/multiplicity rules as the observed sample. Rotation angles, exclusion buffers, replicate count, random seed, and primary false-association endpoint must be committed in that later protocol.
- A future analysis must retain and report ALFALFA quality-code strata, the joint sky/velocity selection, footprint exclusions, missing counterpart coordinates, and all null outcomes. Tuning on the observed association count is forbidden.

## Web admission gate

CI may certify only byte integrity, schema, coordinate conversion, deterministic selection, registry consistency, and pending-review state. Admission to `sky-overlay-releases.v1.json` additionally requires a human/off-author review receipt bound to the exact source, derived bytes, and commit. Controlled-execution, controlled-support, and physical-support flags remain false.
