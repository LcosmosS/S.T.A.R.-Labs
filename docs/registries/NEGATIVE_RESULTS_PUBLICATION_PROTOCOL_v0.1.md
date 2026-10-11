# S.T.A.R.-Labs — Negative results, obstructions, and theory retirement protocol v0.1

**Status:** prospective reporting and review policy; not a preregistration amendment and not an executed result.  
**Authority:** [STAR Research Charter v0.2 PDF](../../charter/STAR_Research_Charter_v0-2.pdf), especially §§3, 10–19, 28–31 and 36–37.  
**Scope:** mathematical counterexamples, null experiments, mechanism-screen failures, replication failure, and invalid or inconclusive runs.

## Principle and non-promotion rule

A failed hypothesis can be a sound, publishable scientific result. A failed **verification gate** is not automatically a scientific refutation, and a non-significant p-value is not evidence that the null is true. Preserve the distinctions among: (a) **valid null rejection**, (b) **valid null non-rejection**, (c) **validated mathematical obstruction**, (d) **negative predictive/replication outcome**, (e) **mechanism candidate ineligible or retired**, and (f) **invalid or inconclusive execution**.

An experiment's result may support only the precisely frozen claim and population it actually tests. Neither favorable nor unfavorable results may leap from arithmetic-only computations to astronomical correspondence, BSD truth, or physical theory. Charter claim categories (D/E/M/P/H/C/T/S) and the success ladder (Levels 0–5) remain separate from execution and review statuses.

## Mandatory outcomes and closure criteria

| Track | Defined decision / publication unit | Permitted negative conclusion | Not permitted |
| --- | --- | --- | --- |
| `EXP-MAP-A01` | Preserve its frozen analysis cohort, `k=10` base-plane neighbor graph, \(T=-\mathrm{mean}(|200r_i-200r_j|)\), exactly 999 fixed-seed rank permutations, and \(\alpha=0.01\). Record observed statistic, full null distribution and p-value | If `p >= 0.01`, **do not reject the specific global-rank-permutation null**. Publish effect size, uncertainty, power/precision limitations and context. If `p < 0.01`, reject only that specified null | “ACSC proven/disproven,” “no arithmetic correspondence exists,” “physical prediction confirmed,” or changing A01's null after observing data |
| `EXP-MAP-A03` (separate successor) | Run only after its own preregistration and activation; stratified/conditional null and group definitions fixed beforehand | Positive or negative result conditions whether arithmetic structure exceeds its prespecified conditional control | Retroactively substituting its null for A01, unregistered endpoint shopping, or synthesizing post-hoc significance |
| `M1-INH-E1a` | Independent reproduction of the exact frozen evolution, density and Weierstrass conventions | A convention/algebra inconsistency is a **protocol-specification failure** requiring terminal archival record for the frozen audit | Silently changing the elliptic record or calling the inconsistency a universal physical no-go theorem |
| `M1-INH-E1b` | Two regular Einstein–dust solutions, identical full \(\mathfrak E\) and branch conventions, differing in curvature-determined scalar \(\mathcal J\); independent tensor, regularity and arbitrary-diffeomorphism audit | If verified: *the registered elliptic evolution data are insufficient to reconstruct full matter inhomogeneity in this Szekeres–Szafron class* | Extending to all elliptic cosmologies, confusing gauge differences with physical inequivalence, or claiming independent proof based only on a self-test |
| `M1-INH-E1c` | Independently select and freeze target observable \(Q\), then assess *observable-specific* sufficiency | Report insufficiency, sufficiency within scope, or inconclusive result for that particular \(Q\) | Assuming E1b implies every lossy observable must differ |
| `P0-SF-v0.1` | All five frozen `P0-T001`–`P0-T005` candidates independently reviewed to auditable terminal statuses, preserving each derivation/counterexample | If all fail under frozen criteria: *no eligible parent was found within P0-SF-v0.1; mechanism-level ACSC-v0.1 is retired as an active physical hypothesis within that closed frame* | Treating five candidates as all possible theories; reopening a failed candidate by silently changing the selection rule |
| ECC / SFT exact-form audit | Check globally defined fields, cochain degree, exactness, transition data, and actual nonzero cohomology class | The specific global \(\theta=d\mathcal M,\omega=d\theta\) construction cannot provide a nontrivial \([\omega]\) | Claiming all conceivable entropy cohomology theories are impossible |
| RTCH conventional-limit gate | A frozen, dimensionally consistent variational action and independent derivation of field equations, signs, conservation and standard-physics limit | If recovery fails, the frozen candidate **fails the necessary consistency gate**, and physical-claim promotion stops | Treating a failed recovery check as a refutation of GR or of every possible completion |
| Astronomical matching / SFR | Frozen source versions, exact matching, group-disjoint holdout and leakage-controlled baselines; record discarded objects and selection effects | Invalid matches are quarantined; on valid data, report a null/non-improving model even if it contradicts historic high fit metrics | Treating prior exploratory fit scores as confirmatory evidence, or interpreting absence of improvement as universal disproof |

**Priority of frozen protocols:** This document may organize decision reporting but cannot amend A01, M1 or P0 preregistered thresholds, sample definitions, test statistics, hypotheses, gate authority or terminal state logic. Where detail conflicts, the pre-existing frozen protocol controls the *experiment design*, and the Charter controls *claim interpretation*.

## Predeclared disposition taxonomy

Use one of the following outcomes in the new result report; never silently replace one with another:

