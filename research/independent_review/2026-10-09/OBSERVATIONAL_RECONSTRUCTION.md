# Observational reconstruction — falsification-first intake

**Scientific status:** fixture-level diagnostics only; canonical `EXP-DATA-A01`, `EXP-DATA-A02`, `EXP-CTRL-A02`, and SFR experiments remain planned. Frozen design candidates: [DATA-A01 draft](../../../preregistrations/EXP-DATA-A01/protocol_draft.md), [CTRL-A02 draft](../../../preregistrations/EXP-CTRL-A02/protocol_draft.md). Parent Charter [PDF](../../../charter/STAR_Research_Charter_v0-2.pdf).

## Contamination and provenance blockers

The historical 1,495-row SDSS/HI associations are quarantined: separation recalculations exceed the claimed 2 arcsec radius and repeated MaNGA identifier violates one-to-one integrity. Do **not** copy/repair this result and claim it was the original source. The SDSS DR18 200k sample still lacks independently locked release/CasJobs SQL/`TOP` ordering/retrieval identity; some records are `STAR`, and negative redshift values demand explicit, predeclared galaxy selection. The MaNGA-HI FITS **raw bytes** have publisher-level verified provenance, which is necessary but insufficient for row-selection/association admission. The recovered Pipe3D file and historical SFR derived targets likewise lack an accepted raw-to-target/feature/split contract.

## Concrete implementation already in repository

`src/data/spherical_match_candidate.py` provides radius-2-arcsec unit-vector KDTree candidate enumeration with haversine distance and an explicit ambiguity bucket. `src/quality/sfr_leakage_gate.py` rejects direct target proxies and cross-group leakage. Synthetic tests exist, but cannot calibrate real-sky purity. This branch adds a **separate dependency-free independent spherical reference** using `atan2(norm(cross),dot)`; randomized RA wrap, near-pole and pair-multiplicity fixtures compare it with the existing implementation. Neither source receives inferred source IDs or astronomy outcomes.

## Locked-data admission sequence (must be future separate preregistration)

1. **Source immutable manifest:** original publisher URL/release, license, download time, full byte SHA256/size, SQL query and response ID where applicable, FITS/HDU/column schemas, coordinate system/equinox/epoch, redshift quality, galaxy-vs-star filtering, primary identifier and exact source-to-derived transforms.
2. **Sky geometry:** test RA modulo 360, poles, coincident records, 2-arcsec boundary and floating stability. Preserve all candidate pairs and sorted separations; compare unit-sphere KDTree against independent great-circle formula and `astropy.coordinates.SkyCoord` at expert review.
3. **Ambiguity:** define before outcomes whether strict unique one-to-one, likelihood-ratio/positional-error matching, or quarantine of one-to-many, both-direction duplicates and blended HI detections; preserve rejected pairs with reason codes.
4. **Control null:** fix survey overlap masks and completeness/exposure, sky-shift magnitude/direction/number/seeds avoiding wrap and mask leakage, uncertainty model, false-association estimator and alpha. Current source draft intentionally **does not** fix these parameters; do not invent them or promote to preregistered.
5. **Leakage-free SFR:** freeze H-alpha conversion/calibration/dust/IMF assumptions, feature lineage graph, column aliases, target descendants, grouped (galaxy/field/sky) train-validation-test split, nested preprocessing and baseline comparisons. Never use an arithmetic rank feature without an independently derived galaxy-to-arithmetic association.
6. **External replication:** second independently maintained matcher, blind signed/zero-separation fixtures, source data manifests, chance-coincidence uncertainty and held-out survey; preserve negative match yield or weak SFR performance.
7. **Only after all locks:** separate canonical lifecycle PR for each target, reviewer approval, activation preflight, controlled execution. Never reclassify all 17 planned rows in bulk.

References: Budavári & Szalay (2008), DOI 10.1086/587156; Pineau et al. (2014), DOI 10.1051/0004-6361/201220021. Literature methods do not certify this dataset.
