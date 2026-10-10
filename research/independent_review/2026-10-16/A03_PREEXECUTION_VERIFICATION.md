# A03 pre-execution verification

Actual local verification date: **2026-10-10**. The directory date identifies the
October 9-16 weekly milestone; it does not claim a future test took place.

Governing authority: [Research Charter v0.2](../../../charter/STAR_Research_Charter_v0-2.pdf),
SHA-256 `9a63284900d5349f1d307160929b2542885e4c751439b785369b722d349a5c03`.
Relevant sections: 6 (BSD independence), 12-15 (statistics, nulls, alternative
mappings and parameter locking), 17 (claim existence versus support), 28-31
(negative results, success levels, independent confirmation and reproducibility).

## Disposition

**PASS for the checks described below. Activation remains blocked pending separate
off-author scientific/governance approval.** This package is a second computation
path with reproducible reference checks; it is not independent investigator
replication, a scientific result, or an approval docket.

The checked clean local revision was
`e9ce748b526d2c9af209a2e5bcf88bc39357678d`, built on main
`edb8f4d94c1bccc23ca108655a7b72cf8c429ce9`. The local machine-readable receipt
is [local_verification_2026-10-10.json](local_verification_2026-10-10.json).
It contains all checked input hashes, five registry-row binding hashes,
environment versions, synthetic outputs, and blocked-function names.
The final PR adds this report and receipt after that clean verification commit;
its CI must recheck the final revision and archive a new receipt.

## Source and arithmetic checks