- **VALID_REJECT_NULL:** eligible controlled test rejects the *specified* null under its locked rule.
- **VALID_DO_NOT_REJECT_NULL:** eligible controlled test does not reject; absence of evidence is not a proved zero effect.
- **VALID_OBSTRUCTION:** all assumptions, solution regularity, invariants and non-equivalence independently verified, with a strictly scoped insufficiency/no-go statement.
- **VALID_NEGATIVE_PREDICTION:** valid prospective/held-out test fails its locked predictive performance criterion.
- **VALID_REPLICATION_FAILURE:** an independent and methodologically eligible rerun fails its preregistered agreement criteria; diagnose heterogeneity, power, and implementation before causal claims.
- **FRAME_EXHAUSTED_RETIRED:** every candidate in a *specified finite search frame* has a signed terminal outcome under the frame's rules.
- **INELIGIBLE_PROTOCOL_OR_DATA:** wrong sample/source, invalid associations, leakage, altered null, wrong dependencies, or corrupted artifacts: **not** a scientific null outcome.
- **INCONCLUSIVE:** numerical failure, insufficient precision or power, ambiguous review, or missing reproducibility evidence prevents a terminal scientific conclusion.

The first six are scientifically interpretable only if all applicable eligibility conditions pass. The last two remain transparent gate outcomes and may still be publishable as methodological investigations, but cannot be reported as evidence for or against the scientific target.

## Immutable report package

For every terminal attempt, create a new, dated, immutable report directory keyed by registered experiment/obstruction/search-frame ID **and** exact code revision. Do not edit the frozen source protocol or overwrite an earlier attempt. At minimum provide:

1. **Identity:** exact Claim_ID, Experiment_ID or obstruction/search-frame ID, frozen protocol version, registered hypotheses and permissible claim scope.
2. **Pre-run locks:** immutable dataset identities/versions/hashes, source rows, environmental lock, scripts, executable entrypoint, dependency commits, parameters, random algorithm and seeds, transformations, outcome threshold and null models.
3. **Integrity checks:** eligibility flags at execution, independent reviewer/approver record with actual identity and dated approval (never synthetic signatures), CI/run URLs and their exact SHA.
4. **Execution manifest:** UTC timestamps, machine/OS/runtime versions, status and exit code, complete stdout/stderr hashes, raw and derived data hashes, inclusion/exclusion counts, intermediate diagnostics and output file hashes.
5. **Full quantitative record:** statistic, sample size/effective sample size, complete null realizations when applicable, tail rule, p-value, effect size, uncertainty interval or justified bounds, power/precision limits, multiple-test family, and sensitivity diagnostics; mark fields genuinely inapplicable with reasons.
6. **Adversarial tests:** competing models/mapping families, negative controls, positive controls where suitable, failed assumptions, confounders, resolution/selection sensitivity, alternate code path, and contradictory evidence.
7. **Independent validation:** reviewer proof audit and/or investigator-B reproduction with independent environment or implementation, signed result interpretation and discrepancies; separate **independent reproduction of computation** from **independent verification of a mathematical proof**.
8. **Final disposition:** one taxonomy value above, exact supported statement, exact unsupported stronger statements, acceptance/retirement rationale, proposed follow-up registered as *new* work, and publication-ready limitation statement.
9. **Append-only record:** content hashes, stable citations, reviewed result revision, and a linked correction record if later errors are discovered. Preserve failures as fully as successes.

The report's author must not self-certify independent review. A missing independent review remains **pending review**, not accepted proof or replication. Do not equate a GitHub checkmark with a scientific endorsement.

## Publication-ready negative-result structure

A report is ready to submit for peer review **only when applicable prerequisites above are met**. It should contain: (i) question and falsifiable hypothesis; (ii) previously frozen protocol and sample; (iii) execution and reproducibility method; (iv) results including full failure diagnostics; (v) null distributions, baseline effects and uncertainties; (vi) independent review or reproduction; (vii) precisely scoped negative conclusion and competing explanations; (viii) limitations, data/software availability and permanent artifact identifiers.

For a mathematical obstruction, state the theorem, assumptions, counterexample/domain, complete algebraic/tensor certificate, invariance/non-isometry argument, and independent proof review. For a statistical non-rejection, never claim a negative theorem or exact zero effect; consider equivalence/non-inferiority tests *only* in a separately frozen prospective protocol with a justified margin and adequate precision.

## Governance and anti-retrofitting

- Treat acceptance of a negative outcome as a **success of the scientific process**, not as promotion of the original hypothesis.
- Result publication must be symmetrical: preserve negative and positive runs, null draws, computational failures, review disagreements, and source digests under the same reporting contract.
- Follow the Charter's ordering: discovery -> locked candidate -> blind/independent test -> replication. Physical interpretation is downstream of demonstrated correspondence and an adequate mechanism; mathematical theory checks may proceed independently but are not a shortcut to astronomical evidence.
- Require off-author review for changes to scientific claims, protocols and terminal dispositions. Approval must be actual and verifiable.
- Any new mapping, post-result parameter, revised physical action, alternative null, or new parent theory requires a separately dated/newly numbered protocol or search frame. Do not rewrite the original terminal decision.
- Nothing in this document switches controlled-execution, controlled-support, or physical-support flags; it establishes **criteria for later evidence**, not evidence itself.

### Frozen source references

- [A01 primary arithmetic test](../../preregistrations/EXP-MAP-A01/protocol.md)
- [M1-INH-E1 registered obstruction](../../preregistrations/M1-INH-E1/protocol.md)
- [P0-ANSATZ-001 finite search frame](../../preregistrations/P0-ANSATZ-001/protocol.md)
- [ECC/RTCH recovery gates](../../research/gates/ECC_RTCH_RECOVERY.md)
- [Charter-governed claim corrections](CHARTER_EPISTEMIC_CORRECTIONS_v0.1.md)
