# M1-INH-E1b — metric-first exact symbolic verification

**Date:** 2026-10-07  
**Scope:** Frozen class-I Szekeres–Szafron dust + cosmological constant constructive pair; **not** the general E1a reduction.  
**Output:** Independent, executable SymPy calculation of both Einstein tensors, dust-flow projectors, shear spectral projectors, Euclidean embeddings, and curvature-derived density-gradient discriminators.  
**Audit classification:** `METRIC_FIRST_SYMBOLIC_REPRODUCTION_PASSED — EXTERNAL_REVIEW_AND_GENERAL_E1a_PENDING` (descriptive only; not a canonical registry status).  
**Registry mutation:** None. No support flags changed.

## 1. Frozen input data

Signature \(+---\); convention \(G_{ab}-\Lambda g_{ab}=\kappa\tilde\rho u_a u_b\); \(\Lambda=3\). Define

\[
M=1+z,\quad K=0,\quad f=z,\quad
P=\Phi=[2(1+z)]^{1/3}\sinh^{2/3}\!\left(\tfrac32(t+z)\right),
\quad H=\coth\!\left(\tfrac32(t+z)\right),\quad B=\frac{1}{3(1+z)}.
\]

Both input metrics are expressed as

\[
g^{(k)}=\operatorname{diag}(1,-a_k^2,-c_k^2,-c_k^2),\quad
 a_k=P(H+B+v_k),\quad c_k=\frac{2Pw_k}{1+w_k^2(x^2+y^2)},
\]

where \(k=0,1\), \(w_0=1\), \(v_0=0\), \(w_1=e^z\), and
\[
q=e^{2z}(x^2+y^2),\quad v_1=\frac{1-q}{1+q}.
\]

The common positive regular domain is
\[
\mathcal U=\{1<t<2,\;-1/4<z<1/4,\;x^2+y^2<1/4\}.
\]
Here \(H>1\), \(P>0\), \(B>0\), \(q<1\), and \(v_1>0\).

## 2. Metric-first differentiation and SO(2) reduction

The verifier first derives \(\Gamma^a{}_{bc}\) and \(R_{ab}\) for a **generic** diagonal metric \(\mathrm{diag}(1,-a^2,-c^2,-c^2)\) with two unknown functions \(a(t,z,x,y)\), \(c(t,z,x,y)\), using

\[
\Gamma^a{}_{bc}=\tfrac12g^{ad}(\partial_bg_{dc}+\partial_cg_{db}-\partial_dg_{bc}),
\]
\[
R_{ab}=\partial_c\Gamma^c{}_{ab}-\partial_b\Gamma^c{}_{ac}
+\Gamma^c{}_{cd}\Gamma^d{}_{ab}-\Gamma^c{}_{bd}\Gamma^d{}_{ac}.
\]

Only after forming the complete Ricci tensor does it insert the two metric functions. The exact chain rules
\[
P_{,t}=PH,\quad P_{,z}=P(H+B),\quad
H_{,t}=H_{,z}=-\tfrac32(H^2-1),\quad B_{,z}=-3B^2,\quad w_{1,z}=w_1
\]
are independently checked against the explicit hyperbolic solution, along with \(P^3(H^2-1)=2M\). Mixed partials are verified to commute.

**Why restriction to \(y=0\) is exact:** the input metrics depend on \(x,y\) only through \(x^2+y^2\) and \(dx^2+dy^2\); rotations of the \((x,y)\)-plane are isometries. Derivatives in all four coordinates are taken *before* setting \(y=0\). Every point with \((x,y)\neq(0,0)\) is related to a point on the meridian by an isometry; the axis follows by continuity. Therefore tensor equations and scalar equalities established symbolically on the meridian hold throughout \(\mathcal U\). No assumption about the Einstein equations, matter density, or shear is used in this reduction.

## 3. Einstein–dust algebra from curvature alone

The program constructs \(G^a{}_b\), defines \(T^a{}_b=G^a{}_b-3\delta^a{}_b\), and takes \(R_\rho=\operatorname{tr}T\), **without importing the registered density formula**. Exact simplification yields
\[
T^a{}_b=\operatorname{diag}(R_\rho,0,0,0)
\]
for each metric, and separately verifies all 16 components of \(T^2-R_\rho T=0\), the rank-one projector, and its timelike unit image. The curvature-derived densities, expressed with \(F=H^2-1\), are
\[
R_{\rho,1}=\frac{3FB}{H+B},\qquad
R_{\rho,2}=\frac{3F(B+v_1)}{H+B+v_1}.
\]
They are strictly positive on \(\mathcal U\). Their difference, obtained **after** separately computing each Einstein tensor, is
\[
R_{\rho,2}-R_{\rho,1}=
\frac{3FHv_1}{(H+B)(H+B+v_1)}>0.
\]
The registered matter-density formulas match these independent curvature traces when checked *post hoc*.

