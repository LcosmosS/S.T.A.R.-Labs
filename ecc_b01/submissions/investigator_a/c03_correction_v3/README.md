# Investigator A C-03 strengthening — v3 (separate source revision)

**Status:** independently testable fixture implementation and CI-only evidence, not a formal Investigator A attestation or ECC-B01 approval.

The original 15-fixture `ecc_b01/investigator_a.py` and its preliminary result remain unchanged. The 16-fixture `ecc_b01/investigator_a_v2.py` and its historical 2026-10-17 WSL execution files remain unchanged. The v2 standalone package explicitly pinned NumPy 2.3.5, outside the main repository's `numpy>=1.26.0,<2.0` range. These results must be labelled nonconformant to the repository dependency constraint, although they were validly executed under the standalone package's own pin.

## What v3 changes

The `c03_record(candidate_entropy, reference_entropy)` function creates a complete C-03 result with `pass_=True` only if the exact symbolic second-derivative difference is zero. The ordinary fixture uses `S2+7` vs. `S2`, obtaining zero. The negative fixture calls **the same constructor** using `S2+7` vs. `2*S2`, obtaining nonzero `A*cos(phi) + B*sin(psi)` and `pass_=False`; C-03-NEG records successful rejection. Thus the negative test does not merely invert a Boolean independent of the C-03 result path.

## Reproduce

```bash
python -m pytest -q tests/test_ecc_b01_a_c03_v3.py
python ecc_b01/investigator_a_v3.py /tmp/ecc_b01_investigator_a_v3_results.json
```

For repository-conformant automated reproduction use `.github/workflows/ecc-b01-a-v3.yml`, which pins Python 3.12, NumPy 1.26.4, SciPy 1.17.0, SymPy 1.14.0 and pytest 9.0.2. The workflow verifies 16 results and both focused tests, records `results.json`, test/runner logs, dependency inventory, the source SHA-256 and a `SHA256SUMS` index in the workflow artifact `ecc-b01-a-v3-ci-evidence` tied to the CI commit. It does not add CI results to the independent-investigator submission without separate human review.

**Review boundary:** Pass/fail of mathematical fixture controls is not physical ECC validation, a new theorem, experimental activation, proof of independent Investigator A execution, or blinded cross-investigator adjudication. PR #103 remains draft and unmerged.
