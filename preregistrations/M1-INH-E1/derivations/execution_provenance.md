# M1-INH-E1a — execution provenance and reproducibility

**Evidence status:** Author-side computational verification of a general algebraic derivation. External independent review pending; no registry state transition.

## Exact local verification (2026-10-08)

- Python: `3.13.5`
- SymPy: `1.14.0`
- Canonical source: `e1a_general_einstein_reduction.py`
- SHA-256: `4a7cc4c429eb6b3f527dca1476a4237d4da8b34aeb1b236ca6d0685db88b732f`
- Git blob SHA-1: `270557976d27055b5db22b814c4dda1970dcb4f2`
- The Git blob SHA-1 of the uploaded file was compared with the local verified script: **identical**.

### Verified console output

```text
M1-INH-E1a: generic Einstein and frozen normal-form checks
PASS generic 4D Hamiltonian Einstein identity
PASS generic 4D longitudinal Einstein identity
PASS general quadratic E transverse identity
PASS z derivative of general quadratic identity
PASS 3-curvature scalar with frozen radial constraint
PASS 3-curvature longitudinal Ricci with frozen constraint
PASS general Einstein Hamiltonian density
PASS frozen X to Weierstrass cubic normalization
PASS Weierstrass discriminant factorization
PASS X-time differential relation (dX/dt)^2 = X^2 Q(X)
ALL CHECKS PASSED — not external review; E1a scope only
```

**Development failure preserved:** An initial version of the very last assertion incorrectly retained a factor of `1/P**4` after substituting `P=-1/X`, rather than expressing that prefactor as `X**4`. Its traceback was an algebra-check implementation defect, not a counterexample to the frozen normal form. The final source fixes this and all checks pass. The other nine assertions passed before this correction.

### Clean reproduction

```bash
python -m pip install 'sympy==1.14.0'
python preregistrations/M1-INH-E1/derivations/e1a_general_einstein_reduction.py
sha256sum preregistrations/M1-INH-E1/derivations/e1a_general_einstein_reduction.py
python -m pytest -q tests/test_m1_inh_e1a_general_reduction.py
```

The repository currently pins `sympy==1.13.1` in `requirements.txt`. The local result above used 1.14.0; a passing CI run under the repository pin must be verified separately.

## Boundaries

The script checks the two **generic four-dimensional curvature** identities before applying the registered ansatz, and then checks the general spatial `E` polynomial/constraint, density and Weierstrass algebra. It **does not** automatically recompute every remaining general off-diagonal component; the accompanying proof derives their vanishing and uses the contracted Bianchi identity to close the transverse equations. These steps remain visible for independent review.

This is E1a theory verification, **not** E1b external review, E1c sufficiency, P0 exhaustion, or ACSC physical support. The preregistration and all control gates remain unchanged.
