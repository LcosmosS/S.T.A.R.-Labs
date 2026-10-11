# EXP-MAP-A01 — approval and source lineage

**Governing PDF:** `charter/STAR_Research_Charter_v0-2.pdf` SHA-256 `9a63284900d5349f1d307160929b2542885e4c751439b785369b722d349a5c03`.

1. **Historical development:** A01 was formerly explored among many arithmetic/cosmic mappings. The repository-qualified A01 preregistered null is a distinct, narrower, one-endpoint experiment and is not an alias for the broad STAR-PDF mapping-family comparison.
2. **Preregistration (frozen):** [`protocol`](../../preregistrations/EXP-MAP-A01/protocol.md), [`config`](../../preregistrations/EXP-MAP-A01/config.json), [`source manifest`](../../preregistrations/EXP-MAP-A01/dataset_manifest.json). Original status was controlled-execution inactive; no claims of a run.
3. **Unauthorized historical transition and reversal:** Original [PR #64](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/64) was reverted by [PR #77](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/77), retaining the Aladin Lite sky-release gate.
4. **Separate shared dataset compatibility:** [PR #87](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/87), merge `4f89bd3bc5c2225d9b0d2ce985e7eb18e8cbd73d`, introduced reviewed reversible A01/A03 binding checks.
5. **Reviewed final activation:** [PR #78](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/78), final head `e0e57cd336a9fce84f21fafadce49ebfcc56fa67`, approved by `LibertySquared` (2026-10-11 01:05:41 UTC) and merged at `7f1a03692539542e23b78263422f3be71da952ea`. This is the provenance record for the **two execution eligibility flags**, not a controlled scientific result.
6. **Exact-head CI:** [A01 source-locked preflight](https://github.com/LcosmosS/S.T.A.R.-Labs/actions/runs/38098877617), [S.T.A.R. CI](https://github.com/LcosmosS/S.T.A.R.-Labs/actions/runs/38098877574), [A03 reference verification](https://github.com/LcosmosS/S.T.A.R.-Labs/actions/runs/38098877595); all reported success at the activation PR head.

### Canonical A01 and shared-dataset row hashes

| Record | Inactive/preactivation SHA-256 | Reviewed active SHA-256 |
| --- | --- | --- |
| `EXP-MAP-A01` | `31f0137f1de87ba1b548758383b664dab13515205a3c2696b0c0edf573a5f4b3` | `97dac41c4d8a866d0abbcdf5515829328e92ea1fb3cf7b4d03e1d9b9c0b9c868` |
| `DATA-ARITHMETIC` | `2fe4ab7f5763f39c6cde8392c3f7d8ff1a565e4664ce6e192640b99f3fe146d7` | `1b81e05ab90ce822c7dcbda88bdb206f191f6523fac03fea5ecdf55724de44c2` |

The A03 frozen execution spec continues to bind the **inactive** shared-dataset row. Compatibility checks prove the **only** difference is the A01 approved dataset eligibility bit. A03's experiment execution flag remains `false`; it must not acquire scientific or execution approval through A01.

**Postmerge status:** A01 execution eligibility true; controlled support false; physical support false. The existence of a merged activation is not evidence of any original experimental statistic, p-value or separate investigator replication.

**External review requirement:** Verify charter, immutable source bytes, locked scientific config, PR #78 human approval, PR #87 shared-dataset compatibility, and exact reviewed source/registry digests. Do not equate a review of this package with an approval of scientific results.
