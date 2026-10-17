# Independent Proof Notes — EXP-ECC-B01

## Status and scope

These derivations independently establish the mathematical behavior of the three specified examples under the conventions below. They do not establish any empirical physics or cosmology, any arithmetic correspondence, or a new theorem beyond the stated differential-geometric facts.

## Conventions

The coordinates \(\phi,\psi,\varphi\) have period \(2\pi\). The orientation of \(T^2\) is \(d\phi\wedge d\psi\); the orientation of \(S^2\) is outward. The Hodge star on the flat oriented torus is defined by

\[
*d\phi=d\psi,\qquad *d\psi=-d\phi.
\]

For a 1-form \(\alpha=a\,d\phi+b\,d\psi\),

\[
d\alpha=(\partial_\phi b-\partial_\psi a)\,d\phi\wedge d\psi.
\]

The Candidate-B normalized curvature flux is \(Q=(2\pi)^{-1}\int_{S^2}F\).

## A. Closed but non-exact 1-form on \(T^2\)

Set

\[
S(\phi,\psi)=\cos\phi+2\sin\psi,
\qquad \eta=d\phi+2d\psi+dS.
\]

Direct differentiation gives

\[
dS=-\sin\phi\,d\phi+2\cos\psi\,d\psi,
\]

so

\[
\eta=(1-\sin\phi)\,d\phi+(2+2\cos\psi)\,d\psi.
\]

The coefficient of \(d\phi\wedge d\psi\) in \(d\eta\) is

\[
\partial_\phi(2+2\cos\psi)-\partial_\psi(1-\sin\phi)=0-0=0.
\]

Thus \(d\eta=0\). For the first positively oriented generating cycle, with \(\psi\) fixed,

\[
\oint_{\gamma_\phi}\eta=\int_0^{2\pi}(1-\sin\phi)\,d\phi=2\pi.
\]

For the second cycle, with \(\phi\) fixed,

\[
\oint_{\gamma_\psi}\eta=\int_0^{2\pi}(2+2\cos\psi)\,d\psi=4\pi.
\]

The \(dS\) part integrates to zero on either closed loop because it is the differential of a globally defined periodic scalar. If \(\eta=df\) for a globally defined function \(f:T^2\to\mathbb R\), then every closed-loop integral would equal \(\oint df=0\). Both displayed periods are nonzero, so \(\eta\) is **not exact**. This is the intended certificate: closedness plus a nonzero period, not merely a symbolic `d(eta)=0` result.

A counterexample demonstrates why a general 1-form need not be closed. For \(\alpha=\sin\phi\,d\psi\),

\[
d\alpha=\cos\phi\,d\phi\wedge d\psi,
\]

which is not identically zero.

### Discrete realization

On a periodic \(N\times N\) parameter grid, edge integrals of \(\eta\) are evaluated by the exact coordinate increment plus the endpoint difference of \(S\). Periodic displacements are unwrapped to their shortest signed angular increments. The sum around each oriented triangle tests the discrete cocycle condition; sums along the two wraparound coordinate loops test the periods. The same triangulation has integer incidence/coboundary matrices with \(D_1D_0=0\) exactly.

## B. Patchwise \(U(1)\) curvature and integer charge on \(S^2\)

On north/south coordinate patches, define

\[
A_N=\frac n2(1-\cos\theta)\,d\varphi,
\qquad
A_S=-\frac n2(1+\cos\theta)\,d\varphi.
\]

Differentiating their scalar coefficients with respect to \(\theta\) yields

\[
F_N=dA_N=\frac n2\sin\theta\,d\theta\wedge d\varphi,
\qquad
F_S=dA_S=\frac n2\sin\theta\,d\theta\wedge d\varphi.
\]

They agree on the overlap and define the same curvature 2-form. With outward orientation,

\[
\begin{aligned}
Q&=\frac1{2\pi}\int_0^{2\pi}\int_0^\pi
\frac n2\sin\theta\,d\theta\,d\varphi\\
&=\frac1{2\pi}\,\frac n2\,(2)(2\pi)=n.
\end{aligned}
\]

The patch difference is

\[
A_N-A_S=n\,d\varphi=d\chi,\qquad \chi=n\varphi.
\]

With transition phase \(g(\varphi)=e^{i\chi}=e^{in\varphi}\), single-valuedness around the overlap circle requires

\[
g(\varphi+2\pi)=g(\varphi)
\quad\Longleftrightarrow\quad e^{2\pi i n}=1
\quad\Longleftrightarrow\quad n\in\mathbb Z.
\]

