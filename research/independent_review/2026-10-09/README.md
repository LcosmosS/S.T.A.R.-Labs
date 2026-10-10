# Independent gate-readiness research packet — 2026-10-09

**Authority:** [STAR Research Charter v0.2, governing PDF](../../../charter/STAR_Research_Charter_v0-2.pdf).  
**Read-only baseline:** `58fef648fd33fb7cce6e9b7573b0522caac305e6` on main; [canonical experiment registry](../../../registry/experiment_registry_v0.2.csv).  
**Claim category:** methodology / audit; **not** a new theorem, control execution, independent human review, preregistration, or physical support.

## Verified starting point

The baseline canonical experiment registry has **18 experiments: 17 planned and one preregistered (EXP-MAP-A01)**. All execution, controlled-support and physical-support flags on that baseline are false. The pinned arithmetic experiment has a real frozen protocol and source-locked software, but cannot be executed as controlled evidence until the separate authorized activation gate. Software CI alone is not human approval.

See the [complete 18-experiment baseline census](experiment_gate_matrix.json), with exact registered dataset/parameter/null identifiers, status, and a specifically identified minimum next gate. This census is a dated **snapshot**, not the canonical source of record or an automatically updated approval.

## Snapshot date versus current canonical state

The 18-row `experiment_gate_matrix.json` is an **immutable October 9
baseline observation**, not today's live activation ledger. In that archived
snapshot A01 alone was preregistered and A03 was planned. Since then, merged
PR #83 preregistered `EXP-MAP-A03` on the canonical `main` branch, so
both A01 and A03 are preregistered with execution/support still disabled.
New observational publisher-source verification also advances provenance
without authorizing inference. Use `python scripts/independent_gate_report.py`
on the checked-out current revision for the live count; do not rewrite the
historical matrix to match newer science-control records.

The source review notes in this dated packet are **methodology and historical
blocker records**, not evidence that every issue is still unresolved after
later integration. In particular, CodeRabbit's S1 metric correction,
eligibility-flag validation, and five-terminal-failure P0 retirement restriction
are reflected in this PR's current files. Independent review must evaluate
the final merged-code candidate, not rely only on the October 9 baseline.

## Workstreams, hard stops and immutable results

| Workstream | What this branch supplies | Remaining **non-waivable** gate |
| --- | --- | --- |
| 1. A01 activation | [Independent PR #78 blocker memo](A01_ACTIVATION_INDEPENDENT_REVIEW.md), including missing watch paths, wrong filename, mutable actions and human review | Only an actual reviewed correction on PR #78 (or superseding activation PR), CI/runner preflight, protection enforcement and accountable off-author approval may activate |
| 2. M1 constructive pair | [Independent second computational route](M1_INDEPENDENT_REPRODUCTION.md): JAX double-precision automatic-differentiation curvature spot checks | Complete frozen E1a conventions, symbolic full-domain proof and *independent human expert* review; nonzero scalar at sampled points alone is not a theorem |
| 3. A01 null experiment | [Prospective execution and result-preservation checklist](A01_EXECUTION_HANDOFF.md) including no-overwrite transaction and symmetric negative outcomes | Do **not** run 999 permutations on unactivated main/this branch; source and protocol immutable, two documented independent transactions after activation |
| 4. Five P0 parents | [Nonterminal five-candidate review worksheets](P0_FIVE_CANDIDATE_AUDIT.md), with individual failure criteria | `N_unresolved=5`; no fabricated terminal statuses, no parameter selection based on ellipticity or historical ACSC outcomes, separate external theory-review sign-off |
| 5. Observations | [Data and negative-control reconstruction plan](OBSERVATIONAL_RECONSTRUCTION.md), plus synthetic independent spherical crossmatch fixture tests | Raw SDSS query provenance, sample and footprint, null mask/offsets, duplicates/redshift policy, leakage-free target and independent validation before preregistration |

## Success, failure and publication package

The three prospective contributions are **separable**:

1. **Mathematical-physics paper:** independently reviewed M1 insufficiency theorem, complete assumptions, exact witness and symbolic/numerical crosschecks, correction history and code, with strictly limited Szekeres–Szafron scope.
2. **Arithmetic-statistics paper:** controlled A01 plus independently executed and separately preregistered successors, full null realizations, reproducibility receipts, controls and all outcomes including non-rejection. A purely arithmetic signal is not a cosmic finding.
3. **Physical-prediction paper (conditional):** only after a P0/P1 parent supplies an independently derived mechanism, a prespecified observable and genuinely blind cosmological survey test. If every registered P0 candidate fails, **retire mechanism-level ACSC-v0.1 within P0-SF-v0.1**; retain negative theorem and arithmetic results.

For each manuscript deposit, the source package must contain: versioned LaTeX source + bibliography + accepted claim/limitation table; frozen hypotheses and deviations; exact commit/release DOI, source license and data hashes; environment lock; proof or analysis scripts; execution/replication logs and raw test values; ethical/review disclosure; figure-generation code; corresponding author and independent reviewer attribution. The source and result package is not made peer-reviewed merely by public code or arXiv submission.

## Nonpromotion controls

- No canonical registry row, controlled/physical support field, source pin, null protocol, parameter selection, science result or PR #78 review state is changed here.
- The new JAX calculation is an independent implementation **within the project**, not an external refereed proof.
- Existing surveys are **not** accessed in a controlled inference. Sky geometry fixtures are diagnostic only.
- Failed source identity, null mismatch or unapproved execution is **INELIGIBLE**, not negative scientific evidence.
- An honest incomplete paper may be methodologically publishable, but acceptance by Oxford Academic, arXiv moderation, or any journal cannot be guaranteed.

See [Charter-governed negative outcome standard](../../../docs/registries/NEGATIVE_RESULTS_PUBLICATION_PROTOCOL_v0.1.md).

## Literature (methods and context)

- Coley, Layden & McNutt (2019), *An invariant characterization of the quasi-spherical Szekeres dust models*, DOI [10.1007/s10714-019-2647-6](https://doi.org/10.1007/s10714-019-2647-6). Related invariant methodology; **does not review this particular pair**.
- Budavári & Szalay (2008), *Probabilistic Cross-Identification of Astronomical Sources*, DOI [10.1086/587156](https://doi.org/10.1086/587156). Association/uncertainty methodology, not this project's observed-match evidence.
- Delgado Gaspar, Sussman, McNutt & Coley (2021), *Comment on Szekeres universes with homogeneous scalar fields*, DOI [10.1140/EPJC/S10052-021-09113-9](https://doi.org/10.1140/EPJC/S10052-021-09113-9). Example of rigorous class-relative consistency scrutiny; distinct model.

**Review requirement:** an independent human reviewer must validate frozen Charter PDF, mathematical signs/normalizations, independence of candidate selection and terminal decision scopes on the actual final PR SHA before approving any scientific status transition.
