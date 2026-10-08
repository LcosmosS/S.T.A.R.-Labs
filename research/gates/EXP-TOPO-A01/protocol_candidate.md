# EXP-TOPO-A01 — prospective, computation-bounded topology protocol candidate

This is a **new, pre-outcome candidate specification**, not a reconstructed historical choice and **not a canonical preregistration**. The canonical experiment, parameter and null registries remain planned/not-preregistered, and all execution and support flags stay false.

## Question and scope

Does elliptic-curve rank contribute to the `H_0` clustering geometry of a rank-containing but non-cosmological arithmetic projection, relative to conductor-matched rank randomization? This is an **internal arithmetic** test; `CLAIM-ACSC-003` receives **no cosmological evidence** from a rejection.

## Preregister-before-execution controls

- Pinned A01 ecdata bytes, 64,687 source rows, 38,042 unique isogeny representatives. SHA-256 `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968`.
- Rank-blind, deterministic sample: SHA-256 of each canonical Cremona UTF-8 label; sort full 32-byte digests, tie-break by ASCII label, take exactly 1,024. Record every selected ID.
- Points: `(ln|Delta|/ln(1e30), ln N/ln(1e9), rank)` using exact integer discriminants first, then binary64 logarithms, Euclidean distance. No learned scaling, jitter or deletion of duplicate coordinates.
- Filtration: **Vietoris–Rips** at edge length `epsilon = d(x,y)` (not half-distance). Calculate degree-0 persistence only. All 1,024 births at zero; exactly 1,023 finite bars including any zero deaths; discard the one essential infinite bar. The finite death multiset equals the Euclidean MST edge weights.
- **Only endpoint:** `T_obs=-mean(all 1023 finite H0 deaths)`. A larger value means tighter arithmetic point-cloud clustering.
- **Null:** conductor-sorted equal-population deciles assigned *on the selected 1,024 curves*; permute rank inside each decile, leaving IDs, conductors, discriminants, `xy`, rank multiset per decile, and sample membership unchanged. `splitmix64-fisher-yates-v1`, 999 sequential draws, seed `8401`, no rerolls.
- One-sided `p=(1+#(T_b>=T_obs))/1000`, `alpha=0.003`. Report all draws, sample labels, MST deaths, source/config/output hashes. Do not use historical `W2<0.01` as a result or rejection criterion.

## Acceptance/failure

Before canonical status transition: implement both MST and independent `H0` persistence on synthetic fixtures, including coincident points, stable tie resolution, and verify finite death multisets within `10^{-10}`. A short toy fixture must not be mistaken for a full controlled result. Fail on any hash/cohort/finiteness/selection/multiplicity mismatch; preserve failures. No tuning after viewing outcomes. The 1024-subsample result does not imply a conclusion for all ecdata classes; an all-cohort test would be a **new experiment**.

## Interpretation

Even a small p-value indicates arithmetic rank/topology dependence under this **specific conditional permutation**; the test is not independent of the arithmetic geometry encoded by conductor/discriminant, does not test cosmic topology, and cannot provide physical-support promotion. The `alpha=0.003` choice does not retrospectively adjust A01's already frozen `0.01` threshold; no uncorrected pooled family inference is allowed.

Machine-readable candidate: [config](./config.json). Required next gate: separate code/spec implementation and explicit canonical lifecycle transition with audit-immutability handling.
