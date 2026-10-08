# M1-INH-E1b — local execution provenance and negative history

**Source:** user-reported terminal and IPython \`%run\` outputs in the research discussion, followed by a separate assistant-side v4 run. The user's execution logs have not been externally attested. Treat the four versions as related implementations, **not four independent validations**.

## User-reported successful file executions

All four ran with \`%run\` as saved source files in \`/home/kepler\`. Each reported exact symbolic checks passing for S1 and S2, plus

\`\`\`text
S1: 16 Einstein-dust components, dust algebra, shear identities, projector identities, Euclidean embedding, J: PASS
S2: 16 Einstein-dust components, dust algebra, shear identities, projector identities, Euclidean embedding, J: PASS
ALL EXACT METRIC-FIRST E1b CERTIFICATE CHECKS PASSED
\`\`\`

| Command | User-reported SHA-256 | Certificate location |
| --- | --- | --- |
| \`%run m1_inh_e1b_metric_first_audit.py\` | \`2cea1c169a6080a08d9a6834d3d5a60e7095d38f4ebc9acec5e64126d8ce5a43\` | \`/home/kepler/m1_inh_e1b_metric_first_audit.json\` |
| \`%run m1_inh_e1b_metric_first_audit_v2.py\` | \`f35286d090d4c84c9c9a95ff30226254009c84fa81d52c78074d7802b06640a6\` | \`/home/kepler/m1_inh_e1b_metric_first_audit_v2.json\` |
| \`%run m1_inh_e1b_metric_first_audit_v3.py\` | \`8a7701f2a3d746d3b53068b5b6051772fac64177c05a3219b45c3f77c1f4e51a\` | \`/home/kepler/m1_inh_e1b_metric_first_audit_v3.json\` |
| \`%run m1_inh_e1b_metric_first_audit_v4.py\` | \`10ccfa264f475fd7bd6d490c80c8862a174730567ee51c0d759b87939b93e6bb\` | \`/home/kepler/m1_inh_e1b_metric_first_audit_v4.json\` |

## Earlier notebook-cell failures (retained)

1. **Original copied-cell assertion:** \`S1: transverse Gram xx: NONZERO residual = -4/(x**2 + y**2 + 1)**2\`.
2. **v2 copied-cell assertion:** \`S1: coordinate-symbol mismatch for x; free symbols={x, y}\`.
3. **v3 copied-cell assertion:** \`S1: missing/mismatched coordinate Symbol('E1B_x', real=True); free symbol identities=["Symbol('E1B_x')", "Symbol('E1B_y')"]\`.

The failures arose when code was executed in notebook cells. Later file-based \`%run\` invocations of **all four** versions passed. The observed discrepancy is consistent with symbol assumptions or differences between cell and file execution, but no single root cause was independently established for each notebook failure. These failures must not be erased from the record.

## Independent assistant-side reproduction

- Fresh execution of the canonical v4 source in a separate runtime reported both sectors passing.
- Source SHA-256: \`10ccfa264f475fd7bd6d490c80c8862a174730567ee51c0d759b87939b93e6bb\`.
- Python syntax compilation completed.
- The attached JSON reports SymPy 1.14.0; repository \`requirements.txt\` currently pins SymPy 1.13.1, so CI on that version must not be claimed equivalent without execution.

## Previous numerical fixture (not a proof)

A NumPy centred-difference comparison at three interior points used \(\varepsilon=10^{-6}\) and \(\mathrm{rtol}=10^{-5}\), giving reported relative errors \(3.320\times10^{-10}\), \(1.460\times10^{-11}\), \(2.018\times10^{-10}\). Only one step size was used; **numerical convergence was not established**. Density ordering and \(\mathcal J_1=0\) were explicitly evaluated at the original single test point. This fixture corroborates, but neither derives nor independently validates, the curvature identities.

## Interpretation and unchanged gates

- Canonical E1b proof calculation: symbolically reproduced in assistant and user file-execution environments.
- External referee or independently maintained implementation: **pending**.
- General M1-INH-E1a Einstein-to-Weierstrass predecessor: **pending**.
- E1c observable-specific insufficiency: **untested**.
- P0-T001 full-parent audit: **unresolved separately**.
- Formal controlled execution/support flags and physical-support claims: **unchanged and false**.

No historical findings, published audit baseline or registered theory-search protocol should be rewritten to promote this candidate.
