# M1-INH-E1a — general Einstein-to-Weierstrass reduction

**Scientific status:** Exact general-class derivation and locally executed symbolic identities, **submitted for review**, not independently peer-reviewed. This record **does not** modify or supersede [the frozen M1-INH-E1 protocol](../protocol.md). The [S.T.A.R. Research Charter v0.2 (governing PDF)](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/main/charter/STAR_Research_Charter_v0-2.pdf) controls interpretation; its [v0.2 Markdown companion](../../../charter/RESEARCH_CHARTER_v0.2.md) separates analytic results from controlled empirical evidence.

**Source convention:** Kraniotis–Whitehouse, *General Relativity, the Cosmological Constant and Modular Forms* (2002), [arXiv:gr-qc/0105022](https://arxiv.org/abs/gr-qc/0105022). The derivation below starts with the registered metric and directly evaluates its Einstein equations, rather than assuming the frozen evolution or density formulas. Signature +---, \(\kappa=8\pi G\), and **frozen sign convention** \(G_{ab}-\Lambda g_{ab}=\kappa\widetilde\rho\,u_a u_b\).

## 1. Frozen geometric input; regularity

Use coordinates \((t,z,x,y)\) and the **already registered** class-I ansatz, with dust flow \(u^a=(\partial_t)^a\):

\[
ds^2=dt^2-a^2 dz^2-c^2(dx^2+dy^2),\quad
a=h(z)D,\quad c=\Phi/E,\quad
D=\Phi_{,z}-\Phi E_{,z}/E.
\]

Write \(E=e^{-\nu}=A(z)(x^2+y^2)+2B_1(z)x+2B_2(z)y+C(z)\). Define

\[
\chi=4(AC-B_1^2-B_2^2),\quad
\chi=h^{-2}+K,\quad
\nu_{,z}=-E_{,z}/E,\quad D=\Phi_{,z}+\Phi\nu_{,z}.
\]

These are input *metric and constraint* data frozen by the protocol, **not** newly deduced from an unrestricted metric ansatz. The field-equation reduction is now derived without assuming either the evolution or density formula.

Work on a connected smooth branch with \(\Phi>0,E>0,h\ne0,D\ne0\), and differentiable radial free functions; \(a^2>0,c^2>0\). Here \(\beta_{,z}=D/\Phi\ne0\), excluding the other Szafron branch and shell crossings. Positivity of the *general* matter density is **not automatic** and must be imposed separately for physical dust solutions.

Two direct polynomial consequences are

\[
 E_x^2+E_y^2-E(E_{xx}+E_{yy})=-\chi,
\]
\[
2(E_xE_{xz}+E_yE_{yz})
-E_z(E_{xx}+E_{yy})-E(E_{xxz}+E_{yyz})=-\chi_{,z}.
\]

No axisymmetry is assumed: all four \(A,B_1,B_2,C\) remain arbitrary functions subject only to their registered constraint.

## 2. Longitudinal Einstein equation and exact time integration

Compute the Levi-Civita connection and Ricci tensor of the *generic* diagonal four-metric with arbitrary \(a(t,z,x,y)\) and \(c(t,z,x,y)\). The resulting mixed longitudinal Einstein component is

\[
G^z{}_z=
2\frac{c_{,tt}}c+\left(\frac{c_{,t}}c\right)^2
-\frac{c_{,xx}+c_{,yy}}{c^3}
+\frac{c_{,x}^2+c_{,y}^2}{c^4}
-\frac{c_{,z}^2}{a^2c^2}.
\tag{1}
\]

The accompanying exact symbolic certificate reconstructs this expression from Christoffel symbols, with no radial evolution equation supplied to the curvature calculation.

For \(c=\Phi/E\), the quadratic identity gives

\[
-\frac{c_{,xx}+c_{,yy}}{c^3}
+\frac{c_{,x}^2+c_{,y}^2}{c^4}=\frac{\chi}{\Phi^2}.
\]

Also \(c_{,z}=D/E\), hence \(c_{,z}/(ac)=1/(h\Phi)\). Equation (1) therefore becomes

\[
G^z{}_z=\frac{2\Phi\ddot\Phi+\dot\Phi^2+\chi-h^{-2}}{\Phi^2}
=\frac{2\Phi\ddot\Phi+\dot\Phi^2+K}{\Phi^2}.
\]

For pressureless comoving matter, \(G^z{}_z=\Lambda\), so

\[
2\Phi\ddot\Phi+\dot\Phi^2+K-\Lambda\Phi^2=0.
\tag{2}
\]

Multiply (2) by \(\dot\Phi\). At fixed \(z\),

\[
\partial_t\bigl(\Phi\dot\Phi^2+K\Phi-\tfrac{\Lambda}{3}\Phi^3\bigr)=0.
\]

The integration constant is an arbitrary radial function, denoted **\(2M(z)\)**. Consequently the *general registered* evolution law is

\[
\boxed{\dot\Phi^2=-K(z)+\frac{2M(z)}{\Phi}+\frac{\Lambda}{3}\Phi^2.}
\tag{3}
\]

The equation also extends through isolated turning points by continuity; the integration step does not divide by \(\dot\Phi\).

## 3. Hamiltonian Einstein equation and spatially dependent density

Let \(\gamma_{ij}=\operatorname{diag}(a^2,c^2,c^2)\) be the induced spatial metric. Computing its Ricci scalar using the same metric data gives the **generic** result

\[
{}^{(3)}R=-2\left[
\frac{c_{xx}+c_{yy}}{c^3}-\frac{c_x^2+c_y^2}{c^4}
+\frac{a_{xx}+a_{yy}}{ac^2}
+\frac{2}{ac}\partial_z\!\left(\frac{c_z}{a}\right)
+\frac{c_z^2}{a^2c^2}\right].
\tag{4}
\]

With the two polynomial identities from §1 and the constraint \(\chi=h^{-2}+K\), individual terms simplify as follows:

\[
\frac{c_{xx}+c_{yy}}{c^3}-\frac{c_x^2+c_y^2}{c^4}
=-\frac{\chi}{\Phi^2},
\]
\[
\frac{a_{xx}+a_{yy}}{ac^2}
=-\frac{\chi_z-2\chi E_z/E}{\Phi D},\quad
\frac{2}{ac}\partial_z\!\left(\frac{c_z}a\right)
=-\frac{2(h_z/h+E_z/E)}{h^2\Phi D},\quad
\frac{c_z^2}{a^2c^2}=\frac1{h^2\Phi^2}.
\]

Using \(\chi_z=K_z-2h_z/h^3\), all dependence on \(h_z\) cancels, yielding

\[
\boxed{{}^{(3)}R=
\frac{2K}{\Phi^2}
+\frac{2(K_z+2K\nu_z)}{\Phi D}.}
\tag{5}
\]

The two principal expansion rates are \(H_\perp=\dot\Phi/\Phi\) and \(H_\parallel=\dot D/D\). A direct generic four-dimensional calculation yields the Hamiltonian identity

\[
G^t{}_t=\tfrac12{}^{(3)}R+H_\perp^2+2H_\perp H_\parallel.
\tag{6}
\]

Differentiate (3) radially, **without setting any spatial free function constant**:

\[
2\dot\Phi\,\dot\Phi_{,z}
=-K_z+\frac{2M_z}{\Phi}
-\frac{2M\Phi_z}{\Phi^2}
+\frac{2\Lambda}{3}\Phi\Phi_z.
\tag{7}
\]

Substitute (3), (5), (7), and \(\dot D=\dot\Phi_z+\dot\Phi\,\nu_z\) into (6). Terms involving \(K,K_z\) cancel, and \(\Lambda\) separates as

\[
G^t{}_t=\Lambda+
\frac{2M_z+6M\nu_z}{\Phi^2 D}.
\]

Since \(G^t{}_t-\Lambda=\kappa\widetilde\rho\) for comoving dust,

\[
\boxed{\kappa\widetilde\rho=
\frac{2M_{,z}+6M\nu_{,z}}
{\Phi^2(\Phi_{,z}+\Phi\nu_{,z})}.}
\tag{8}
\]

This is an Einstein-equation consequence, not an imposed density formula. The explicit appearance of \(\nu_z\) establishes why the spatial functions \(A,B_1,B_2,C,h\) are not reconstructed by the radial elliptic record.

### Remaining Einstein components

The above reduction is not merely a two-equation ansatz: the mixed off-diagonal Ricci terms vanish using \(c_t/c=\dot\Phi/\Phi\), \(c_z=D/E\), \(a=hD\), \(E_{xy}=E_{zxy}=0\), and the quadratic identities. For example,

\[
R_{tz}=\frac{2(-a c_{tz}+a_t c_z)}{ac}=0,\qquad
R_{zx}= \frac{-ac c_{zx}+a c_xc_z+c a_xc_z}{ac^2}=0.
\]

The \(x/y\) analogues vanish; \(R_{xy}=0\) follows from \(E_{xy}=E_{zxy}=0\). Moreover \(G^x{}_x=G^y{}_y\) follows from \(E_{xx}=E_{yy}\) and \(E_{zxx}=E_{zyy}\). Denote the common remaining diagonal residual by \(p_\perp=G^x{}_x-\Lambda=G^y{}_y-\Lambda\). The contracted Bianchi identity in the radial direction, after \(G^z{}_z-\Lambda=0\), is

\[
0=\nabla_a(G^a{}_z-\Lambda\delta^a_z)
=-2(c_z/c)\,p_\perp.
\]

Since \(c_z/c=D/\Phi\ne0\), \(p_\perp=0\). Thus all Einstein–dust components close on the stated regular branch; no transverse field equation is silently discarded. This closure argument does **not** derive the initially registered metric ansatz from a completely unrestricted spacetime metric.

## 4. Exact Weierstrass normal form, no BSD assumptions

At each fixed \(z\), define precisely the frozen variable

\[
X=-1/\Phi,\qquad
Q(X)=-2MX^3-KX^2+\Lambda/3.
\]

From (3), \((dX/dt)^2=X^2 Q(X)\). On a connected physical branch choose the sign of the square root consistently with \(dt/du=+\Phi\), and set

\[
du=\frac{dX}{\sqrt{Q(X)}}.
\]

Next apply the **frozen, not refitted** affine transform

\[
X=-\frac{\xi+K/12}{M/2},
\qquad\Longleftrightarrow\qquad
\xi=-\frac M2 X-\frac K{12}.
\]

Then

\[
\left(\frac{d\xi}{du}\right)^2
=\frac{M^2}{4}Q\!\left(-\frac{2}{M}(\xi+K/12)\right)
=4\xi^3-\frac{K^2}{12}\xi-
\left(\frac{K^3}{216}-\frac{\Lambda M^2}{12}\right).
\]

Hence the **unchanged registered** invariants are

\[
\boxed{g_2=\frac{K^2}{12},\quad
g_3=\frac{K^3}{216}-\frac{\Lambda M^2}{12},\quad
\Delta_\wp=g_2^3-27g_3^2
=\frac{\Lambda M^2}{48}(K^3-9\Lambda M^2).}
\]

The last factorization is a derived diagnostic, **not** a replacement for the frozen discriminant definition. On a nondegenerate interval \(\Delta_\wp\ne0\) (which also forces \(M\ne0\)), a locally chosen inverse yields

\[
\xi(u,z)=\wp(u+\epsilon;g_2(z),g_3(z)),\qquad
\boxed{\Phi(t,z)=\frac{M(z)/2}
{\wp(u+\epsilon;g_2,g_3)+K(z)/12}}.
\]

The frozen representative \(v_0(z)\) is chosen, where appropriate over the elliptic curve, by \(\wp(v_0)=-K/12\), modulo its period lattice. The continuous physical branch and the discrete sign/period choices \(\sigma(z)\) remain explicitly part of the registered record; no branch is changed post hoc. With the signed \(u\) orientation specified above,

\[
\frac{dt}{du}=\Phi,\qquad
\boxed{t+f(z)=\int\Phi\,du}
\]

(up to the corresponding choice of primitive). On a collapsing branch reverse the sign of the \(u\)-differential when necessary to maintain the registered time convention. No globally single-valued Weierstrass inverse is asserted.

## 5. Verification, scope and governance

Execute \`e1a_general_einstein_reduction.py\` in this directory with SymPy. It independently derives the **generic 4D** Hamiltonian and longitudinal Einstein identities from Levi-Civita curvature and symbolically checks the two general transverse \(E\)-polynomial identities, the frozen spatial curvature reduction, Hamiltonian density, Weierstrass affine transform, discriminant and \(X\)-time relation. The script does **not** use the special M1-INH-E1b pair. The off-diagonal/Bianchi closure is explicitly derived in §3 and remains a human-review obligation; it is not represented as an automated all-16-component generic tensor certificate.

**Derivation result:** General E1a reduction mathematically obtained and locally corroborated; **external independent review is pending**. There is no detected protocol-specification failure, and **the frozen protocol has not been altered**. This is theoretical verification of established Szekeres mathematics, not an observational test, not E1c, not a P0 candidate failure, and not ACSC physical support. The registries, historical audit, support flags and controlled execution eligibility remain unchanged.