## 4. Metric-derived shear, spectral polynomial, and \(\mathcal J\)

Using the timelike direction extracted from \(T/R_\rho\), the verifier constructs
\[
h^a{}_b=\delta^a{}_b-u^a u_b,\qquad
\sigma_{ab}=h_a{}^c h_b{}^d\nabla_{(c}u_{d)}-\frac{\Theta}{3}h_{ab},
\quad\Theta=\nabla_a u^a.
\]
The shear is calculated from the Levi-Civita connection derived above, not supplied as a known Szekeres expression. For \(L=H+B+v_k\), its spatial eigenvalues *emerge* as
\[
-\frac{F}{L},\quad \frac{F}{2L},\quad\frac{F}{2L}.
\]
Consequently
\[
I_2=\frac{3F^2}{2L^2},\quad I_3=-\frac{3F^3}{4L^3}.
\]
The code verifies exactly
\[
I_2^3=6I_3^2,\quad
\sigma^2-\frac{I_3}{I_2}\sigma-\frac{I_2}{3}h=0.
\]
It then constructs \(P_\perp{}^a{}_b=\tfrac23h^a{}_b-\frac{I_2}{3I_3}\sigma^a{}_b\) and verifies idempotence, trace two, and orthogonality to \(u^a\). Only now is the density-gradient scalar formed:
\[
\mathcal J=-P_\perp^{ab}\partial_aR_\rho\partial_bR_\rho.
\]
For \(S_1\), \(\mathcal J_1\equiv0\). For \(S_2\), the curvature-first calculation gives
\[
\boxed{\mathcal J_2=\frac{36H^2F^2q}{P^2L^4(1+q)^2}}.
\]
Using the independently checked first integral \(F=2M/P^3\), this equals
\[
\boxed{\mathcal J_2=\frac{144M^2H^2q}{P^8L^4(1+q)^2}>0\quad\text{for }q>0.}
\]
These identities establish a diffeomorphism-invariant obstruction because positive density reconstructs the unique dust eigendirection of the Einstein tensor, and the nonzero shear uniquely determines the repeated eigenspace. The zero set of \(\mathcal J\) is preserved by any diffeomorphism identifying Einstein–dust solutions.

## 5. Separate exact Euclidean embedding certificate

Independently of the curvature calculation, let
\[
\mathbf n=\frac{(2w_kx,2w_ky,1-q_k)}{1+q_k},\qquad
\mathbf X=P\mathbf n+k\mathbf e_3\int^z P(t,s)\,ds.
\]
For both sectors, exact full-\((x,y)\) symbolic identities verify \(\mathbf n^2=1\),
\(\partial_z\mathbf n=k(n_3\mathbf n-\mathbf e_3)\),
\(\mathbf n\cdot\partial_A\mathbf n=0\),
\(\partial_A\mathbf n\cdot\partial_B\mathbf n=(c_k/P)^2\delta_{AB}\), and every coefficient of the induced three-metric:
\[
\partial_i\mathbf X\cdot\partial_j\mathbf X=
\operatorname{diag}(a_k^2,c_k^2,c_k^2)_{ij}.
\]
This is a second, independent mathematical route to the flatness of each spatial slice; it is **not** used in the metric-first Ricci calculation.

## 6. Computational provenance and scope

- Interpreter: Python 3, package: SymPy 1.14.0.
- Entry point: `python m1_inh_e1b_metric_first_audit.py`.
- Every assertion is an exact symbolic-zero identity; no numerical tolerance is used.
- The produced JSON record includes the SHA-256 hash of the executed script.
- During development an embedding test initially compared the Gram matrix with \(E^2\) rather than the correct \(E^{-2}\); this **test expectation** was corrected, and the complete final certificate was rerun successfully. The Einstein-tensor calculation was unaffected.
- This is an independently authored implementation of the mathematical calculation, **not** independent external peer review.
- No registry or support flags have been modified.
- The complete frozen elliptic record agrees because both solutions use the same \(M,K,f,\Lambda,\epsilon,v_0,\sigma\) and derived \(g_2,g_3,\Delta_\wp\), with a common expanding branch on \(J\subset(-1,\infty)\).
- **General M1-INH-E1a remains pending:** deriving the *general* Szekeres–Szafron evolution and density equations from the unreduced Einstein system and then checking the Weierstrass transformation, rather than verifying this fixed special pair, is a distinct obligation.

**Conclusion:** The specified class-relative E1b constructive pair has a passing independent metric-first symbolic computation and an exact invariant inequivalence argument. Formal registry promotion awaits the registered general E1a predecessor and external/maintainer review of the proof certificate.