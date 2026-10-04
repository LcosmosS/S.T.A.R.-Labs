# Entropy–Geodesic Stabilization Treatment v0.1

**Model identifier:** `ECC-ENTROPY-GEODESIC-FR-v0.1`  
**Status:** candidate mathematical/computational treatment  
**Evidence status:** not empirical evidence; not physical validation  
**Parent prototype:** `src/entropy/entropy_geodesics.py`  
**Integrity rule:** the historical prototype is preserved unchanged. This treatment is implemented in a separate module and must not be substituted into a registered experiment without an explicit parameter-set update.

## 1. Purpose

The historical entropy-geodesic prototype attempts to evolve a trajectory using

[
ddot x^k+Gamma^k{}_{ij}dot x^idot x^j=0
]

with a metric described as the Hessian of a Shannon-like entropy field. Numerical tests show overflow and invalid-value warnings. The objective of v0.1 is **not** to hide those warnings with clipping. It is to specify a Riemannian state space and geodesic flow for which:

1. the metric is positive definite on the allowed tangent space;
2. the geodesic equation is mathematically defined;
3. the numerical implementation preserves its defining invariants to stated tolerance;
4. singular boundaries are reported rather than crossed silently;
5. any interior regularization is explicit and parameterized.

## 2. Why the historical prototype is not used as the controlled stabilized model

The historical implementation is retained as provenance, but it has four mathematical/numerical problems.

### 2.1 Sign of the Shannon Hessian

For

[
S(p)=-sum_{i=1}^n p_ilog p_i,
qquad p_i>0,quad sum_i p_i=1,
]

the ambient Hessian is

[
D^2S(p)=-operatorname{diag}(p_1^{-1},ldots,p_n^{-1}).
]

Therefore (D^2S) is negative definite, not a positive Riemannian metric. The natural positive metric induced by entropy is

[
g_p=-D^2S(p)
=operatorname{diag}(p_1^{-1},ldots,p_n^{-1}),
]

restricted to the simplex tangent space

[
T_pDelta^{n-1}
=left{uinmathbb R^n:sum_i u_i=0ight}.
]

This is the Fisher–Rao/Shahshahani metric.

### 2.2 The state space is constrained

Entropy probabilities live on the open simplex

[
Delta_{++}^{n-1}
={pinmathbb R^n:p_i>0, sum_i p_i=1},
]

not unconstrained Euclidean space. Velocities must be tangent to the simplex.

### 2.3 Christoffel symbols require metric derivatives

For a metric (g),

[
Gamma^k{}_{ij}
=rac12 g^{kell}
left(
partial_i g_{ell j}
+partial_j g_{ell i}
-partial_ell g_{ij}
ight).
]

Metric entries themselves cannot be substituted for these derivatives. v0.1 therefore avoids an ad hoc Christoffel approximation entirely.

### 2.4 Explicit Euler stepping is unnecessary here

For the Fisher–Rao simplex, a closed-form geodesic representation exists. Using it removes the Euler instability without modifying the differential equation.

## 3. Entropy metric and square-root isometry

Define

[
Psi:Delta_{++}^{n-1}	o S_{++}^{n-1}(2),
qquad
Psi(p)=q=2(sqrt{p_1},ldots,sqrt{p_n}),
]

where (S^{n-1}(2)) is the sphere of radius 2 and the subscript (++) denotes its positive orthant.

For (uin T_pDelta^{n-1}),

[
DPsi_p[u]_i=rac{u_i}{sqrt{p_i}}.
]

Hence

[
langle DPsi_p[u],DPsi_p[v]angle_{mathbb R^n}
=sum_irac{u_i v_i}{p_i}
=g_p(u,v).
]

Thus (Psi) is an isometry from the Fisher–Rao simplex to the positive orthant of the radius-2 sphere.

## 4. Exact geodesic

Let (p_0inDelta_{++}^{n-1}) and (u_0in T_{p_0}Delta^{n-1}). Set

