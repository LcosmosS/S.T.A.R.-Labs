# ECC and RTCH mathematical/physical recovery gates

**Status:** proof-obligation design only. Registry statuses `EXP-ECC-B01` and `EXP-RTCH-B01` stay planned and all support/activation flags false.

## ECC — exact-form obstruction

For any globally defined smooth scalar \(\mathcal M\) on a smooth manifold \(X\),

\[
\theta=d\mathcal M \implies d\theta=d^2\mathcal M=0,\qquad [\theta]_{H^1_{\mathrm{dR}}(X)}=0.
\]

The second conclusion follows from **global exactness**; merely computing `dtheta=0` would prove closedness, **not** cohomological nontriviality. A torus cohomology `H¹ != 0` is a property of the *space*, not evidence that the proposed entropy 1-form is a nonzero class.

Candidate repairs are logically different theories and must be separately versioned: (a) a globally closed but non-exact 1-form with nonzero cycle periods `∮_gamma theta`; (b) locally defined potentials related by nontrivial transition cocycles, with gluing/holonomy proved; (c) a higher-degree closed curvature `F` with a global characteristic class, not merely `d(dM)`. None can be imported into the existing conjecture as a silent fix. For `EXP-ECC-B01`, the **first** preregistration must select the cochain degree, domain, coefficient group, exactness criterion, fixed numerical discretization, positive/negative controls, noise null, and resolution-stability diagnostics. Forbidden: using random synthetic torus Betti numbers to claim cosmic entropy support or recycling target-derived ML features.

## RTCH — standard-physics recovery before fitting

Freeze a dimensional and variationally meaningful action `S[g,fluid,entropy-fields;epsilon]` and a designated decoupling parameter `epsilon` before data inspection. A successful recovery test must derive, at `epsilon=0` with the proposed additional fields held in a permitted regular reference configuration,

\[
G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G T^{\rm conventional}_{\mu\nu},
\qquad\nabla_\mu T^{\mu\nu}_{\rm conventional}=0,
\]

plus the corresponding ordinary energy conservation and thermodynamic first-law limit.

**Sign-convention gate:** This conventional \(G+\Lambda g=\kappa T\) display is schematic and must not silently replace the frozen M1-INH-E1 convention \(G-\Lambda g=\kappa T\). The same Riemann/Ricci and cosmological-constant signs must be derived consistently from the selected RTCH action; the reviewer must explicitly provide the dictionary before comparing formulas or interpreting numerical residuals. Derive the stress tensor from variation of the **same** action, check Bianchi compatibility, units, boundary terms, signs, weak-field and homogeneous limits, and numerical convergence as `epsilon→0`. Distinguish mathematical existence of the limit from numerical approximation error. Reject singular couplings, ill-posed scalar dynamics or hidden residual stress. No fitting of `epsilon` or new thermodynamic coefficients to Hubble data before this stage.

## Controlled protocol gates

Before changing `PAR-ECC-001/NULL-ECC-001` or `PAR-RTCH-001/NULL-RTCH-001`, obtain independent theory-review signatures on exact definitions, counterexamples, both positive and negative controls, convergence tolerances, frozen solver/environment, and primary decision logic. Software fixtures cannot substitute for physical data; recovery of standard physics is **necessary**, not sufficient, for a new physical modification.
