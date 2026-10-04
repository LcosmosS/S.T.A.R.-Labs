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

**Status:** completed

Implemented `src/entropy/fisher_rao_geodesics.py`.

Changes:
- added the exact radius-2 great-circle representation of Fisher–Rao geodesics;
- added the raw-weight normalization and velocity pushforward;
- added an explicit nonnegative `pseudocount` parameter with default zero;
- reject negative raw weights and undeclared zero-weight interiorization;
- added analytic first-boundary-time detection;
- stop before the singular simplex boundary instead of clipping through it;
- added runtime checks for simplex normalization, sphere radius, and constant Fisher speed;
- return structured diagnostics containing model ID, boundary time, termination state, and invariant errors;
- added no dependency on the historical approximate Christoffel or Euler integrator.

## EG-STAB-004 — Mathematical regression tests

**Status:** completed

Implemented `tests/test_fisher_rao_entropy_geodesics.py`.

Coverage:
- positivity of the entropy-derived Fisher metric on a nonzero tangent vector;
- square-root isometry between Fisher norm and Euclidean sphere norm;
- raw-velocity pushforward satisfies the simplex tangent constraint;
- exact geodesic conserves simplex normalization and Fisher speed;
- RuntimeWarnings are elevated to errors in the stabilization fixture;
- zero velocity gives a stationary geodesic;
- first boundary contact is analytic, reported, and never crossed by clipping;
- zero weights require an explicit pseudocount;
- an explicit pseudocount produces an interior state;
- negative raw weights remain invalid even with a pseudocount;
- direct simplex velocities must satisfy the tangent constraint.

## Integrity statement

The existing files

- `src/entropy/entropy_geodesics.py`
- `src/entropy/entropy_field.py`
- `tests/test_entropy_geodesics.py`

remain historical/current prototype artifacts unless a later reviewed change explicitly supersedes them. v0.1 is additive.

## EG-STAB-005 — Review boundary

**Status:** active

This branch is ready for CI/review as an additive candidate treatment. No registry,
claim-status, evidence-status, or historical-source mutation is included. Promotion
into a controlled experiment requires a separate reviewed decision that fixes the
input interpretation, any pseudocount, integration interval, and acceptance/null
criteria.
