# M1-INH-E1 — Szekeres-Szafron Inhomogeneous Elliptic Sufficiency Audit

## Governance state

- Obstruction ID: `M1-INH-E1`
- Claim: `CLAIM-ACSC-MECH-002`
- Parent sector: GR + irrotational pressureless matter
- Status: **planned**
- Controlled execution: **disabled**
- Controlled support: **not established**
- Physical support: **not established**

This is a class-relative obstruction program. It does not claim to disprove all
possible elliptic mechanisms in cosmology.

## Scope

The audit concerns the Szekeres-Szafron dust+`Lambda` family in which the
radial/time evolution admits an elliptic reduction while additional
nonspherical free functions control spatial structure.

No Cremona data, BSD quantities, historical `Phi_0`, survey topology, or
astronomy-fitted parameters enter this audit.

## M1-INH-E1a — exact reduction

Reproduce from the Einstein equations the registered Szekeres-Szafron evolution
equation and its Weierstrass/elliptic representation. Identify exactly which
free functions determine the elliptic evolution data.

This stage reproduces known mathematics; it is not a new physical-support
claim.

## M1-INH-E1b — field-level insufficiency

Construct two regular, physically inequivalent solutions `S1` and `S2`
such that

[
\mathfrak E[S_1]=\mathfrak E[S_2]
]

for the complete registered elliptic evolution data, while

[
\rho_{S_1}\neq\rho_{S_2}
]

on an open region.

The intended construction holds the radial evolution data fixed and varies an
independent nonspherical Szekeres function while preserving regularity and
avoiding reliance on a coordinate artifact.

A successful construction permits only the conclusion:

> Elliptic evolution data are insufficient to reconstruct the complete matter
> inhomogeneity in the registered Szekeres-Szafron class.

It does not permit the conclusion that no other theory can achieve elliptic
structure sufficiency.

## M1-INH-E1c — observable-specific sufficiency

Field non-injectivity does not automatically imply that every lossy topological
or statistical observable differs.

For any later candidate observable `Q`, sufficiency must therefore be tested
separately. A counterexample pair satisfying

[
\mathfrak E[S_1]=\mathfrak E[S_2],
\qquad
Q[S_1]\neq Q[S_2]
]

falsifies elliptic sufficiency for that specific observable inside this class.

No observable is selected by this preregistration. Selection remains subject to
the mechanism-program observable embargo where applicable.

## Differential criterion

For a candidate observable, a local obstruction is a physically admissible
variation satisfying

[
D\mathfrak E(\delta\lambda)=0
]

but

[
DQ(\delta\lambda)\neq0.
]

Equivalently, observable sufficiency requires

[
\ker D\mathfrak E \subseteq \ker DQ
]

on the physical solution space under consideration.

## Interpretation boundary

A successful E1b or E1c result is a negative theorem for a specified solution
class or observable. It is not a universal no-go result, does not establish
ACSC, and does not activate a DESI or other physical correspondence test.
