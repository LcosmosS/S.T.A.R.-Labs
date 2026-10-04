# EXP-MAP-A01 preregistration — primary arithmetic projection null test

## Governance state

- Qualified experiment: `REPO-CSV-v0.2:EXP-MAP-A01`
- Dataset: `REPO-CSV-v0.2:DATA-ARITHMETIC`
- Parameter set: `PAR-MAP-001`
- Null model: `NULL-MAP-001`
- Protocol version: `EXP-MAP-A01-prereg-v1`
- Controlled execution: **disabled**
- Controlled support: **not established**
- Physical support: **not established**

This PR contains protocol commitment and validation machinery only. It contains
no controlled experiment result.

The historical PDF namespace also used the literal string `EXP-MAP-A01` for a
broader mapping-family comparison. That is not an alias. The repository-qualified
experiment is now defined narrowly as the single primary-projection null test
below. PTD, MCJ, FT, IWT, cosmological joint inference, SFR modeling, TDA, and
rank-scale sensitivity are outside this protocol.

## Canonical source and provenance

`DATA-ARITHMETIC` is anchored directly to the repository's existing ecdata git
submodule:

- upstream: `https://github.com/JohnCremona/ecdata.git`
- repository gitlink: `data/ecdata`
- pinned commit: `25cec5ecfec8b9f016eb1631ac633194c2bed39f`
- source commit date: `2026-02-04T16:54:47Z`
- controlled provenance capture: `2026-10-04`
- canonical file: `allcurves/allcurves.00000-09999`
- Git blob SHA-1: `baab5801d7f81e1d5c44f5eb5acf4f1e100bc90b`
- SHA-256: `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`
- byte size: 2,146,401
- rows: 64,687
- conductor range: 11 through 9,999
- upstream license: Artistic License 2.0
- upstream README release-family DOI: `10.5281/zenodo.161341`

The canonical input is the whitespace-delimited upstream `allcurves` file,
not a CSV conversion and not the historical derived
`cremona_3selmer_full_pari.csv`.

### allcurves schema

Every source line must parse exactly as:

`conductor isogeny_letter curve_number [a1,a2,a3,a4,a6] rank torsion_order`

Malformed or blank lines abort the protocol.

## Analysis cohort

Rank is invariant under isogeny. Treating all 64,687 curves as independent
records would therefore build a known arithmetic redundancy into the endpoint.

The preregistered cohort retains **exactly curve number 1 from each isogeny
class**. At the pinned source revision this yields exactly **38,042** analysis
records.

No other filtering, imputation, rank fallback, outlier removal, resampling, or
post-result cohort change is allowed.

The canonical curve label is `<conductor><isogeny_letter><curve_number>`.
The canonical analysis order is ascending `(conductor, isogeny_class)`.

## Arithmetic quantities

The conductor and algebraic rank are read directly from the pinned `allcurves`
record.

The integral Weierstrass discriminant is recomputed exactly from
`[a1,a2,a3,a4,a6]`:

`b2=a1^2+4a2`

`b4=2a4+a1*a3`

`b6=a3^2+4a6`

`b8=a1^2*a6+4*a2*a6-a1*a3*a4+a2*a3^2-a4^2`

`Delta=-b2^2*b8-8*b4^3-27*b6^2+9*b2*b4*b6`

A zero discriminant aborts execution.

## PAR-MAP-001 — locked primary projection

For every retained curve:

`longitude = 360 * ln(|Delta|) / ln(10^30)`

`latitude  = 180 * ln(N)       / ln(10^9)`

`elevation = 200 * rank`

Locked choices:

- natural logarithm;
- `DELTA_MAX=10^30`;
- `N_MAX=10^9`;
- rank scale `200`;
- no clipping;
- no sample-derived renormalization;
- no fitting or jitter;
- regulator excluded;
- exact integer arithmetic precedes binary64 logarithm/geometry conversion.

These constants are historical candidate model choices under test, not uniquely
derived physical constants.

## Primary endpoint

The protocol has one inferential endpoint.

1. Construct each curve's `(longitude, latitude)` base point.
2. Find its `k=10` nearest distinct neighbors by Euclidean base-plane distance.
3. Resolve equal-distance ties by canonical Cremona label in ASCII order.
4. Convert the directed neighbor relation to the sorted set of unique undirected
   edges.
5. Compute

   `T = -mean(|elevation_i - elevation_j|)`

   over those edges.

Larger `T` means greater local elevation/rank coherence.

Elevation is not used to construct the neighbor graph. No alternative k,
distance metric, persistence statistic, clustering score, subgroup endpoint, or
secondary hypothesis is part of this experiment.

## NULL-MAP-001 — locked null

The null keeps fixed:

- curve identities;
- discriminants;
- conductors;
- base coordinates;
- base neighbor graph;
- empirical rank/elevation multiset.

Ranks are permuted across the fixed curve identities.

Locked null settings:

- realizations: `B=999`;
- seed: `1729`;
- algorithm: `splitmix64-fisher-yates-v1`;
- one sequential 64-bit SplitMix64 state;
- no discarded or regenerated null realizations.

The PRNG/permutation is implemented in the experiment module so the null
sequence is independent of NumPy's high-level permutation implementation.

## Inferential rule

For observed statistic `T_obs` and null values `T_b`:

`p = (1 + count(T_b >= T_obs)) / (B + 1)`

with a preregistered one-sided threshold `alpha=0.01`.

- `p < 0.01`: reject this rank-permutation null for this endpoint.
- otherwise: do not reject this null.

Either outcome is admissible. Rejection does not establish ACSC, cosmological
correspondence, BSD, or physical support.

## Output contract

A controlled run must create:

- `summary.json`
- `observed_projection.csv`
- `null_statistics.csv`

The controlled runner separately records and hashes all outputs, stdout/stderr,
Git state, registry records, environment identity, source hashes, and exit
status.

## CI subset correction

`data/raw/ci_subset.csv` is **not** the controlled input.

The prior file was malformed: its 800 data rows were exactly the first 800
records of `ecdata/alllabels/alllabels.110000-119999` copied as one CSV field,
for example `110001 a 2 110001 a 1`. Those are label-mapping records, not
individual Cremona curve labels.

This preregistration regenerates the CI fixture from the pinned
`allcurves.00000-09999` source as a genuine one-column CSV of the first 800
number-1 representative labels. That repair is CI/data-hygiene only and does
not enter the controlled endpoint.

## Activation boundary

Merging this preregistration must leave:

- experiment `Controlled_Execution_Eligible=false`;
- dataset `Controlled_Execution_Eligible=false`;
- controlled support `false`;
- physical support `false`.

The executable runner spec is committed against the preregistration snapshot.
Because the runner hashes complete registry rows, a later activation PR that
changes the two execution-eligibility booleans must mechanically refresh the
experiment and dataset binding hashes in the spec. No scientific field may
change in that activation PR.

The activation PR may merge only if:

1. the ecdata gitlink remains the pinned commit above;
2. the source SHA-256 and row/class counts revalidate;
3. only the eligibility booleans and mechanically consequent binding hashes
   change;
4. `star-controlled-experiment preflight` succeeds on the activation branch;
5. no endpoint, dataset selection, projection constant, null setting, seed, or
   output contract changes.

Primary results must appear only after activation. An independent rerun and
scientific review are required before controlled-support promotion is considered.
