# M1-INH-E1b — independent numerical curvature spot check

**Date:** 2026-10-09. **Frozen scope:** [M1-INH-E1](../../../preregistrations/M1-INH-E1/protocol.md); comparison with [metric-first symbolic proof record](../../../preregistrations/M1-INH-E1/evidence/metric-first/M1-INH-E1b_metric_first_proof_record.md). **Evidence:** numerical consistency only; **NOT** peer-reviewed theorem or complete E1a verification.

## Different route

The original verifier uses symbolic generic-metric Ricci differentiation and symbolic `SO(2)` reduction. This audit instead computes from the **explicit 4x4 metric**, without substituting supplied Einstein tensor components, using JAX double-precision forward-mode automatic differentiation. It reconstructs all mixed Einstein tensor components and checks `G^a_b - 3 delta^a_b = diag(rho,0,0,0)`. Independently sample-compute the transverse gradient of the Einstein-derived trace and use the repeated shear-plane spatial metric to obtain `J`. No recorded symbolic certificate values were inputs to curvature differentiation.

### Registered witness

`P=[2(1+z)]^(1/3) sinh(3(t+z)/2)^(2/3)`, `H=coth(3(t+z)/2)`, `B=1/[3(1+z)]`, `F=H²-1`, `q=exp(2z)(x²+y²)`, `d=(1-q)/(1+q)`.

- `S1:` `a=P(H+B)`, `c=2P`;
- `S2:` `a=P(H+B+d)`, `c=2P exp(z)/(1+q)`;
- `rho1=3FB/(H+B)`, `rho2=3F(B+d)/(H+B+d)`;
- `J1=0`, `J2=36 H²F² q/[P²(H+B+d)^4(1+q)²]`.

## Independent numerical run (executed, no cosmological data)

The audit used Python + JAX 0.9.0.1 CPU with x64 enabled. A derivative-based Christoffel-to-Ricci-to-Einstein implementation was evaluated at points strictly inside the proposed regular domain.

| Sector | `(t,z,x,y)` | Max absolute `G^a_b -3δ^a_b-T^a_b` | `J` from curvature finite-difference gradient | Analytic `J` |
| --- | --- | --- | --- | --- |
| S1 | (1.3,0.10,0.20,0.10) | 1.76e-15 | 1.26e-25 | 0 |
| S1 | (1.8,-0.17,-0.15,0.25) | 1.51e-15 | 2.02e-23 | 0 |
| S2 | (1.3,0.10,0.20,0.10) | 1.78e-15 | 3.0246199541016246e-05 | 3.024619976047543e-05 |
| S2 | (1.8,-0.17,-0.15,0.25) | 1.33e-15 | 4.615559792500682e-06 | 4.615559815744113e-06 |

All four field-equation residuals were below 2e-11 and absolute `J` errors below 2e-6; actual errors for S2 were under 2.4e-13. `J1` was numerically zero and `J2` positive at sampled off-axis points. Re-run the [standalone optional JAX verifier](../../../scripts/m1_e1b_independent_autodiff.py) to check on a separate CPU, recording environment and SHA. It deliberately is **not** part of default CI or the controlled experiment suite.

### Non-overclaiming

- **Not proved by sampled checks:** full-domain equality `G-Lambda g=kappaho u u`, global regularity, equality of all frozen elliptic branch data, intrinsic construction of the two-plane from the curvature-determined dust flow and shear, universal nonisometry, general E1a derivation.
- To upgrade the math status: rederive general E1a under fixed sign/inverse-Weierstrass convention; reproduce exact E1b symbolic certificates from a clean environment; verify the full-domain positivity/flatness and eigenprojector, and secure **independent external mathematical referee sign-off** on every assumption.
- The candidate nonisometry argument remains plausible because `J` is a diffeomorphism scalar once constructed from uniquely curvature-determined matter and shear. That underlying geometric reconstruction still needs exact proof audit rather than extrapolation from the samples.
