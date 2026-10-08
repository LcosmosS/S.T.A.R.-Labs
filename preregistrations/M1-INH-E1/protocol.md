# M1-INH-E1 — Szekeres-Szafron Inhomogeneous Elliptic Sufficiency Audit

## Governance state

- Obstruction ID: \`M1-INH-E1\`
- Claim: \`CLAIM-ACSC-MECH-002\`
- Parent sector: GR + irrotational pressureless matter
- Status: **planned**
- Controlled execution: **disabled**
- Controlled support: **not established**
- Physical support: **not established**

This is a class-relative obstruction program. It does not claim to disprove all
possible elliptic mechanisms in cosmology.

## Scope

The registered obstruction sector is the \(\beta_{,z}\neq0\)
Szekeres-Szafron dust+\(\Lambda\) family in comoving coordinates
\((t,x,y,z)\), with signature \(+---\). The time/radial evolution admits a
Weierstrass reduction while additional nonspherical free functions control
spatial structure.

No Cremona data, BSD quantities, historical \`Phi_0\`, survey topology, or
astronomy-fitted parameters enter this audit.

The frozen source convention for the exact reduction is the independent
pre-S.T.A.R. treatment in Kraniotis and Whitehouse,
\`arXiv:gr-qc/0105022\`, especially its Szekeres-Szafron equations and
Weierstrass reduction. The audit may rederive these equations but may not change
their registered meaning after E1b begins.

## Registered Szekeres-Szafron sector

The metric functions are written as

\[
ds^2
=
dt^2-e^{2\alpha}dz^2-e^{2\beta}(dx^2+dy^2),
\]

with

\[
e^\beta=\Phi(t,z)e^{\nu(z,x,y)},
\qquad
e^\alpha
=
h(z)e^{-\nu(z,x,y)}
\partial_z\!\left(e^\beta\right),
\]

and

\[
e^{-\nu}
=
A(z)(x^2+y^2)
+2B_1(z)x
+2B_2(z)y
+C(z).
\]

The spatial free functions obey

\[
A(z)C(z)-B_1(z)^2-B_2(z)^2
=
\frac14\left[h(z)^{-2}+K(z)\right].
\]

The registered dust+\(\Lambda\) evolution equation is

\[
\dot{\Phi}(t,z)^2
=
-K(z)
+\frac{2M(z)}{\Phi(t,z)}
+\frac{\Lambda}{3}\Phi(t,z)^2.
\]

The matter-density sector is spatially sensitive. In the same convention, after
separating the cosmological-constant contribution, the matter density may be
written as

\[
\kappa\widetilde{\rho}
=
\frac{
2M_{,z}+6M\nu_{,z}
}{
\Phi^2\left(\Phi_{,z}+\Phi\nu_{,z}\right)
}.
\]

Thus \(A,B_1,B_2,C,h\) can alter \(\nu_{,z}\), and hence the density geometry,
without appearing as independent variables in the radial evolution equation.

## Frozen Weierstrass convention

Define

\[
X=-\frac{1}{\Phi}.
\]

For fixed \(z\), introduce the parametric variable \(u\) by

\[
u
=
\int
\left[
-2M(z)X^3
-K(z)X^2
+\frac{\Lambda}{3}
\right]^{-1/2}
dX.
\]

Then define

\[
X
=
-\frac{\xi+K(z)/12}{M(z)/2}.
\]

The reduced equation is

\[
\left(\frac{d\xi}{du}\right)^2
=
4\xi^3-g_2(z)\xi-g_3(z),
\]

with the frozen invariants

\[
g_2(z)=\frac{K(z)^2}{12},
\qquad
g_3(z)
=
\frac{K(z)^3}{216}
-\frac{\Lambda M(z)^2}{12}.
\]

On a nondegenerate elliptic interval,

\[
\Delta_{\wp}(z)
=
g_2(z)^3-27g_3(z)^2
\neq0,
\]

and

\[
\xi(u,z)
=
\wp\!\left(u+\epsilon;g_2(z),g_3(z)\right).
\]

Accordingly,

\[
\Phi(t,z)
=
\frac{M(z)/2}{
\wp\!\left(u+\epsilon;g_2(z),g_3(z)\right)
+K(z)/12
}.
\]

Equivalently, if \(v_0(z)\) is chosen so that

\[
\wp(v_0;g_2,g_3)=-\frac{K(z)}{12},
\]

then the denominator may be written
\(\wp(u+\epsilon)-\wp(v_0)\).

The physical time is fixed by

\[
t+f(z)=\int \Phi\,du,
\]

together with the selected connected physical branch. The discrete branch data
must identify the connected interval, the sign of \(\dot{\Phi}\), and the
chosen representatives of the Weierstrass inverse modulo its period lattice.
No branch may be changed between the two solutions in an E1b/E1c comparison.

Degenerate points with \(\Delta_{\wp}=0\) are recorded but are not treated as
nondegenerate elliptic points in this obstruction test.

## Registered elliptic-evolution data record

Before E1a begins, the complete registered elliptic-evolution record is fixed as

\[
\boxed{
\mathfrak E[S]\big|_J
=
\left(
M(z),
K(z),
f(z),
\Lambda,
\epsilon,
v_0(z),
\sigma(z);
g_2(z),
g_3(z),
\Delta_{\wp}(z)
\right)_{z\in J}
}
\]

for a common open radial interval \(J\) on which the chosen physical branch is
regular. Here \(\sigma(z)\) denotes the discrete branch data just specified.

The entries \(g_2,g_3,\Delta_{\wp}\) are derived from \(M,K,\Lambda\) but are
retained explicitly in the record so that the elliptic curve used by the audit
is unambiguous.

The functions

\[
A(z),\ B_1(z),\ B_2(z),\ C(z),\ h(z)
\]

are **not** components of \(\mathfrak E\). They are the registered
elliptic-blind spatial sector, subject to their field-equation constraint above.

For E1b/E1c,

\[
\mathfrak E[S_1]=\mathfrak E[S_2]
\]

means componentwise equality of this complete record on the same interval
\(J\), in a common comoving radial gauge and with identical branch conventions.
A pair related only by a coordinate transformation or gauge relabeling is not a
valid counterexample.

## M1-INH-E1a — exact reduction

Starting from the Einstein equations for the registered sector, reproduce and
check the frozen evolution equation, Weierstrass normal form, invariants, time
relation, and density expression above.

E1a is a verification of the preregistered record. It may identify an algebraic
or convention error, in which case the audit stops and records
\`FAILS_DYNAMICAL_SPECIFICATION\`; it may not redefine \(\mathfrak E\) after
seeing the E1b/E1c outcome.

This stage reproduces known mathematics; it is not a new physical-support
claim.

## M1-INH-E1b — field-level insufficiency

Construct two regular, physically inequivalent solutions \`S1\` and \`S2\`
such that

\[
\mathfrak E[S_1]=\mathfrak E[S_2]
\]

for the complete registered elliptic-evolution record while

\[
\widetilde{\rho}_{S_1}\neq\widetilde{\rho}_{S_2}
\]

on an open spacetime region.

The intended construction holds the entire registered record fixed and varies
the elliptic-blind spatial sector
\((A,B_1,B_2,C,h)\) within the field-equation constraint, preserving regularity
and avoiding any pair related only by a diffeomorphism or coordinate artifact.

A successful construction permits only the conclusion:

> Elliptic evolution data are insufficient to reconstruct the complete matter
> inhomogeneity in the registered Szekeres-Szafron class.

It does not permit the conclusion that no other theory can achieve elliptic
structure sufficiency.

## M1-INH-E1c — observable-specific sufficiency

Field non-injectivity does not automatically imply that every lossy topological
or statistical observable differs.

For any later candidate observable \(Q\), sufficiency must therefore be tested
separately. An exact counterexample pair satisfying

\[
\mathfrak E[S_1]=\mathfrak E[S_2],
\qquad
Q[S_1]\neq Q[S_2]
\]

falsifies elliptic sufficiency for that specific observable inside this class.

No observable is selected by this preregistration. Selection remains subject to
the mechanism-program observable embargo where applicable.

## Differential criterion

The differential test is restricted to regular points of the physical solution
space. Let \(\mathcal S_{\rm reg}\) be a local smooth solution manifold on which
\(\mathfrak E\) and \(Q\) are \(C^1\), and assume \(D\mathfrak E\) has locally
constant rank so that the exact level set

\[
\mathfrak E^{-1}\!\left(\mathfrak E[S]\right)
\]

is locally a smooth submanifold whose tangent space at \(S\) is

\[
T_S\mathfrak E^{-1}\!\left(\mathfrak E[S]\right)
=
\ker D\mathfrak E_S.
\]

Under these regularity and fiber-tangency assumptions, a local differential
obstruction is a physically admissible tangent variation
\(\delta\lambda\in T_S\mathcal S_{\rm reg}\) satisfying

\[
D\mathfrak E_S(\delta\lambda)=0
\]

but

\[
DQ_S(\delta\lambda)\neq0.
\]

If \(Q\) admits a differentiable local factorization
\(Q=q\circ\mathfrak E\), then a necessary condition is

\[
\ker D\mathfrak E_S
\subseteq
\ker DQ_S.
\]

Failure of this inclusion at a regular point therefore obstructs a
differentiable local factorization of \(Q\) through \(\mathfrak E\). It does
**not** by itself establish failure of exact sufficiency at a singular point or
on a disconnected fiber.

Exact observable insufficiency under E1c is established only by the exact
equal-\(\mathfrak E\), unequal-\(Q\) pair specified above.

## Interpretation boundary

A successful E1b or E1c result is a negative theorem for a specified solution
class or observable. It is not a universal no-go result, does not establish
ACSC, and does not activate a DESI or other physical correspondence test.
