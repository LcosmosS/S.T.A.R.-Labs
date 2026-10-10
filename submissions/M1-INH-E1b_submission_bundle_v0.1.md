# M1-INH-E1b — submission bundle and independent verification invitation

**Status (2026-10-09):** Candidate **class-relative mathematical insufficiency theorem**, supported by an exact symbolic certificate; **external independent proof review pending**. This document is an external invitation, **not** acceptance of the theorem or a change to any canonical evidence/eligibility gate. The governing authority remains the [STAR Research Charter v0.2 PDF](../charter/STAR_Research_Charter_v0-2.pdf) and the [frozen M1-INH-E1 protocol](../preregistrations/M1-INH-E1/protocol.md).

## Precisely claimed theorem (M1-INH-E1b)

Within the **registered nondegenerate, $\beta_{,z}\ne0$ Szekeres–Szafron irrotational dust + $\Lambda$ class**, the **complete frozen elliptic-evolution record**
\[
\mathfrak E[S]|_J=(M,K,f,\Lambda,\epsilon,v_0,\sigma;\,g_2,g_3,\Delta_{\wp})|_J
\]
**does not determine the full dust inhomogeneity up to diffeomorphism**. The two explicit regular positive-density Einstein–dust solutions below have **identical $\mathfrak E$ component by component**, with the same inverse-Weierstrass representatives and time normalization, but are not related by a diffeomorphism of Einstein–dust solutions: their *curvature-defined* scalar $\mathcal J$ vanishes identically for the first and is positive on an open subset of the second. This is an **existence/insufficiency** claim for this registered class and record, **not** a universal no-go theorem.

## Exact domain, metrics, signs and elliptic branch

Coordinates $(t,z,x,y)$, signature $(+---)$, future dust flow $u=\partial_t$, convention
\[
G_{ab}-\Lambda g_{ab}=\kappa\widetilde\rho\,u_a u_b,\quad \Lambda=3,\quad
\mathcal U=\{1<t<2,\ -\tfrac14<z<\tfrac14,\ x^2+y^2<\tfrac14\},\quad J=(-\tfrac14,\tfrac14).
\]
Set $M=1+z$, $K=0$, $f=z$, $P=\Phi=[2(1+z)]^{1/3}\sinh^{2/3}(\tfrac32(t+z))$,
$H=\coth(\tfrac32(t+z))$, $B=[3(1+z)]^{-1}$, $F=H^2-1$ and $q=e^{2z}(x^2+y^2)$. For $k=0,1$, define
\[
g^{(k)}=\mathrm{diag}(1,-a_k^2,-c_k^2,-c_k^2),\quad
a_k=P(H+B+d_k),\quad c_k=\frac{2Pw_k}{1+w_k^2(x^2+y^2)},
\]
with $(w_0,d_0)=(1,0)$ and $(w_1,d_1)=(e^z,(1-q)/(1+q))$. The elliptic-blind sectors correspond to $A=C=\tfrac12$ and $(A,C)=(e^z/2,e^{-z}/2)$, respectively, with $B_1=B_2=0$ and $h=1$; each satisfies the registered spatial constraint. On $\mathcal U$, $P,B,F,H>0$, $q<1$, $a_k,c_k>0$, and the curvature-derived quantities are
\[
R_k:=\operatorname{tr}(G^{(k)a}{}_b-3\delta^a_b)=\kappa\widetilde\rho_k,\quad
R_0=\frac{3FB}{H+B}>0,\quad R_1=\frac{3F(B+d_1)}{H+B+d_1}>0.
\]