[
q_0=2sqrt{p_0},
qquad
w_0=DPsi_{p_0}[u_0]
=rac{u_0}{sqrt{p_0}}.
]

Because (sum_i u_{0i}=0),

[
q_0cdot w_0=2sum_i u_{0i}=0,
]

so (w_0) is tangent to the sphere. Let

[
sigma=|w_0|_2.
]

If (sigma=0), the geodesic is stationary. Otherwise,

[
q(t)
=
q_0cosleft(rac{sigma t}{2}ight)
+
2rac{w_0}{sigma}
sinleft(rac{sigma t}{2}ight).
]

The corresponding simplex trajectory is

[
p_i(t)=rac{q_i(t)^2}{4}
]

for as long as every (q_i(t)>0). The tangent velocity is

[
u_i(t)=rac12 q_i(t)dot q_i(t).
]

No Euler update, velocity cap, coordinate clipping, or pseudoinverse is part of the geodesic dynamics.

## 5. Conserved quantities and software invariants

For every valid interior point of the exact trajectory:

[
sum_i p_i(t)=1,
]

[
|q(t)|_2^2=4,
]

and the Fisher speed is constant,

[
g_{p(t)}(u(t),u(t))
=
sum_irac{u_i(t)^2}{p_i(t)}
=
sigma^2.
]

The implementation must check these invariants against a declared numerical tolerance and fail if they drift beyond tolerance.

## 6. Boundary semantics

The Fisher–Rao metric is singular at (p_i=0). v0.1 therefore does **not** clip a component to an epsilon and continue as if nothing happened.

For each component,

[
q_i(t)=a_icos	heta+b_isin	heta,
qquad
	heta=rac{sigma t}{2},
]

with (a_i=q_{0i}>0) and (b_i=2w_{0i}/sigma). The first positive root determines the first boundary contact. The controlled implementation reports the earliest such time and returns only states strictly before that boundary.

Crossing the boundary would require a separately specified extension of the model.

## 7. Mapping raw nonnegative weights into the simplex

The mathematical model is defined on (p), not arbitrary Cartesian coordinates. For compatibility with S.T.A.R. projected weights, v0.1 permits an explicit normalization map.

For strictly positive raw weights (x),

[
p_i=rac{x_i}{sum_j x_j}.
]

For raw velocity (v=dot x), the induced simplex tangent velocity is

[
u
=
rac{v-psum_j v_j}{sum_j x_j}.
]

This satisfies (sum_i u_i=0).

### Optional pseudocount

A nonnegative parameter (alpha) may be declared explicitly:

[
p_i
=
rac{x_i+alpha}{sum_jx_j+nalpha}.
]

This is an **interiorization policy**, not part of the unregularized Fisher–Rao model. The default is (alpha=0). If any required weight is nonpositive and (alpha=0), the implementation must fail rather than guess a correction.

Any experiment using (alpha>0) must record (alpha) in its parameter set.

## 8. Interpretation limits

This construction establishes a mathematically coherent entropy-derived information geometry. It does **not** establish that:

- S.T.A.R. arithmetic coordinates are thermodynamic probabilities;
- Fisher–Rao geodesics are physical particle trajectories;
- the entropy field is a physical entropy without an operational thermodynamic definition;
- the stabilized trajectory validates ECC, RTCH, ACSC, or GLMPCT.

Those remain separate hypotheses requiring independent experiments.

## 9. Acceptance criteria for v0.1

The stabilization implementation is acceptable as a mathematical software model only if tests establish:

1. positivity of the Fisher metric on nonzero simplex tangent vectors;
2. the square-root isometry numerically;
3. simplex normalization conservation;
4. constant Fisher speed;
5. stationary behavior for zero tangent velocity;
6. deterministic boundary detection;
7. rejection of nonpositive undeclared weights;
8. explicit behavior when a pseudocount is supplied;
9. no overflow/invalid warnings on the stabilization test fixture.

Passing these criteria is a software/mathematical consistency result, not empirical support.