The source was freshly fetched from the exact publisher commit URL:
[JohnCremona/ecdata source](https://raw.githubusercontent.com/JohnCremona/ecdata/25cec5ecfec8b9f016eb1631ac633194c2bed39f/allcurves/allcurves.00000-09999).
The repository's declared gitlink was also checked. This procedure verifies the
specified raw artifact and its gitlink, not a fully initialized upstream checkout.

| Check | Actual result | Disposition |
|---|---|---|
| Source SHA-256 | `259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968` | PASS |
| Source bytes / rows | 2,146,401 / 64,687 | PASS |
| Curve-number-1 representatives | 38,042 unique classes | PASS |
| Exact j=0 exclusions / accepted curves | 106 / 37,936 | PASS |
| Accepted labels and exclusions | Exact agreement between reference parser and frozen loader | PASS |
| c4 and Delta | Exact integer agreement on every representative | PASS |
| Principal-log branch | x and z agree exactly; direct log(abs(j)) agrees within 1e-12 absolute rounding tolerance | PASS |
| Frozen protocol/code/config/manifest bindings | Exact source-file and registry-row hashes match the execution spec | PASS |

The reference parser uses whitespace fields and literal integer a-invariants
without calling the production parser. It selects number-1 representatives and
excludes exact j=0 before reading accepted rank labels. It computes
`c6 = -b2^3 + 36*b2*b4 - 216*b6` and
`Delta = (c4^3 - c6^2)/1728`, rather than using the production b8 discriminant
formula. A symbolic polynomial expansion proves the two expressions identical.
The reference j is an exact rational number. The floating comparison tolerance
is a diagnostic allowance for equivalent logarithm evaluation; it changes no
registered coordinate calculation, parameter, or acceptance rule.

Accepted-label SHA-256 (conductor/ASCII order, LF-separated):
`9a9784bd2ccb0b89f072db365ab4dd3ac52460b6574effeea2efb406621c105a`.
Excluded-label SHA-256 (ASCII order, LF-separated):
`ddab1f40f49367c1f83595e2234cac1bd05d958e399bf89bae9780d8571a2c2d`.

## Deterministic and safety checks

| Check | Actual result | Disposition |
|---|---|---|
| k=10 graph against all-pairs reference | 40-row tie, duplicate, asymmetric fixtures: 237 / 243 / 267 edges | PASS |
| Duplicate coordinates / ASCII ties / self exclusion | Same unique sorted undirected edges as reference; graph unchanged by rank reversal | PASS |
| Conductor strata | Exact floor(10*i/n) membership on 40-row and unequal 37-row fixtures | PASS |
| SplitMix64 | 128 words agree with independent implementation; fixed seed-zero vectors checked | PASS |
| Fisher-Yates / rejection sampling | Continuing stream agrees over eight permutation sizes; boundary and maximum uint64 draws rejected | PASS |
| Original-rank permutations | Three draws per synthetic fixture agree with reference; each stratum's rank multiset preserved | PASS |
| Binding-only preflight | PASS on clean tree | PASS |
| Normal execution preflight | Rejects both inactive experiment and dataset flags | PASS |
| Focused regression tests | 31 passed in the isolated local environment | PASS |
| Scientific files and registry bytes | Hashes unchanged across verification | PASS |

The real-cohort pass replaces graph, endpoint, null, fixture-statistic, and run
functions with exceptions. It verifies cohort construction only. The brute-force
reference additionally rejects more than 64 rows. No real-cohort graph, observed
statistic, experimental null distribution, effect size, p-value, or decision was
computed. Existing regression coverage includes a 999-draw **synthetic fixture**;
that is not the registered 37,936-curve experiment.

Seed 4103, B=999, alpha=0.005, one-sided greater inference, and the four-file
contract remain locked. The spec requires `summary.json`,
`observed_mcj_projection.csv`, `null_statistics.csv`, and
`exclusions_j_zero.csv`; output reservation/failure/overwrite protections are
covered by the safety suite. Both experiment and dataset execution, controlled
support, and physical support flags remain false.

## Reproduce

Use a clean checkout with the exact ecdata artifact hydrated. Install the direct
version pins in [requirements.txt](requirements.txt), then run from repository root:

```sh
python -c 'import runpy; runpy.run_path("research/independent_review/2026-10-16/verify_a03.py", run_name="__main__")' --output /tmp/a03-new-receipt.json
python -c 'import runpy; runpy.run_path("scripts/validate_exp_map_a03_preregistration.py", run_name="__main__")'
python -m pytest -q tests/test_a03_reference_verification.py tests/test_exp_map_a03_candidate.py tests/test_exp_map_a03_safety.py
```

Use a fresh output path outside the checkout: receipt creation is exclusive and
binding preflight requires a clean tree. The dedicated
[CI workflow](../../../.github/workflows/a03_preexecution_verification.yml)
fetches and hashes the frozen publisher artifact, repeats these checks, and
publishes the receipt as `a03-reference-verification`.

The local environment was Python 3.12.13, NumPy 1.26.4, pandas 2.2.3, SciPy 1.13.1,
SymPy 1.13.3 and PyYAML 6.0.2. Direct pins and recorded runtime versions document
this verification environment; they do not establish an authorized experiment
environment or a container digest.

## Discrepancies and blocking dispositions

- The transition ledger still describes A03 as planned/pending canonical
  transition, while PR #83 and the canonical registry say preregistered. A
  ledger-only follow-up is required; this verification package changes no
  lifecycle or scientific bindings.
- Off-author scientific/governance approval remains absent from this verification
  package. Review the exact final activation revision separately; passing these
  checks cannot provide that approval or authorize execution.
- Synthetic fixtures cannot exhaust all binary64 neighbor-boundary cases. Any
  later discrepancy affecting the frozen scientific implementation must be
  preserved and block activation; a scientific correction requires a new
  protocol version and Experiment_ID.
- The source hash identifies published rank labels; these checks do not prove
  every rank independently, prove BSD, or establish any astronomical relation.

Failure of any source/count/membership/arithmetic/graph/stream/hash/gate check
must fail the verifier or CI job and block activation. Retain failed receipts
and diagnostics rather than changing the frozen target to obtain a pass.

## Manuscript-ready methods subsection

EXP-MAP-A03 preregisters an internal arithmetic rank-coherence test on 37,936
number-1 isogeny representatives from a frozen Cremona ecdata source, after 106
exact j=0 exclusions. Its rank-blind embedding is (ln N, Re(log j), Im(log j))
on the principal branch. The locked endpoint uses a deterministic Euclidean
k=10 graph, with ASCII label tie resolution, and compares neighboring ranks
against 999 conductor-stratified permutations generated with seed 4103. The
one-sided test uses alpha=0.005. Pre-execution verification checked exact
arithmetic, membership, source/code/configuration hashes, synthetic graph and
permutation fixtures, and closed execution gates. The registered experiment
has not been executed by this package. No statistical outcome, physical
correspondence, BSD proof, predictive utility, or independent replication is
claimed.

Context: [PR #83](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/83) froze A03;
[PR #84](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/84) added governed
observational intake; [PR #78](https://github.com/LcosmosS/S.T.A.R.-Labs/pull/78)
is a separate A01 activation proposal and is outside this verification scope.
