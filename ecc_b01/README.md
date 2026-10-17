# ECC-B01 — Investigator A fixture kit (draft PR #103)

**Status:** documentation, source code, and a preliminary uploaded Investigator A WSL fixture report; **not** activated controlled execution, independent reproduction, or physical evidence.

This folder is copied from the previously issued `ECC_B01_Investigator_A_Test_Kit.zip` for use on the **draft** branch `docs/ecc-b01-blinded-foundation-comparison`. The governing proposal is [EXP-ECC-B01_FOUNDATION_COMPARISON_PROPOSAL.md](../research/gates/EXP-ECC-B01_FOUNDATION_COMPARISON_PROPOSAL.md), under [ECC_RTCH_RECOVERY.md](../research/gates/ECC_RTCH_RECOVERY.md).

## Run in WSL

From the repository root (`~/S.T.A.R.-Labs`):

```bash
git fetch origin
git switch docs/ecc-b01-blinded-foundation-comparison
git pull --ff-only origin docs/ecc-b01-blinded-foundation-comparison
ls -l ecc_b01/investigator_a.py
python -m pip install sympy numpy scipy
python ecc_b01/investigator_a.py ecc_b01/investigator_a_results.json
```

Alternatively:

```bash
cd ~/S.T.A.R.-Labs/ecc_b01
python investigator_a.py investigator_a_results.json
```

Do **not** run `python investigator_a.py` from the repository root: the script lives in `ecc_b01/`. Do **not** use `/ecc_b01/investigator_a.py`: that absolute path addresses the filesystem root, not your home-directory repository.

If the file is still missing after checkout, inspect `pwd`, `git branch --show-current`, `ls -la ecc_b01`, and `find ~/S.T.A.R.-Labs -name investigator_a.py -print`.

## Included / submitted evidence

- `investigator_a.py`: original test-kit source, unchanged.
- `protocol.md`: draft mathematical fixture specification accompanying the original kit.
- `partner_handoff.md`: original partner handoff; Investigator B can use a genuinely independent SageMath/PARI-GP or Python/SymPy/Gmsh/GUDHI workflow.
- `submissions/investigator_a/preliminary_2026-10-17/results.json`: **user-uploaded WSL run**, reporting 15/15 PASS; source SHA-256 and environment recorded in file.
- `submissions/investigator_a/preliminary_2026-10-17/README.md`: immutable report hash, provenance, known C-03 unconditional PASS defect, scope limits, and blinding caution.
- Root-level `investigator_a_results.json` is still ignored as a local transient output; the separately archived preliminary submission is intentionally tracked. The earlier demonstration result is not being substituted for the user's WSL output.

The supplied code performs 15 symbolic/numerical checks. **It does not run Gmsh/GUDHI meshes, four-resolution cochain convergence, or any physical/astronomical inference.** A `PASS` here is a smoke-test outcome, not the ECC-B01 primary decision.

Review note: the present `C-03` assertion passes an unconditional Boolean `True` rather than independently checking the computed residual. This should be corrected under the protocol review before the fixture suite is treated as frozen or comprehensive.

## Independence and governance

Known exact fixture targets are public. **Investigator A's source and preliminary WSL results are now visible in this draft PR** at a clearly labeled submission path, so strict blind access is not enforced by GitHub. Investigator B should not inspect Investigator A's source or results until their own implementation and results have been committed; record any prior exposure transparently. A later blinded comparison requires independently frozen output submissions and a documented access protocol.

This PR does not change experiment registries, support flags, claims, or the ECC monograph's dependent theorems. Keep it in draft, unmerged state pending two investigator submissions and documented adjudication.

## Investigator B submission — Shaughn McNamara

Investigator B's independently submitted package is maintained in [draft PR #108](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/108). The [evidence index](submissions/investigator_b/README.md) links the reviewed #108 head, three distinct run records, attestation, manifests, and the complete historical #103 archive by immutable SHA. Imported evidence copies were removed from the current tree by a forward commit; historical bytes remain accessible without rewriting history.

See the [integrity receipt](verification/2026-10-17_cross_pr_integrity.json) and [non-claim/governance checklist](GOVERNANCE_GATES.md). Both PRs remain DRAFT/UNMERGED. Public historical access remains a blinding limitation; reported mathematical fixture passes do not imply physical support or a selected foundation.
