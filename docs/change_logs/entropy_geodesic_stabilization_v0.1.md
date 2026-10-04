# Entropy–Geodesic Stabilization Change Log

**Model:** `ECC-ENTROPY-GEODESIC-FR-v0.1`  
**Branch:** `research/entropy-geodesic-stabilization-v0.1`  
**Base:** `main@c562a9e1b60de90ed28a0f74e398f4b7d15e06cb`

This log records changes to the candidate stabilization treatment. Historical entropy files are not rewritten.

## EG-STAB-001 — Isolation and model-status guard

**Status:** completed

- Created a dedicated branch from `main`.
- Chose a separate-module treatment rather than modifying the historical Euler prototype.
- Declared the treatment a candidate mathematical/computational model, not physical validation.
- Declared that no claim/evidence/experiment registry status is promoted by this work.

## EG-STAB-002 — Mathematical correction

**Status:** completed in specification

- Replaced the ambiguous “entropy Hessian metric” with the positive metric (-D^2S) on the open probability simplex.
- Identified this metric with Fisher–Rao/Shahshahani geometry.
- Enforced the tangent constraint (sum_i u_i=0).
- Replaced approximate Christoffel construction with the exact square-root-sphere isometry.
- Specified an exact geodesic and explicit singular-boundary semantics.
- Made any pseudocount/interiorization parameter explicit rather than implicit.

## EG-STAB-003 — Reference implementation

**Status:** pending

Planned file: `src/entropy/fisher_rao_geodesics.py`.

Implementation requirements:
- exact great-circle evaluation;
- raw-weight-to-simplex pushforward;
- explicit optional pseudocount;
- first-boundary-time calculation;
- invariant checks;
- structured diagnostics;
- no silent clipping.

## EG-STAB-004 — Mathematical regression tests

**Status:** pending

Planned file: `tests/test_fisher_rao_entropy_geodesics.py`.

Required tests are listed in the mathematical specification.

## Integrity statement

The existing files

- `src/entropy/entropy_geodesics.py`
- `src/entropy/entropy_field.py`
- `tests/test_entropy_geodesics.py`

remain historical/current prototype artifacts unless a later reviewed change explicitly supersedes them. v0.1 is additive.
