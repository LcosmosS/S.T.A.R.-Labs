# Relativistic Thermodynamic Cohomology (RTCH)

## RTCH-E1 — Arithmetic–Geodesic–Cohomological Test

RTCH-E1 is a falsifiable computational experiment for testing whether the arithmetic
state space of elliptic curves over Q develops reproducible nontrivial topology
($H^1/H^2/H^3$ signatures), whether that topology survives null models, and whether
geodesic/scalar constructions reveal invariant quantities.

## Important interpretation rule

A persistent $H_k$ feature in a finite point cloud is evidence for a topological
feature of the sampled metric space at a scale. It is NOT, by itself, proof that
the full arithmetic state space is a smooth manifold with $H^k != 0$.

RTCH-E1 therefore reports:

1. persistent homology of the observed arithmetic point cloud;
2. matched null distributions;
3. effect sizes and empirical p-values;
4. stability across seeds, feature subsets, and sample sizes;
5. graph/geodesic structure;
6. scalar embeddings and out-of-sample prediction tests.

The experiment does NOT assume a Fibonacci/Lucas/golden-ratio map, a rank-to-height
map, or a desired topology.

## Recommended progression

Start with:
    `python rtch_e1.py --mode demo`

Then use a local CSV:
    `python rtch_e1.py --mode analyze --input your_lmfdb.csv`

Or let the program query the LMFDB API:
    `python rtch_e1.py --mode download --max-conductor 500000 --download-limit 20000`

Then analyze:
    python rtch_e1.py --mode analyze --input data/lmfdb_curves.csv --n-sample 6000

For H^1/H^2/H^3, increase `--n-sample` only after the pilot is stable.

## Dependencies

Python 3.10+ recommended.

Install:
    `pip install -r requirements.txt`

Optional:
    `pip install gudhi`

The core persistent-homology calculation uses ripser when installed.
A fallback Vietoris-Rips implementation is included for small demo data, but it
is intentionally not intended for the full experiment.

## Data provenance

The current LMFDB elliptic-curve database exposes an `ec_curvedata` schema with
fields including conductor, absolute discriminant, rank, regulator, Faltings
height, j-invariant, torsion, CM, Sato–Tate and other arithmetic data.

RTCH-E1 stores the raw downloaded records and a run manifest so that the exact
dataset and parameters can be audited.

## Scientific protocol

Primary topology feature space excludes the target variable rank.

Default intrinsic features:
    log_conductor
    signed_log_discriminant
    log_abs_j
    faltings_height
    log_regulator

Rank is retained as an independent response variable when available.

Three topology families are tested:

A. Arithmetic-intrinsic:
   conductor/discriminant/j/height/regulator-derived coordinates.

B. Structural-without-regulator:
   conductor/discriminant/j/height.

C. Rank-conditioned exploratory:
   adds rank, but is NOT allowed to be presented as independent evidence that
   topology predicts rank because rank is then part of the geometry.

Null models:

N1. Independent-column permutation:
    each feature column is independently permuted, preserving every marginal.

N2. Joint-row permutation:
    entire rows are permuted before rebuilding the geometry. This is a control
    for implementation artifacts rather than a strong independence null.

N3. Rank-label permutation:
    topology is held fixed and rank labels are shuffled for prediction tests.

N4. Feature-block permutation:
    correlated arithmetic blocks can be shuffled as blocks in sensitivity tests.

Primary null for topology:
    N1, with identical preprocessing, sample size, metric, neighborhood
    parameters, and random seed.

A topology feature is called "null-surviving" only if:
    - it exceeds the predeclared observed-vs-null effect threshold;
    - empirical p-value remains below alpha after multiple-testing correction;
    - it appears in the majority of independent resamples;
    - its persistence interval has nontrivial length;
    - it is not eliminated by reasonable feature transformations.

No single run is considered decisive.

## Outputs

results/
    run_manifest.json
    observed_persistence.csv
    null_persistence.csv
    topology_summary.csv
    stability_summary.csv
    geodesics.csv
    scalar_embeddings.csv
    prediction_tests.csv
    figures/
        persistence_H1.png
        persistence_H2.png
        persistence_H3.png
        scalar_embedding.png
        geodesic_projection.png

The script also writes a machine-readable `result.json`.

## Geodesics

RTCH-E1 constructs a kNN graph from the standardized arithmetic state vectors.
Edge lengths are Euclidean distances in the declared feature metric.

Shortest paths on the graph are used as empirical geodesics. This is deliberately
more conservative than inventing a smooth metric tensor.

For each selected source/target pair, the program records:
    - graph-geodesic length
    - Euclidean chord length
    - tortuosity = geodesic/chord
    - integrated feature changes along the path

A later stage can replace this graph metric with a learned Riemannian metric,
but that should be a separate preregistered experiment.

## Scalar embeddings

The program computes several scalar candidates:

1. first principal component;
2. diffusion-style graph coordinate;
3. geodesic eccentricity;
4. distance-to-selected persistent landmarks.

These are tested for association with rank and other held-out arithmetic
quantities. Association is not called an invariant unless it is reproducible
under resampling and null testing.

## What would count as a meaningful result?

A strong mathematical result would look like:

- a stable persistent H1/H2/H3 signature;
- persistence intervals substantially longer than matched nulls;
- stability across seeds and reasonable metric choices;
- topology not caused by a single arithmetic feature;
- geodesic quantities reproducible across resamples;
- scalar coordinates that predict an independent held-out invariant;
- effect survives rank-label permutation and multiple-testing correction.

Even then, this establishes an empirical structure in the chosen arithmetic
metric representation, not a physical law.

## What would falsify the RTCH-E1 hypothesis?

Examples:

- observed persistence is statistically indistinguishable from matched nulls;
- topology disappears under small, justified feature perturbations;
- topology is entirely explained by one marginal distribution;
- geodesic/scalar quantities have no reproducible relation to held-out invariants;
- apparent structure is destroyed by duplicate/isogeny-class controls.

A null result is scientifically useful: it tells us the proposed arithmetic
state representation does not support the claimed cohomological structure.

## Positive-control topology correction

The RTCH-E1 positive control uses a complete Euclidean Vietoris--Rips distance matrix for the bounded synthetic torus sample. The kNN graph is used separately for empirical geodesics and graph-derived scalar coordinates. This separation is intentional: a sparse kNN adjacency matrix is not itself a complete metric distance matrix and must not be passed to Ripser as one.

For larger real datasets, topology is bounded to `--max-dense-topology-points` (default 1800) by a deterministic subsample rather than silently changing the meaning of the metric. Geodesic calculations continue to use the kNN graph.

The geodesic pair sampler excludes direct kNN neighbors, so reported tortuosity is based on a genuine multi-edge shortest path rather than an edge whose graph length is identical to its Euclidean chord.

## Demo safety mode

`--mode demo` is intentionally bounded to protect local machines from the combinatorial cost of Vietoris–Rips complexes. It caps the demo at 350 points, H2, 2 nulls, 2 resamples, and 50 geodesic pairs, even if larger values are supplied on the command line. The LMFDB `analyze` mode is not subject to these demo-specific caps.
