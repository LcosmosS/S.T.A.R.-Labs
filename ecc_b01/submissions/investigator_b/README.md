# Investigator B — Shaughn McNamara: preserved mathematical-reproduction evidence

**Experiment:** `EXP-ECC-B01` (mathematical foundation controls, draft/not activated)  
**Investigator B (reported):** Shaughn McNamara  
**PR:** [#103](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/103) — **DRAFT; UNMERGED**  
**Evidence classification:** submitted independent-implementation report and mathematical fixture executions; **not** approval of physical, arithmetic–cosmological, or new-theorem claims.

## Timestamped execution records

| Folder (UTC date/time) | Run environment and backend | Reported result | Preserved components |
|---|---|---|---|
| [`original_2026-10-17_1606UTC/`](original_2026-10-17_1606UTC/) | Python 3.13.5 on Linux; Gmsh and GUDHI **unavailable**; independent GF(2) fallback | 92 PASS, 0 FAIL; Gmsh/GUDHI toolchain gate **BLOCKED** | Original 14-file frozen manifest inventory, exact first-run JSON recovered after overwrite, original unmodified manifest, source, tests, protocol, proof notes, requirements, unit-test log, numerical data |
| [`fallback_2026-10-17_1627UTC/`](fallback_2026-10-17_1627UTC/) | Python 3.12.11 on WSL2; fallback mesh | 92 PASS, 0 FAIL; Gmsh/GUDHI gate **BLOCKED** | Later run's result JSON, mesh details, convergence CSV |
| [`gmsh_2026-10-17_1632UTC/`](gmsh_2026-10-17_1632UTC/) | Python 3.12.11 on WSL2; Gmsh 4.15.2, GUDHI 3.13.0 | 92 PASS, 0 FAIL **reported** | Separate Gmsh/GUDHI run's result JSON, mesh details, convergence CSV, package-version snapshot |

Run timestamps are reported by the submitted JSON files, not independently certified clock times. The first run was generated at 16:06:23 UTC and its original manifest at 16:06:26 UTC; the later runs at 16:27:49 and 16:32:37 UTC, respectively.

## Provenance reconciliation: no history rewritten

The `implementation_manifest.json` in `original_2026-10-17_1606UTC/` is **unaltered**. It lists 14 files and their original sizes/SHA-256 values. The first run's `results/reproduction_results.json` was subsequently overwritten in its source working directory. The separately recovered original output (26,175 bytes; SHA-256 `26aab3dfd025620f1e59e02b0f29e40483794993e24300f85c15411217fc103b`) has now been restored to the original timestamped snapshot, making **all 14/14 listed manifest entries match**. The later overwritten fallback result (26,231 bytes; SHA-256 `8091f04522a576e809e76ca21a33e01dfbab98980ffcc86f1fd90d134b63934d`) has its own timestamped directory.

The Gmsh/GUDHI run postdates the first manifest and was never part of its 14-file inventory. It is preserved as a separate event, **not retroactively inserted into or claimed to be covered by the original manifest**. The supplemental `archive_integrity.json` inventories all three retained records without altering them.

## Submission preservation and exclusions

This archive commits all relevant human-authored source/protocol/test files and all three substantive result sets: **22 preserved files**, plus this explanatory index and the supplemental integrity inventory. The approximately 133 MiB source ZIP is **not** copied into GitHub because it contains an entire virtual environment. The later lightweight ZIP contains the same relevant non-environment files, while the first-run overwritten JSON was recovered separately. We also deliberately exclude `.venv/`, `__pycache__/`, `*.pyc`, and Windows `Zone.Identifier` metadata.

Original ZIP SHA-256: `96f10252cef652d643c45a765eb4d918dad80120273f2152099bcd17eed4eec6`.  
Lightweight ZIP SHA-256: `fcb408926043c220441b349fc74e4c6883c0ab9481ef6d858e35ee6c22f153df`.

## Evidence limits and blinded comparison

- Investigator B's JSON declares a fresh implementation and proofs. Independent authorship is **reported by the submission**, not independently certified by the existence of a script alone.
- A fallback-backend rerun of the 92 controls and eight unit tests was separately reported in the audit; the Gmsh/GUDHI backend was reviewed for internal consistency, but was **not independently rerun** by that audit.
- The tests establish specified mathematical examples: nonzero periods of a closed non-exact 1-form; local bundle curvature and integer flux; and local entropy-coupled exact curvature redistribution with fixed cohomology class. They do **not** establish an entropy-derived topological law or observational correspondence.
- Both Investigator A's preliminary files and these Investigator B files are in the **same visible draft PR**. GitHub access does not implement cryptographic blinding. Any independent comparison must document prior exposure and freeze submissions before adjudication.
- The original Investigator A C-03 smoke-test assertion defect and any unexecuted gauge/mesh tests remain open unless corrected in a separately versioned test.
- This evidence does **not** activate `EXP-ECC-B01`, amend `PAR-ECC-001`/`NULL-ECC-001`, modify support flags, choose a foundation, or revise the ECC monograph's dependent theorems.

## Recommendation

Retain PR #103 as **DRAFT/UNMERGED**. Record subsequent corrections or new executions in new timestamped directories, rather than overwriting these frozen submissions. The next gate is independently reviewed paired comparison, discrepancy and coverage analysis, and a predeclared foundation-selection/non-selection rule.
