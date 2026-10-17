# EXP-ECC-B01 — Full Independent Mathematical Reproduction Kit

**Purpose.** Independently derive and test the mathematical fixtures in the Investigator-B handoff: (A) a closed, non-exact 1-form on a torus; (B) a patchwise U(1) connection and integer-normalized curvature flux on a sphere; and (C) an entropy-coupled closed 2-form on a torus. This is a mathematical-control package, not evidence for a physical, cosmological, arithmetic, or new-theorem claim.

The implementation and tests in this directory were authored independently. The starter script and its saved JSON were not imported, executed, or used as measured results. The original handoff was used only to identify the requested definitions, conventions, test requirements, and target outcomes.

## What is included

- `partner_proof_notes.md` — first-principles derivations, signs/orientations, exact results, and logical implications.
- `reproduce.py` — symbolic, quadrature, oriented-chain/cochain, topology, sphere-flux, and torus face-integration pipeline.
- `tests/test_independent_reproduction.py` — separately invoked unit tests for the identities and numerical invariants.
- `results/reproduction_results.json` — machine-readable output, dependency report, test outcomes, tolerances, and limitations.
- `results/convergence_b.csv` — per-resolution measured values, expected values, absolute errors, element counts, and observed convergence rates where meaningful.
- `results/mesh_details.json` — per-mesh topology, Betti numbers, incidence identities, flux estimates, and mesh-source metadata.
- `claim_boundary.md` — exactly what these controls do and do not support.
- `reproduction_protocol.md` — execution protocol and frozen numerical tolerances.
- `implementation_manifest.json` — SHA-256 hashes of code, documentation, and outputs in this package (excluding the manifest file itself).

## Reproduce

Python 3.11 or 3.12 is recommended; newer compatible versions may also work. In a new virtual environment:

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the complete available pipeline and unit tests:

```bash
python reproduce.py --mesh --backend auto --h 0.8 0.5 0.3 0.2 --out-dir results
python -m unittest discover -s tests -v
```

Or on macOS/Linux, run `./run_all.sh`.

### Gmsh and GUDHI

The original requested toolchain includes Gmsh geometry meshing and GUDHI simplicial homology. They are optional runtime dependencies here because the current execution environment had neither installed and could not reach the package index to install them. Install them on a machine where package installation is available:

```bash
python -m pip install -r requirements-optional.txt
```

Then run:

```bash
python reproduce.py --mesh --backend gmsh --h 0.8 0.5 0.3 0.2 --out-dir results
```

The runner uses Gmsh if it imports successfully. If Gmsh is missing or fails to initialize, the output records that the **Gmsh-specific gate is blocked** and runs independently generated fallback meshes instead. It does not silently report the fallback as a Gmsh run. If GUDHI is unavailable, the pipeline calculates Betti numbers with an independently written GF(2) boundary-rank routine; output identifies which method was used.

The fallback run is useful and executable: it checks periodic torus cochains, face-wise curvature integrals, sphere-flux convergence, chain-complex identities, and the homology of triangulated sphere, torus, and solid-ball models. It is not a substitute for an actual Gmsh/GUDHI execution when the review protocol specifically requires those libraries.

## Current execution status

The packaged results were generated with `--mesh --backend auto --h 0.8 0.5 0.3 0.2` and the separate unit-test suite. The recorded run reports **92 passed checks and 0 failed checks** across analytic, quadrature, discrete-mesh, and topology checks. The overall state is `PASS_CORE_AND_AVAILABLE_MESH; GMSH_GUDHI_GATE_BLOCKED`, because Gmsh/GUDHI were not available in this environment. The eight supplemental unit tests also pass. See `results/reproduction_results.json` and `results/mesh_details.json` for the details; do not paraphrase this as a complete Gmsh/GUDHI run.

After making changes or re-running, refresh hashes:

```bash
python freeze_manifest.py
```

`implementation_manifest.json` excludes its own hash to avoid a self-referential digest. For a two-investigator blinded protocol, each person should freeze and share their own manifest only after agreeing in advance on formulas, orientations, tolerances, and pass/fail criteria.

## Conventions

Angles have period \(2\pi\). The torus is oriented by \(d\phi\wedge d\psi\); the sphere uses outward orientation. The flat torus Hodge star satisfies \(*d\phi=d\psi\), \(*d\psi=-d\phi\). Curvature flux for Candidate B is normalized as \(Q=(2\pi)^{-1}\int_{S^2}F\).