The **identical** frozen Weierstrass data are $g_2=0$, $g_3=-M^2/4$, $\Delta_\wp=-27M^4/16\ne0$, $\epsilon=0$, and the **same expanding real branch** $\dot P>0$, $\wp'(u)<0$, with positive-real inverse and period indices $(0,0)$:
\[
\xi=\frac{M}{2P},\quad
u(t,z)=\int_{\xi}^{\infty}\frac{d\eta}{\sqrt{4\eta^3+M^2/4}},\quad
v_0(z)=\int_0^\infty\frac{d\eta}{\sqrt{4\eta^3+M^2/4}},\quad
0<u<v_0,\quad t+z=\int_0^u P(u',z)\,du'.
\]
These choices fix $\sigma$ (common connected interval, expansion sign and inverse/lattice representatives); they are **not** inferred solely from equality of $(g_2,g_3,\Delta_\wp)$.

## Intrinsic distinguishing certificate

For $R=\kappa\widetilde\rho>0$, the rank-one tensor $G^a{}_b-3\delta^a_b$ uniquely determines the timelike dust eigendirection up to time orientation. Its nonzero shear $\sigma^a{}_b$ determines the repeated-eigenvalue two-plane via $h^a{}_b=\delta^a_b-u^a u_b$, $I_j=\operatorname{tr}(\sigma^j)$, and
$P_\perp{}^a{}_b=\tfrac23 h^a{}_b-\tfrac{I_2}{3I_3}\sigma^a{}_b$. Hence $\mathcal J=-P_\perp^{ab}\nabla_aR\nabla_bR$ is a scalar invariant of the Einstein–dust solution. The claimed exact identities are
\[
\mathcal J[g^{(0)}]\equiv0,\qquad
\mathcal J[g^{(1)}]=\frac{36H^2F^2q}{P^2(H+B+d_1)^4(1+q)^2}>0
\quad\text{on }\mathcal U\cap\{x^2+y^2>0\}.
\]
Thus no open set in the second solution can be diffeomorphic (as an Einstein–dust solution) to an open set in the first on which $\mathcal J$ is identically zero.

## Canonical verifier identity and replication

**Canonical source:** [m1_inh_e1b_metric_first_audit_v4.py](../preregistrations/M1-INH-E1/evidence/metric-first/m1_inh_e1b_metric_first_audit_v4.py) (Python 3; **SymPy 1.14.0**). **Expected exact file SHA-256:**  
`10ccfa264f475fd7bd6d490c80c8862a174730567ee51c0d759b87939b93e6bb`.

Run in a *disposable checkout* (the verifier writes a JSON certificate beside itself): `sha256sum preregistrations/M1-INH-E1/evidence/metric-first/m1_inh_e1b_metric_first_audit_v4.py`; then `python preregistrations/M1-INH-E1/evidence/metric-first/m1_inh_e1b_metric_first_audit_v4.py` after installing `sympy==1.14.0`. Compare the new output against the [preserved proof record](../preregistrations/M1-INH-E1/evidence/metric-first/M1-INH-E1b_metric_first_proof_record.md) and [certificate](../preregistrations/M1-INH-E1/evidence/metric-first/m1_inh_e1b_metric_first_audit_v4.json); do **not** call a rerun of the same code independent implementation.

**Explicit non-claims:** This is **not** the general **M1-INH-E1a** Einstein-to-Weierstrass derivation or its independent acceptance; **not** a **M1-INH-E1c** test of sufficiency for any selected observable; **not** a terminal **P0-T001** failure or exhaustion of the five-parent P0 search frame; and **not** physical ACSC support, proof of BSD, a cosmological correspondence, or authorization to execute an experiment.

**Invitation:** Independent researchers are invited to **re-implement from the two metric tensors**, in another symbolic tensor system or an independently authored differential-geometric derivation, and check: the complete Einstein tensor and sign convention; positive-density regularity on $\mathcal U$; the full *frozen* branch record; dust/shear spectral uniqueness; and the $\mathcal J$ identities, including possible counterexamples. Please publish source/derivation, environment, exact source hashes, failed as well as successful checks, and an explicit scoped verdict. Criticism and falsification are equally welcome. **Any change to the repository's independent-review/registry gates requires its existing separate approval process; distribution in a tagged release does not satisfy or bypass that process.**
