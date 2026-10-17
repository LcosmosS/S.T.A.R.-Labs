# ECC-B01 — Investigator A fixture kit (draft PR #103)

**Status:** documentation and source code only; mathematical fixture smoke test, **not** activated controlled execution, independent reproduction, or physical evidence.

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

## Included / intentionally withheld

- `investigator_a.py`: source copied from the original test kit.
- `protocol.md`: draft mathematical fixture specification accompanying the original kit.
- `partner_handoff.md`: original partner handoff, previously written for SageMath/PARI-GP; the current Investigator B contingency may use Python/SymPy/Gmsh/GUDHI under the same independent mathematical protocol.
- **Not committed:** `investigator_a_results.json` from the earlier demonstration run. That file is a preliminary fixture demonstration, not a frozen WSL investigator submission. Keep your new results local until the submission procedure and blinding boundary are agreed.

The supplied code performs 15 symbolic/numerical checks. **It does not run Gmsh/GUDHI meshes, four-resolution cochain convergence, or any physical/astronomical inference.** A `PASS` here is a smoke-test outcome, not the ECC-B01 primary decision.

Review note: the present `C-03` assertion passes an unconditional Boolean `True` rather than independently checking the computed residual. This should be corrected under the protocol review before the fixture suite is treated as frozen or comprehensive.

## Independence and governance

Known exact fixture targets are public. The *implementations and investigator-specific observed outputs* must be kept independent until committed to separate immutable submissions. Neither investigator should inspect or port the other's implementation before submitting results. Code hosted in this PR is visible; coordinate access and implement independent derivations accordingly.

This PR does not change experiment registries, support flags, claims, or the ECC monograph's dependent theorems. Keep it in draft, unmerged state pending two investigator submissions and documented adjudication.
