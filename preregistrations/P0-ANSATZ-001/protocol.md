# P0-ANSATZ-001 — Parent-Theory Eligibility and Closed Search Frame v0.1

## Governance state

- Search frame: `P0-SF-v0.1`
- Mechanism claim: `CLAIM-ACSC-MECH-001`
- Search status: **preregistered_closed**
- Candidate count: **5**
- Controlled execution: **disabled**
- Controlled support: **not established**
- Physical support: **not established**
- Search-frame cutoff: **2026-10-07**
- Historical ACSC/GLMPCT inputs permitted during construction: **no**
- Cosmic target observable selected during P0/P1: **no**

This protocol is a theory-eligibility preregistration. It is not a controlled
physical result, and it does not claim that the five registered candidates
exhaust all possible physical theories.

## Purpose

P0-ANSATZ-001 asks whether S.T.A.R. has any independently motivated parent
physical theory from which a structure-determining principle can be derived
without reference to the historical arithmetic-cosmological correspondence.

The admissible logical direction is

[
\mathcal T \longrightarrow P_1 \longrightarrow \mathfrak E
\longrightarrow \mathcal D \longrightarrow Q,
]

where:

- `T` is an independently motivated parent physical theory;
- `P1` is a structure-determining principle derived from that theory;
- `E` is an endogenous elliptic/modular sector;
- `D` is the resulting physical dynamics;
- `Q` is an observable selected only after the preceding construction is frozen.

The reverse direction is prohibited:

[
Q \longrightarrow \mathfrak E \longrightarrow P_1 \longrightarrow \mathcal T.
]

## Scope of the exhaustion claim

`P0-SF-v0.1` is an operationally closed S.T.A.R. search frame. It is not a
claim that theoretical physics has a finite hypothesis space.

When all five registered candidates have terminal audited statuses, the search
frame is exhausted in the following restricted sense:

> No eligible parent theory was found within the prospectively registered
> P0-SF-v0.1 search frame.

If all candidates fail, the permitted program-level conclusion is:

> Mechanism-level ACSC-v0.1 is retired as an active S.T.A.R. physical
> hypothesis under P0-SF-v0.1.

The following conclusion is prohibited:

> No possible physical theory can ever connect elliptic structure to cosmic
> structure.

A later independently developed theory may motivate a new search-frame version;
it may not retroactively change the result of v0.1.

## Admission criteria

Every candidate in the frozen search frame was required, before detailed
elliptic analysis, to satisfy all of the following.

1. **Prior independent existence.** The theory or ansatz exists in the
   scientific literature independently of S.T.A.R.
2. **Independent physical motivation.** It addresses relativistic structure
   formation, collisionless self-gravitating matter, cosmic acceleration,
   modified gravitational dynamics, cosmological perturbation growth,
   structure formation by physical defects, or a recognized gravitational
   consistency problem.
3. **Explicit dynamics.** It has a defined action, field equations, or
   equivalent well-posed dynamical system.
4. **Inhomogeneous degrees of freedom.** It permits physical inhomogeneities;
   a homogeneous background alone is insufficient.
5. **Structure relevance.** It contains variables capable of changing density
   contrast, shear, tidal fields, velocity dispersion, defect structure, or
   equivalent structure-forming degrees of freedom.
6. **No ellipticity-first selection.** Presence or suspected presence of
   Weierstrass functions, elliptic curves, modular forms, or genus-one
   fibrations is not an admission reason.
7. **Pre-cutoff literature.** The independent framework predates this
   preregistration.
8. **Distinct dynamical content.** Trivial coordinate rewritings, parameter
   relabelings, or simple limits of another registered candidate are not
   separate candidates.

## Frozen candidate set

The complete P0-SF-v0.1 search frame is:

1. `P0-T001` — General relativity + irrotational pressureless matter.
2. `P0-T002` — Einstein-Vlasov collisionless matter.
3. `P0-T003` — General relativity + canonical exponential quintessence.
4. `P0-T004` — Brans-Dicke-`Lambda` scalar-tensor gravity.
5. `P0-T005` — Einstein-Abelian-Higgs topological-defect cosmology.

The canonical machine-readable definitions are in
`registry/theory_candidate_registry_v0.1.csv`.

After the first detailed P0 derivation begins, this list is immutable for
v0.1. A newly encountered theory requires a new search-frame version.

## One-representative rule

Each candidate class has one registered representative definition. After audit
begins:

- no alternative potential may replace the registered scalar potential;
- no alternative matter sector may be substituted;
- no extra field may be added;
- no modified gauge group may replace the registered Abelian-Higgs model;
- no parameter may be selected because it creates elliptic integrability;
- no within-class model shopping is permitted.

A failure of the registered representative is retained as a failure of that
registered candidate. It is not silently replaced.

## Required P0 audit for every candidate

Each candidate receives the same audit.

### P0.1 Independent motivation

Document the pre-S.T.A.R. physical reason for considering the theory.

### P0.2 Governing dynamics

Freeze the exact action/equations and their physical dimensions.

### P0.3 Degrees of freedom

Enumerate dynamical fields, constraints, gauge variables, propagating modes,
and freely specifiable initial/boundary data.

### P0.4 Symmetries

Record diffeomorphism invariance, internal gauge symmetries, global/discrete
symmetries, topological restrictions, and relevant conserved quantities.

