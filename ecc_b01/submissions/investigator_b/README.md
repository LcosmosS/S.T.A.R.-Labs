# Investigator B evidence index — Shaughn McNamara

**Review date:** 2026-10-17. **Disposition:** keep PRs [#103](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/103) and [#108](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/108) DRAFT and UNMERGED. This index is packaging/governance documentation, not scientific approval.

## Ownership and pinned provenance

Investigator A/control protocol stays in #103. Investigator B's independently submitted package is maintained in #108, submitted by GitHub account `LibertySquared`. No change to #108 is made by this cleanup.

- Reviewed #103 head and complete pre-cleanup archive: [`c33916a35009674ab5abd5e74c717cc0289b1cbd`](https://github.com/LcosmosS/S.T.A.R.-Labs/commit/c33916a35009674ab5abd5e74c717cc0289b1cbd); [historical evidence directory](https://github.com/LcosmosS/S.T.A.R.-Labs/tree/c33916a35009674ab5abd5e74c717cc0289b1cbd/ecc_b01/submissions/investigator_b).
- Reviewed #108 head: [`79296815837985d25f4f1a732d89811814cac4ad`](https://github.com/LcosmosS/S.T.A.R.-Labs/commit/79296815837985d25f4f1a732d89811814cac4ad); [package README](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/79296815837985d25f4f1a732d89811814cac4ad/ECC_B01_Full_Independent_Reproduction/README.md).
- [Typed independent-authorship/non-consultation attestation](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/79296815837985d25f4f1a732d89811814cac4ad/ECC-B01%20Independent%20Reproduction%20Attestation.txt) signed Shaughn McNamara, dated 2026-10-17. SHA-256 `84527bae4c8e600eb6bdd7369315921dbdce936bce3619d0e55cf3965c0b083a` (4,637 bytes).
- [Governance/non-claim gates](../../GOVERNANCE_GATES.md) and [verification receipt](../../verification/2026-10-17_cross_pr_integrity.json).

This forward commit removes the imported 22 evidence/source files and supplemental archive inventory from #103's current tree, retaining this index. **No history is rewritten.** Thirteen evidence files are byte-identical to their #108 counterparts; nine source/document/dependency/test files have evolved in #108. Those nine historical versions remain at the pinned #103 SHA, not represented as byte-identical copies. The receipt supplies all 22 path/blob mappings and permanent links. The previous [archive index](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/c33916a35009674ab5abd5e74c717cc0289b1cbd/ecc_b01/submissions/investigator_b/README.md) and [supplemental inventory](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/c33916a35009674ab5abd5e74c717cc0289b1cbd/ecc_b01/submissions/investigator_b/archive_integrity.json) remain accessible in history.

## Three distinct run records

All times below are reported UTC timestamps embedded in submitted artifacts, not certified execution times. Each JSON reports 92 PASS / 0 FAIL for its specified mathematical checks.

| Record | Pinned #108 artifact | Toolchain interpretation |
| --- | --- | --- |
| 16:06:23 historical fallback | [recovered JSON](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/79296815837985d25f4f1a732d89811814cac4ad/ECC_B01_Full_Independent_Reproduction/results/reproduction_results_gmsh_missing.json) | Gmsh/GUDHI unavailable; gate blocked |
| 16:27:49 later fallback | [result JSON](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/79296815837985d25f4f1a732d89811814cac4ad/ECC_B01_Full_Independent_Reproduction/results/reproduction_results.json); [retrospective inventory](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/79296815837985d25f4f1a732d89811814cac4ad/ECC_B01_Full_Independent_Reproduction/run_manifests/fallback-20261017T162749Z.json) | Separate fallback record; gate blocked |
| 16:32:37 Gmsh/GUDHI | [result JSON](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/79296815837985d25f4f1a732d89811814cac4ad/ECC_B01_Full_Independent_Reproduction/results_gmsh/reproduction_results.json); [retrospective inventory](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/79296815837985d25f4f1a732d89811814cac4ad/ECC_B01_Full_Independent_Reproduction/run_manifests/gmsh-gudhi-20261017T163237Z.json) | Reports actual Gmsh/GUDHI gates PASS; not independently reexecuted in this audit |

The [unchanged original manifest](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/79296815837985d25f4f1a732d89811814cac4ad/ECC_B01_Full_Independent_Reproduction/implementation_manifest.json) names `results/reproduction_results.json` with SHA-256 `26aab3dfd025620f1e59e02b0f29e40483794993e24300f85c15411217fc103b` and 26,175 bytes. In #108 these bytes are explicitly remapped to `results/reproduction_results_gmsh_missing.json`. The present `results/reproduction_results.json` instead contains the later fallback record (`8091f04522a576e809e76ca21a33e01dfbab98980ffcc86f1fd90d134b63934d`, 26,231 bytes). Renaming the recovered file does not create a new original manifest entry.

The original manifest's **14/14 entries** were independently checked against the complete historical #103 snapshot. The new [#108 package inventory](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/79296815837985d25f4f1a732d89811814cac4ad/ECC_B01_Full_Independent_Reproduction/implementation_manifest_PR108_20261017T215518Z.json) passed **26/26 references**, and the two retrospective run inventories passed **10/10 references**, including their repeated historical-context references. SHA-256, byte counts, and Git blob hashes matched. This verifies artifact integrity only.

Historical run source SHA-256 is `7857fca7f3642fdaa896ab10c46e92ffb07588450bcf687a4791a830f3ec1639`. Revised #108 source SHA-256 is `a8ed8fbd9678fbd42944f4a83a9517e654ff4d8fe56f51f0aa0674cb0451fa21`. Historical 92-check reports and the eight-test log do not certify execution of the revised runner or its expanded tests.

## Receipts, independence and non-claims

#108 now contains unique-output/collision safeguards, a non-overwriting manifest writer, and code to emit `run_receipt.json` binding new outputs to source, environment, parameters and gates. The reviewed file list contains retrospective manifests but no committed fresh `run_receipt.json`. No new revised-source run is asserted here. Require the actual new run receipt and its hashed outputs before execution signoff.

The attestation declares independent authorship and non-consultation with A's results during initial development/reproduction. It is a typed declaration, not an external signature or proof of blindness. Both investigators' materials have been publicly accessible; removing current-tree duplicates cannot undo prior exposure or create retrospective blinding. Preserve exposure disclosures and freeze comparison criteria before adjudication.

Mathematical fixture passes do not establish physical/cosmological support, arithmetic correspondence, entropy-generated topology, a new ECC theorem, or foundation selection. This cleanup does not activate EXP-ECC-B01 or authorize registry, PAR/NULL, eligibility/support-flag, foundational-definition or dependent-theorem changes. See the [open gate checklist](../../GOVERNANCE_GATES.md).
