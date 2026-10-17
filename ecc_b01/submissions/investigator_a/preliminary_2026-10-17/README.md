# Investigator A — preliminary WSL fixture submission

**Experiment:** `REPO-CSV-v0.2:EXP-ECC-B01` (planned; not activated)  
**Evidence class:** preliminary symbolic/numerical smoke test — **not** blinded comparison, controlled mathematical verification, or physical evidence.  
**Execution date:** reported from user's WSL run on 2026-10-17; no trusted execution timestamp embedded in JSON.  
**Submission:** `results.json` was uploaded by Investigator A and committed without altering its contents.

## Integrity

- **Results SHA-256 (original uploaded bytes):** `e5ac9a776caafd527c90508b9d164e372fad8ffde0ba59189dbb320ea5a06673`
- **Reported source SHA-256:** `68108885ff5349f53d4b692a6d3b1937cae7924e0c7954584794b5bd70b031f2`
- **Source:** `ecc_b01/investigator_a.py` in this draft branch; script hash corresponds to the original Investigator A kit.
- **Result:** reported `PASS`, 15 of 15 fixtures with `pass_=true`. This is the program's result, not independent formal verification.
- **Reported execution environment:** WSL2 Linux, Python 3.12.13 (conda-forge), SymPy 1.14.0, NumPy 1.26.4, SciPy 1.17.1.

## Scope limitations and known defect

- Symbolic controls and two independent numerical quadratures only; no Gmsh/GUDHI mesh-cochain test, four-resolution convergence, independent Investigator B implementation, or downstream entropy/cosmology inference.
- Fixture **C-03** checks the expected symbolic residual value but calls `record(..., True, ...)` unconditionally. This can report PASS even if a future change invalidates the residual. Repair the assertion in a **subsequent versioned script**; do not rewrite this original provenance record.
- `results.json` has no run ID, locked environment digest, or external signature. It therefore serves as a reproducible *preliminary report*, not a complete cryptographically attested execution bundle.
- This GitHub PR is visible to other collaborators. Therefore the raw Investigator A results are **not blinded from someone who opens this path**. Investigator B must commit their own independent implementation and output before comparison, without examining this submission.
- Do not use 15/15 PASS as an inference that the ECC foundational revision is selected or validated.

## Hold conditions

PR #103 stays **draft/unmerged**. `EXP-ECC-B01` remains planned; no support/activation flags change. The controlled foundation comparison requires a signed/frozen protocol, corrected smoke-test assertion, independent B results, cochain/mesh convergence, and discrepancy adjudication.
