# A01 execution and null-result preservation handoff

**Primary authority:** [locked A01 protocol](../../../preregistrations/EXP-MAP-A01/protocol.md), [config](../../../preregistrations/EXP-MAP-A01/config.json) and [Charter](../../../charter/STAR_Research_Charter_v0-2.pdf). All protocol choices below **repeat**, and do not amend, the frozen preregistration.

## Before execution

- Verify an **approved and merged** activation, source-locked checks, clean checkout and source hash from pinned `data/ecdata`; confirm actual `Controlled_Execution_Eligible` and runner preflight.
- Take execution-specific SHA, environment lock, full source checksum, registry/protocol/spec hashes, executor identity and independent off-author activation approval. Author of code is not independent reproducer.
- Freeze cohort at 38,042 isogeny-class first representatives of 64,687 rows (N=11…9,999); discriminants recomputed from integral coefficients exactly; no exclusions or imputation.
- Freeze `longitude=360 ln|Delta|/ln(1e30)`, `latitude=180 ln N/ln(1e9)`, `elevation=200 rank` without rank input to graph; unique undirected 10-NN edges with ASCII-label tie breaking.
- Freeze single endpoint `T=-mean(|200 rank_i-200 rank_j|)`, 999 global permutations using continuous SplitMix64/Fisher–Yates state seed 1729, `p=(1+count(T_null>=T_obs))/1000`, `alpha=0.01`.
- Validate all source and full configuration checks. No early peeking, subgroup endpoint, posthoc reweighting, graph recomputation, or adaptive draw stop.

## Transaction and independent rerun (not executed here)

After authorization, in a clean checkout use the repo's actual CLI:
```sh
star-controlled-experiment preflight --spec controlled_execution/specs/EXP-MAP-A01.json
star-controlled-experiment run --spec controlled_execution/specs/EXP-MAP-A01.json --executor-id investigator-A
```
Then, by a genuinely separate individual/environment, perform the runner's documented `rerun` and `verify-reproduction` transaction. Preserve all receipts, **never** overwrite an attempt, even if the first run fails or finds a null result. Do not call a repeated execution by the same researcher an independent human replication.

## Output/report decision table

| Condition | Controlled scientific disposition |
| --- | --- |
| Source/input hash, license, cohort, protocol or gate invalid | `INELIGIBLE_PROTOCOL_OR_DATA`; quarantine artifacts |
| Numerical/runtime failure or incomplete 999 draws | `INCONCLUSIVE`; preserve failed transaction |
| Valid complete run and `p < 0.01` | Reject **only** the registered global rank-permutation null |
| Valid complete run and `p >= 0.01` | **Do not reject** the registered null; not proof that effects are zero |
| Independent rerun discrepancy | `VALID_REPLICATION_FAILURE` only after verifying both runs eligible and checking locked reproducibility criteria; otherwise investigate and preserve |

Report observed statistic, graph edge count, all 999 null values, exceedance count, p-value, effect/uncertainty, source rows, exact code/dependencies and all deviations. Commit **no** controlled outcome files as part of this readiness PR. Regardless of statistical direction, support flags are not automatically upgraded; arithmetic-only results are not cosmological validation.
