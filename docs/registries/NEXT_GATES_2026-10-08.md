# S.T.A.R. next gates — post-recovery audit, 2026-10-08

**Source of authority:** `charter/STAR_Research_Charter_v0-2.pdf` and its [charter summary](../../charter/RESEARCH_CHARTER_v0.2.md). This is a *prospective decision record*, not a retrospectively reconstructed scientific result. **No canonical registry row, frozen audit snapshot, controlled runner, null outcome or physical-support flag is modified.** See `registry/preregistration_transition_candidates_v0.1.json`.

## Gate ordering and evidence requirements

| Gate | Observable completion requirement | Current decision |
|---|---|---|
| G0 — engineering correctness | fail-closed runner/registry checks, offline data fixtures, stable CI, isolated outputs | substantially complete as software; does **not** imply data or scientific support |
| G1 — immutable source identity | source release/githash, SHA-256, valid row count, schema, units and selection | `DATA-ARITHMETIC` verified; SDSS/MaNGA identity still under reconciliation |
| G2 — prospective protocol | experiment/claim/dataset/param/null identities, exactly one primary endpoint, settings, exclusions, null, seed and alpha committed *before testing* | A01 preregistered; MCJ A03 has a newly committed prospective protocol; DATA-A01 and CTRL-A02 only design drafts |
| G3 — canonical lifecycle transition | explicit validator-preserving migration of planned→preregistered (and locked param/null records), complete code and spec binding | A03 migration pending; do **not** alter original frozen-audit baseline silently |
| G4 — controlled activation | same pinned data/protocol/code, only eligibility fields and consequent spec hashes change; controlled runner preflight on clean branch | not open |
| G5 — result and independent replication | first permitted run, signed/hashes manifest, independent executor rerun, fail/negative result preserved | no new controlled science result claimed |
| G6 — astrophysical relevance | independent survey test with geometry/selection controls, significance and replication | not established |
| G7 — physical support | independent cross-survey correspondence, conventional astrophysical baselines, domain/systematic alternatives ruled out, model prediction before exposure | not established |

## Priority 0: preserve A01 (already preregistered)

`EXP-MAP-A01`: fixed ecdata 38,042 isogeny representatives; k=10 rank-elevation coherence; 999 fixed-base rank permutations; seed 1729; alpha=0.01. Confirm hash-bound preflight and execute through its **separate activation** gate without refitting constants, switching endpoints or merging with the successor MCJ experiment. Independent rerun is a distinct gate.

## Priority 1: `EXP-MAP-A03` MCJ (most immediate planned→prereg)

The source is the **same already locked** 64,687-row ecdata file, with unique isogeny-class representatives and a fully prospective rank-blind `(log N,Re(log j),Im(log j))` mapping. A03 tests only internal arithmetic rank coherence under a conductor-decile conditional permutation. New singular-case rules (j=0 exclusion), k=10 graph, alpha=0.005, 999 null draws and seed 4103 are frozen in `preregistrations/EXP-MAP-A03/config.json`. Neither A01 nor A03 tests cosmology. Before canonical transition, implement *and test* exact c4/Delta/j calculations, principal-log sign/branch, coordinate duplicates and neighbor ties, PRNG and non-overwriting output. Have the governance validator explicitly permit the named transition without allowing silent changes to historical definitions or unrelated rows.

## Priority 2: `EXP-DATA-A01` matching (high scientific leverage; currently blocked)

Known negative evidence: legacy 1,495-row SDSS–HI artifact fails its two-arcsecond claim, with a repeated MaNGA ID. The recovered TOP-200000 SDSS query and its renamed CSV improve acquisition provenance but do not prove the complete joined survey identity. Before preregistration: lock source IDs/epoch/units, astronomical spherical geometry, multiplicity policy, a survey-aware coordinate-shift null and output refusal rules. The candidate's 2-arcsecond primary radius and 1/3-arcsecond sensitivity are **design proposals, not a completed null**. Use the reconstructed matches as an input-quality test, not cosmic correspondence evidence.

## Priority 3: `EXP-CTRL-A02` leakage audit (must precede SFR significance)

Historical SFR scripts contained target-derived proxies and global imputation/scaling before split. Freeze `log_SFR_Ha` derivation, prohibit target-leaking predictor aliases, assign groups before fitting, and freeze ordinary astrophysics baseline and redshift/mass/sky-aware arithmetic null. Invalid prior reported scores are diagnostic only. Defer `EXP-SFR-A01`, `EXP-L001` and stronger cosmological claims until this gate is met.

## What not to promote

- PTD A02: periods need canonical full/half normalization, computational precision and independent source/algorithm checks.
- Topology A01: no null-calibrated filtration or settled physical comparator; historic W2<0.01 is not a criterion.
- ECC B01: if theta=dM globally, dtheta=0; nontrivial cohomology requires a different closed non-exact construction.
- RTCH B01: must reproduce ordinary Einstein/thermodynamic limits before fitting cosmology.
- M1/P0 preregistered *theory* search is separate; unresolved analytic cases are mathematics gates, not permission to assert a universal theorem.

## Crossmatch methodological context

Pineau et al., *Probabilistic positional association of catalogs of astrophysical sources: the Aspects code*, A&A (2014), DOI [10.1051/0004-6361/201220021](https://doi.org/10.1051/0004-6361/201220021), discusses positional-association uncertainty. The citation is **context**, not independent validation of recovered S.T.A.R. matches.

## Snapshot discipline

The current audit validator historically permits only the reviewed A01 planned→preregistered exception. For A03, first implement/validate its frozen design, then write a **separate explicit registry transition PR** with a targeted validator update, a v0.1→v0.2 transition record, and freshly validated controlled-spec input/code hashes. The state of the existing canonical experiment and parameter/null registries remains authoritative until that change merges. Any dataset/parameter/null mismatch, input mutation, missing source or test mismatch is a hard stop. Do not auto-execute historical notebooks or serialized models.
