# Claim Boundary — EXP-ECC-B01

## Supported by this kit if the recorded tests pass

- The displayed Candidate-A 1-form has zero exterior derivative under the stated coordinate convention.
- Its integrals over the two chosen generating cycles are \(2\pi\) and \(4\pi\); therefore it is not globally exact.
- The displayed example \(\sin\phi\,d\psi\) is not closed.
- The specified north/south connection potentials have matching local curvature \((n/2)\sin\theta\,d\theta\wedge d\varphi\).
- The normalized sphere curvature integral is \(n\); the stated transition phase is single-valued precisely for integer \(n\).
- The Candidate-C density is \(q-\cos\phi-2\sin\psi\), and its total flux over the torus is \(4\pi^2 q\).
- In this example, adding a constant to \(S\) leaves the curvature unchanged; scaling \(S\) scales its local perturbation while its integrated contribution remains zero.
- At \((0,0)\), the local perturbation is \(-1\). At \(q=0\), total flux is zero although the local 2-form need not vanish.
- The supplied 3D form \(z\,dx\wedge dy\) is not closed.
- The checked mesh chain complexes satisfy the listed boundary-squared identities and expected Betti numbers for the specific triangulated models.
- The independent centroid quadrature error for the monopole-like sphere flux decreases across the tested mesh refinements in the recorded run.

## Not supported by this kit

- No laboratory, observational, biological, cosmological, or other physical prediction is tested.
- No empirical relation between curvature/entropy and physical charge is established.
- No arithmetic correspondence, prime-number formula, or new ECC theorem is proved.
- A successful mesh topology test does not prove a differential form is non-exact; Candidate A's non-exactness follows from its analytically derived nonzero periods.
- A closed form is not necessarily exact. A zero total flux does not imply zero local curvature. A test on one specified form is not a theorem about all forms.
- If the output says `GMSH_GUDHI_GATE_BLOCKED`, this is **not** a completed Gmsh execution. An independently generated fallback mesh does not remove that limitation.
- If GUDHI is absent, the Python GF(2) homology fallback is a separately written computation, not a GUDHI run.

## Exact interpretation of the current packaged run

The recorded run passes its analytic, quadrature, fallback mesh, incidence, topology, and convergence checks. Its overall state remains `PASS_CORE_AND_AVAILABLE_MESH; GMSH_GUDHI_GATE_BLOCKED` because Gmsh/GUDHI could not be installed in the current environment. A downstream review requiring those exact tools should rerun with the optional dependencies and retain the new outputs and hashes.
