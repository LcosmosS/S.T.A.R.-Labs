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
./run_all.sh
# Or choose a unique, not-yet-existing output directory:
python reproduce.py --mesh --backend auto --h 0.8 0.5 0.3 0.2 --out-dir runs/manual-$(date -u +%Y%m%dT%H%M%SZ)
```

Or on macOS/Linux, run `./run_all.sh`.

### Gmsh and GUDHI

The original requested toolchain includes Gmsh geometry meshing and GUDHI simplicial homology. They are optional runtime dependencies here because the current execution environment had neither installed and could not reach the package index to install them. Install them on a machine where package installation is available:

```bash
python -m pip install -r requirements-gmsh.txt
```

Then run:

```bash
python reproduce.py --mesh --backend gmsh --h 0.8 0.5 0.3 0.2 --out-dir runs/gmsh-$(date -u +%Y%m%dT%H%M%SZ)
```

An explicit `--backend gmsh` request is fail-closed: an unavailable Gmsh/GUDHI gate produces a nonzero exit code even if fallback fixture checks pass. `--backend auto` may use fallback meshes but records the blocked gate; `--backend fallback` reports Gmsh as `NOT_REQUESTED`. Existing output directories are refused, and every completed run includes `run_receipt.json` with output hashes, source hash, environment, parameters, and gate status. It does not silently report the fallback as a Gmsh run. If GUDHI is unavailable, the pipeline calculates Betti numbers with an independently written GF(2) boundary-rank routine; output identifies which method was used.

The fallback run is useful and executable: it checks periodic torus cochains, face-wise curvature integrals, sphere-flux convergence, chain-complex identities, and the homology of triangulated sphere, torus, and solid-ball models. It is not a substitute for an actual Gmsh/GUDHI execution when the review protocol specifically requires those libraries.

## Current execution status

Three separate records are preserved: (1) the 16:06:23Z historical fallback bytes at `results/reproduction_results_gmsh_missing.json`, which match the hash and size of the original manifest entry named `results/reproduction_results.json`; (2) the distinct 16:27:49Z fallback report at `results/reproduction_results.json`, with 92/92 checks but Gmsh/GUDHI blocked; and (3) the 16:32:37Z Gmsh/GUDHI report under `results_gmsh/`, with 92/92 checks and both toolchain gates PASS. The third run does not retroactively satisfy the historical manifest. Dated manifests created by this patch are retrospective artifact inventories, not contemporaneous run-time receipts. The eight supplemental unit tests also pass. See `results/reproduction_results.json` and `results/mesh_details.json` for the details; do not paraphrase this as a complete Gmsh/GUDHI run.

After making changes or re-running, refresh hashes:

```bash
python freeze_manifest.py --out implementation_manifest_review_snapshot.json
```

`implementation_manifest.json` is an immutable historical snapshot. The freezer refuses to replace an existing manifest; provide a new timestamped path for each snapshot. `requirements-fallback-20261017T1606.txt` and `requirements-fallback-20261017T1627.txt` record the known core package versions for those fallback runs; the 16:06 and 16:27 reports did not record mpmath, so those are not complete transitive locks. `requirements-gmsh.txt` is the exact toolchain list from `results_gmsh/pip-freeze.txt`. For a two-investigator blinded protocol, each person should freeze and share their own manifest only after agreeing in advance on formulas, orientations, tolerances, and pass/fail criteria.

## Conventions

Angles have period \(2\pi\). The torus is oriented by \(d\phi\wedge d\psi\); the sphere uses outward orientation. The flat torus Hodge star satisfies \(*d\phi=d\psi\), \(*d\psi=-d\phi\). Curvature flux for Candidate B is normalized as \(Q=(2\pi)^{-1}\int_{S^2}F\).
