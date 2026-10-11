# P0-SF-v0.1 — independent review worksheets (NONTERMINAL)

**Status:** Five admitted theory classes, all `REGISTERED_UNTESTED` in baseline registry, `N_unresolved=5`. This document **does not adjudicate** any candidate or trigger a canonical transition. Authority: [P0 frozen search-frame protocol](../../../preregistrations/P0-ANSATZ-001/protocol.md), [candidate registry](../../../registry/theory_candidate_registry_v0.1.csv), [transition automaton](../../../scripts/theory_search_states.py), [Charter](../../../charter/STAR_Research_Charter_v0-2.pdf).

## Audit-wide rules

Perform P0.1–P0.8 on **the frozen registered representative**, in the order prescribed. Source DOI establishes prior motivation, *not* P0 acceptance. Elliptic behavior must be **forced endogenously** by theory, not chosen via lucky solutions, gauge transformations, best-fit couplings, mapping resemblance or galaxy data. A Weierstrass ODE is not the Mordell–Weil rank of an elliptic curve over Q. Physics sign conventions differ between P0 representative `G + Lambda g=...` and M1's `G - Lambda g=...`; explicitly reconcile parameter/sign definitions before transferring lemmas.

| Candidate | Registered dynamics / independent physical motivation | Essential degrees of freedom and adverse case | Independent audit question and provisional conclusion |
| --- | --- | --- | --- |
| **P0-T001** | Einstein gravity + irrotational geodesic dust, DOI 10.1103/PhysRevD.86.023520 | Initial density/velocity, shear, tidal Weyl data and nonspherical spatial functions | M1's candidate pair offers a **possible obstruction to sufficiency of its specific elliptic evolution record**; it does **not** prove every GR+dust elliptic sector optional, or justify terminal `NO_ENDOGENOUS_ELLIPTIC_SECTOR`. **UNTESTED** |
| **P0-T002** | Einstein–Vlasov, DOI 10.1088/1475-7516/2013/11/002 | Distribution `f(x,p)`, mass-shell constraints, infinite-dimensional kinetic moments, Einstein metric | Identify a uniquely derived genus-one/modular invariant controlling all relevant inhomogeneous kinetic/metric degrees without selecting a special distribution. A homogeneous integrable example fails sufficiency. **UNTESTED** |
| **P0-T003** | GR + canonical exponential scalar `V0 exp(-lambda phi/Mpl)`, DOI 10.1088/0264-9381/30/21/214003 | Scalar perturbations, metric/matter fields, `V0` and `lambda` remain theory parameters | Derive a forced, nondegenerate elliptic sector valid across admissible inhomogeneous solutions; exclude selecting `lambda` to make an integrable potential. Verify GR/standard quintessence limit. **UNTESTED** |
| **P0-T004** | Jordan-frame Brans–Dicke–Lambda, DOI 10.3847/2041-8213/AB53E9 | `g_ab`, BD scalar, `omega_BD`, boundary/initial data, extra scalar mode | Derive correct Jordan-frame action variation, field equations and GR limit (including nontrivial caveats). Test whether elliptic record determines independent scalar/spatial modes without opportunistic `omega_BD`. **UNTESTED** |
| **P0-T005** | Einstein–Abelian–Higgs defects, DOI 10.1088/1475-7516/2012/05/026 | Higgs modulus/phase, U(1) connection, topology, metric, symmetry breaking and gauge constraints | Check global/topological sectors and full PDE dynamics; existence of elliptic vortex profiles does not automatically force a structure-determining universal elliptic invariant. **UNTESTED** |

## Deliverable for EACH candidate, separately and before terminal statuses

1. P0.1 exact source citation and prior independent physical motivation; independent referee validates citation and frozen class.
2. P0.2 field equations/action and **units/sign/gauge** derivation, independent check of identities and Bianchi/stress conservation.
3. P0.3 initial/boundary degrees, constraints and propagating variables; use actual PDE solution space rather than only homogeneous ansatz.
4. P0.4 gauge/global symmetries and transformation-invariant test quantities.
5. P0.5 inhomogeneous structure drivers, prospective obstruction examples and regularity assumptions.
6. P0.6 standard known-theory limit proved with parameter conditions.
7. P0.7 mathematical statement showing elliptic/genus-one/modular sector **necessary** vs merely *possible*; exact counterexample where possible.
8. P0.8 if P0 passes, derive P1 structure-determining factorization/sufficiency `Q=q(E)` as appropriate under observable embargo. Independent sign-off and permanent `Audit_Record_Path`.

**Terminal decisions:** only the pre-existing `scripts/theory_search_states.py` transition rules and the registered failure gate/mechanism may change a canonical status, via separately reviewed PR. `PASSES_P0` is **still unresolved**, not an eligible physical result. If all 5 become terminal failures after genuine audits, retire *only* `ACSC-MECH-v0.1` within `P0-SF-v0.1`.

## External research scope

Coley, Layden & McNutt, DOI 10.1007/s10714-019-2647-6 provides **related Szekeres invariant characterization**. Delgado Gaspar et al., DOI 10.1140/EPJC/S10052-021-09113-9 cautions against unsupported matter couplings in Szekeres models. Neither independently certifies this registered P0 decision. Original registered representative DOIs are frozen in candidate registry; bibliographic verification against the exact actions/equations should be done by an outside specialist.
