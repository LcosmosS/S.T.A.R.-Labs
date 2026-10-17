# Reproduction Protocol and Predeclared Controls

## Freeze before exchanging investigator outputs

The mathematical definitions and conventions are in `partner_proof_notes.md`. For a blind two-investigator study, both investigators should freeze independently written code, formula derivations, orientation conventions, requested mesh sizes, tolerances, and comparison criteria before comparing outputs. Do not modify criteria after seeing discrepancies without documenting a protocol revision.

## Tolerances used by the current runner

| Test | Acceptance rule |
|---|---:|
| Exact symbolic identities | Simplify to exactly zero / exact expected expression |
| SciPy 1D quadrature periods and sphere integral | Absolute deviation below `1e-10` |
| Discrete Candidate-A generating-cycle periods | Absolute deviation below `1e-9` |
| Discrete Candidate-A triangle circulations | Maximum absolute residual below `1e-9` |
| Candidate-C analytically integrated face flux | Absolute deviation below `2e-9` from `4*pi^2*q` |
| Candidate-C face-barycentre total flux | Absolute deviation below `2e-8` from `4*pi^2*q` |
| Candidate-C local response at `(0,0)` | Absolute deviation below `1e-12` from `-1` |
| Sphere solid-angle normalized flux | Absolute deviation below `1e-8` from integer charge |
| Sphere centroid/flat-facet quadrature | Per-resolution size-aware bound plus strictly decreasing errors across the requested refinement sequence |
| Chain-complex identities | Exact zero matrices, no floating tolerance |
| Betti vectors | Exact equality with the expected vector |

The mesh-size inputs `0.8, 0.5, 0.3, 0.2` are passed to Gmsh as target sizes when Gmsh is used. In the fallback backend they parameterize reproducible grid/refinement choices; actual maximum edge length is reported separately and may differ from target size. Candidate-A and Candidate-C parameter-torus grids use `N=ceil(2*pi/h)` divisions along each angular coordinate.

## Run matrix

1. **Exact controls**: symbolic Candidate A/B/C identities, transition integer test, 3D nonclosure, and `d^2=0` sanity checks.
2. **Independent quadrature**: SciPy integration of both Candidate-A periods and the sphere curvature.
3. **Discrete Candidate A**: face circulations plus the two noncontractible periods on every structured torus grid.
4. **Candidate B mesh flux**: solid-angle flux and flat-facet centroid quadrature at each sphere resolution; record absolute error and observed rate.
5. **Candidate C face flux**: analytic per-triangle integrals compared with barycentre quadrature; report total and local-face errors, plus the zero-flux/nonzero-local-response case.
6. **Chain/cochain consistency**: integer incidence/coboundary matrices with `D1 @ D0 = 0` and, for tetrahedral meshes, `D2 @ D1 = 0`.
7. **Topology**: Betti-number checks for sphere, torus, and solid ball.
8. **Independent unit tests**: run the tests directory after the reproduction pipeline.

## Required artifact retention

Keep `reproduction_results.json`, `convergence_b.csv`, `mesh_details.json`, console output, Python/dependency versions, and `implementation_manifest.json`. When changing the script, use a new output directory; the runner refuses existing targets and writes a run receipt. Do not overwrite a failed run without retaining its report. The manifest freezer refuses to replace an existing manifest; create a new timestamped snapshot instead. A review package should include discrepancies and blocked gates as well as passes.


## PR #108 provenance/runtime safeguards

- Gate PASS is derived from every expected per-shape mesh and homology record; import availability alone is insufficient. An explicit `--backend gmsh` request exits nonzero if the requested Gmsh/GUDHI gate is not PASS.
- `--backend fallback` labels Gmsh `NOT_REQUESTED`.
- Mesh targets must be finite and positive, and fallback resolution estimates are checked against documented resource budgets before allocation. Sphere refinement follows requested `h`, not input ordering.
- Each new completed run writes `run_receipt.json` with the source hash, environment, requested parameters, overall result, toolchain gate status, and hashes/byte counts of all other run outputs.
- The original `implementation_manifest.json` and historical result JSONs are preserved unchanged; retrospective run manifests are labelled as retrospective.
- Smooth gauge-transformation consistency on overlapping connection patches remains an unmet mathematical gate.