### P0.5 Inhomogeneous structure sector

Identify the variables that control density contrast, shear, tidal fields,
velocity dispersion, defects, or equivalent structure-generating modes.

### P0.6 Standard recovery regime

State and derive the appropriate standard-physics limit.

### P0.7 Endogenous elliptic test

Ask whether the registered theory itself forces a genus-one, elliptic, or
modular structure:

[
\mathcal T \vdash \mathfrak E.
]

Mere mathematical compatibility is insufficient. If ellipticity is optional,
selected after the fact, or imposed by representation choice, the candidate
does not pass this gate.

### P0.8 Candidate P1 derivation

If an endogenous elliptic sector exists, determine whether the parent equations
themselves constrain the independent structure-generating modes. The constraint
may not be imposed merely because it removes elliptic-blind directions.

### P0.9 Elliptic-blind variation test

Determine whether physically admissible variations exist such that

[
D\mathfrak E(\delta\lambda)=0
]

while a structure variable changes:

[
D\mathcal I(\delta\lambda)\neq0.
]

If such variations survive and the parent theory does not independently remove
them, the candidate fails structure-determining sufficiency.

### P0.10 Contamination audit

Certify that the construction was not selected or tuned using:

- historical `Phi_0`;
- Cremona or LMFDB data;
- discriminant/conductor/rank distributions;
- prior ACSC or GLMPCT outcomes;
- DESI, SDSS, MaNGA, GAMA, or other target survey topology;
- SFR performance;
- persistent-homology results;
- symbolic-regression expressions fitted to target astronomy;
- any chosen cosmic-web summary.

## Observable embargo

No primary physical observable `Q` may be registered during P0 or P1.

This is stronger than blinding its measured value. The observable itself must
not yet be chosen. Only after a candidate has passed P0 and produced a derived
P1 may the project ask which observables the theory predicts.

## Candidate status vocabulary

The only candidate audit states are:

- `REGISTERED_UNTESTED`
- `FAILS_INDEPENDENT_MOTIVATION`
- `FAILS_DYNAMICAL_SPECIFICATION`
- `FAILS_STANDARD_LIMIT`
- `NO_ENDOGENOUS_ELLIPTIC_SECTOR`
- `ELLIPTIC_REPRESENTATION_ONLY`
- `FAILS_P1`
- `FAILS_STRUCTURE_SUFFICIENCY`
- `PASSES_P0`
- `PASSES_P1`
- `RETIRED`

Failed records are never deleted.

## Exhaustion rule

The search frame is exhausted when all five registered candidates have terminal
audited states. Operationally:

[
N_{\rm unresolved}=0.
]

The count is registry-derived. No elapsed time, publication count, or subjective
judgment such as "enough theories have been tried" constitutes exhaustion.

## Midstream expansion rule

Once the first candidate leaves `REGISTERED_UNTESTED`, the candidate list is
immutable for v0.1. New theories may be documented but require
`P0-SF-v0.2` or later.

## Program decision rule

### At least one candidate passes P0

The positive mechanism track may open only for that exact registered theory.
Passing P0 does not activate an empirical ACSC experiment and establishes no
physical support.

### All candidates fail P0

`ACSC-MECH-v0.1` is retired under this search frame. The exact permitted
conclusion is:

> No independently motivated parent theory in P0-SF-v0.1 produced an eligible
> route to a structure-determining elliptic mechanism.

### Candidates reach P1 but all fail structure sufficiency

`ACSC-MECH-v0.1` is retired at the structure-sufficiency gate, with each
surviving elliptic-blind physical degree of freedom recorded.

## Construction embargo

The following artifacts are specifically prohibited from selecting or modifying
the P0/P1 theories, couplings, fields, constraints, or parameter values:

- the historical primary projection `Phi_0`;
- historical rank scaling;
- Cremona or LMFDB distributions;
- DESI or other survey topology;
- historical SFR results;
- historical ACSC correlations;
- persistence-diagram matches;
- astronomy-fitted symbolic-regression expressions.

This does not delete or suppress those artifacts. It prevents them from
contaminating the mechanism derivation.

## Search-frame source basis

The five candidates have independent literature bases concerned with gravity,
structure formation, kinetic matter, dark energy, modified gravity, or
defect-seeded structure formation. Representative sources are recorded in the
candidate registry. Presence of elliptic structure was not an admission
criterion.

## Execution boundary

P0-SF-v0.1 is a governance/theory-search preregistration, not an executable
numerical experiment. Therefore all controlled-execution, controlled-support,
and physical-support flags remain false.

If a later candidate yields an executable derivation/test, that work must
receive a separate Experiment_ID, parameter specification, inputs/provenance,
and any applicable null/control definitions through the existing controlled
transaction system.

## Surviving program after retirement

If mechanism-level ACSC-v0.1 is retired, the following may continue:

- historical reconstruction of ACSC/GLMPCT;
- mathematical study of endogenous elliptic/modular structures in cosmological
  equations;
- class-relative no-go and insufficiency theorems;
- FLRW/Szekeres elliptic reductions as mathematical-physics results;
- independently justified successor mathematical frameworks;
- provenance/reproducibility methodology;
- cross-domain comparisons explicitly labeled as exploratory mathematical
  associations.

Retirement does not convert a class-relative negative result into a universal
no-go theorem.
