# Investigator A C-03 assertion correction — version 2 (draft)

This is a **versioned correction**, not a replacement of historical evidence.

- Original source: `ecc_b01/investigator_a.py`, SHA-256 `68108885ff5349f53d4b692a6d3b1937cae7924e0c7954584794b5bd70b031f2`. Leave it unchanged.
- Original preliminary 15/15 result: `ecc_b01/submissions/investigator_a/preliminary_2026-10-17/results.json`. Leave it unchanged.
- Corrected script: `ecc_b01/investigator_a_v2.py`, locally checked SHA-256 `38c12d385f772edb9fbf6c76dfb6f11c0587cb450be8e37927c794bee089f0a8`.
- `C-03` now passes **only when** the simplified constant-shift invariance residual equals zero.
- `C-03-NEG` injects a deliberately wrong residual `1`. The same predicate must reject it; a regression to unconditional `True` would fail this control.
- Root test `tests/test_ecc_b01_a_c03.py` exercises both cases and runs the versioned script under a temporary output path. It is included in the existing root `pytest -q` discovery scope.

## Verification commands

```bash
python -m pytest -q tests/test_ecc_b01_a_c03.py
python ecc_b01/investigator_a_v2.py /tmp/ecc_b01_investigator_a_v2.json
```

Local preliminary check on 2026-10-17 (**assistant execution, not an Investigator A attestation**): 16/16 symbolic/numerical fixtures and 2/2 focused pytest regressions passed. The C-03 residual was `0` and the injected residual `1` was rejected. The standalone v2 package pinned NumPy **2.3.5**, outside the **main repository's** declared `numpy>=1.26.0,<2.0` range (though within the standalone package's exact pin). Therefore the v2 preliminary and subsequently committed WSL results are **nonconformant repository-dependency evidence**; retain them historically, but do not present them as repository-conformant validation or independent mathematical approval.

The further versioned `investigator_a_v3.py` tests the deliberately wrong comparator `2*S2` through the same `c03_record` path and verifies `pass_=False`. The new Python 3.12 / NumPy 1.26.4 workflow publishes its results separately as the `ecc-b01-a-v3-ci-evidence` artifact. Any successful CI run is an **automated, assistant-authored check, not an Investigator A attestation**; it must not retroactively replace v2 execution evidence.

**Evidence boundary:** A fresh Investigator A-owned run, immutable output manifest, independent review, and cross-investigator adjudication are still required under `ecc_b01/GOVERNANCE_GATES.md`. This correction does not establish complete ECC-B01 mathematical validation, activate controlled execution, amend registries, or authorize any physical claim. PR #103 remains draft.