For \(n=\tfrac12\), the phase changes by \(-1\), so it is not a well-defined transition map on that circle. The code checks charges \(-1,0,1,2\) and a half-integer separately.

### Independent flux integrations

The mesh study compares two methods on sphere triangulations:

1. **Spherical-triangle solid angle.** For unit vertices \(a,b,c\), the signed solid angle is
   \[
   \Omega(a,b,c)=2\operatorname{atan2}\!\left(a\cdot(b\times c),\,1+a\cdot b+b\cdot c+c\cdot a\right).
   \]
   Since \(F=(n/2)d\Omega\), the normalized charge is \(n\sum\Omega/(4\pi)\). The solid-angle formula integrates each spherical triangle rather than approximating its curved area by a flat patch.

2. **Flat-facet centroid quadrature.** The vector representative of the curvature is \(B(x)=(n/2)x/\lVert x\rVert^3\). Each planar triangular facet contributes the midpoint/centroid estimate \(B(x_c)\cdot\vec A\). This is a distinct approximation whose error should decrease with mesh refinement. The CSV reports its absolute error and observed rate rather than relying only on a passing tolerance.

The sphere model uses outward-oriented faces; the implementation independently corrects each triangle's orientation before either integration.

## C. Entropy-coupled closed 2-form on \(T^2\)

With the Hodge-star convention above and the same scalar \(S\),

\[
*dS=S_\phi\,d\psi-S_\psi\,d\phi
=-\sin\phi\,d\psi-2\cos\psi\,d\phi.
\]

Applying the 1-form exterior derivative rule gives

\[
\begin{aligned}
d(*dS)
&=\left[\partial_\phi(-\sin\phi)-\partial_\psi(-2\cos\psi)\right]d\phi\wedge d\psi\\
&=(-\cos\phi-2\sin\psi)\,d\phi\wedge d\psi.
\end{aligned}
\]

For

\[
F_S=q\,d\phi\wedge d\psi+d(*dS),
\]

the density is

\[
F_S=(q-\cos\phi-2\sin\psi)\,d\phi\wedge d\psi.
\]

The integrated flux is

\[
\begin{aligned}
\int_{T^2}F_S
&=q(2\pi)^2-\left(\int_0^{2\pi}\cos\phi\,d\phi\right)(2\pi)
-2(2\pi)\int_0^{2\pi}\sin\psi\,d\psi\\
&=4\pi^2q.
\end{aligned}
\]

Adding a constant to \(S\) does not change \(dS\), and scaling \(S\) scales the local perturbation linearly without changing its zero integral over the torus. At \((\phi,\psi)=(0,0)\), the local perturbation is

\[
-\cos(0)-2\sin(0)=-1,
\]

which is a deliberately chosen point with a nonzero response. For \(q=0\), total flux is zero but the local density at this point is \(-1\); zero flux does **not** mean \(F_S\equiv0\).

In two dimensions any 3-form vanishes, so every smooth 2-form is closed. This dimensional fact explains why Candidate C is closed locally; it should not be overstated as a separate discovery. In three dimensions the 2-form \(G=z\,dx\wedge dy\) is not closed:

\[
dG=dz\wedge dx\wedge dy=dx\wedge dy\wedge dz\ne0,
\]

where the last equality is a cyclic permutation of the factors.

### Mesh integration

Each parameter-space rectangle is split into two positively oriented triangles. The code integrates the specified trigonometric density analytically on each triangle, and separately estimates the same integral using the triangle barycentre. It records both total-flux errors and the maximum local-face quadrature error. Exact integration should preserve the flux at every resolution; centroid quadrature has local truncation error even when the periodic grid makes the global sinusoidal errors cancel particularly well.

## Topological/chain controls

For each simplicial complex, the oriented boundary operators are built from the ordered simplex faces. Their transposes define the cochain coboundaries \(D_0,D_1,D_2\). The implementation verifies integer-exact

\[
D_1D_0=0,\qquad D_2D_1=0
\]

where the dimensions exist. Betti numbers are computed by GUDHI when available; otherwise they are computed independently over \(\mathbb F_2\) from ranks of boundary matrices. Expected Betti vectors are \([1,0,1]\) for a sphere, \([1,2,1]\) for a torus, and \([1,0,0,0]\) for a solid ball. These topological checks describe the triangulated spaces; they do not establish that a particular differential form is nontrivial.
