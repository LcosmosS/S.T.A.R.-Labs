# Charter-governed epistemic and implementation corrections v0.1

**Recorded:** 2026-10-08 (America/New_York)  
**Base inspected:** \`main\` at \`791c423514bd0d10c667c42106e55e41e445f09c\`  
**Status:** interpretive erratum and source-path audit; **not** a new theorem, controlled experiment, or support claim.

## Controlling authority and preservation

The authoritative scientific specification is [STAR Research Charter v0.2 (PDF)](../../charter/STAR_Research_Charter_v0-2.pdf). The shorter [Markdown summary](../../charter/RESEARCH_CHARTER_v0.2.md) is a navigation aid, not a replacement for the PDF's detailed sections. In particular, the PDF's §§1–3, 10–19, 26–30 and 32–37 govern scientific status, negative outcomes, and confirmation.

Historical \`OVERVIEW.md\`, \`2_STARMAP.md\`, \`3_SMAT.md\`, and \`4_SFT.md\` are **retained as historically proposed research visions**. Their original claims are not silently rewritten or upgraded. In any conflict, this correction and the controlling PDF determine how the historical text is to be read. Further changes to those theories require separately identified revisions and registry review.

The charter's **canonical epistemic categories** are:

| Code | Charter category | Interpretation |
| --- | --- | --- |
| D | Derived | Follows mathematically from stated assumptions/definitions; independent proof review remains an additional verification state |
| E | Empirical | Supported by a qualifying reproducible computation or observation under the applicable evidence requirements; scope must be stated |
| M | Model | Investigative mathematical/phenomenological construction |
| P | Postulate | Explicit assumption of a proposed theory |
| H | Hypothesis | Testable proposition under investigation |
| C | Conjecture | Broader proposition without proof |
| T | Testable prediction | Independently assessable consequence, not an observed success |
| S | Speculative interpretation | Interpretation without sufficient physical support |

Use **separate process/evidence tags** (not substitute epistemic categories): proposed, mathematically derived, symbolically checked, independently reviewed, preregistered, controlled-executed, independently replicated, and physically supported. These are *orthogonal* to D/E/M/P/H/C/T/S. An executable test, successful CI run, or symbolically checked equality is not independently proved or physically supported. The PDF's **success ladder** (§29, Levels 0–5) likewise remains distinct from both claim categories and experiment registry flags.

## Historical claim disposition (not a new canonical claim registry)

| Location and historical wording | Classification under PDF | Correction / minimum unresolved evidence |
| --- | --- | --- |
| \`OVERVIEW.md\`: the cosmos is predetermined by elliptic-curve arithmetic; constants and cosmic geometry arise of necessity | C/S, not D or E | Unestablished; charter §1 expressly rejects this as an assumption. Requires a fixed bridge and prospective independent astronomical tests |
| \`OVERVIEW.md\`: metric-preserving arithmetic-to-cosmic projection and inverse rank recovery | M/H/T, not a demonstrated bijection or isometry | Prove the claimed metric property or retract it; record degeneracies and isogeny structure; independently test inversion |
| \`OVERVIEW.md\`, \`2_STARMAP.md\`: arithmetic-weighted periods yield local/CMB Hubble rates and resolve Hubble tension | M/H/S | No completed preregistered, replicated Hubble-tension test. \`H_eff = H_0 × average(Omega_E)\` also needs dimensionally justified normalization and a causal/variational mechanism |
| \`2_STARMAP.md\`: projected maps reveal real filaments, voids, radiation, and CMB anomalies | H/T/S | Arithmetic point clouds are not observed sky maps; compare separately specified statistics with masked surveys and simulation nulls; persistent Betti numbers are not direct counts of physical filaments (§8) |
| \`2_STARMAP.md\`: isogeny flow, entropy dynamics, and repulsion preserve physical geometry | M/P/H | No established physical flow, conservation law, or metric-preservation theorem in the document |
| \`3_SMAT.md\`: arithmetic/entropy fields inform flight trajectories, link reliability, mission risk or ephemerides | M/T/S | Proposed mission-analysis architecture only; no validated trajectory engine, flight qualification, or operational predictions |
| \`4_SFT.md\`: entropy \`theta=dM\` gives a non-exact \`omega=dtheta\` | Inconsistent as stated | For global smooth M, \`d(dM)=0\` and \`[dM]=0\` in H¹; do not cite this as nontrivial H² evidence. Charter §26 instead specifies a *candidate* closed potentially non-exact target-space two-form and pullback; nonzero target class does not automatically imply nonzero pullback class |
| \`4_SFT.md\`: \`d omega=0\` guarantees \`nabla^mu T_munu=0\` | P/H, not D | Closure is not the field equations; conservation needs a specified action, stress tensor variation, compatible equations and Bianchi identities |
| \`4_SFT.md\`: derived expansion corrections \`a z+b z²\`, natural Hubble-tension solution | M/S | No demonstrated derivation with parameter/units consistency or blind physical confirmation; coefficients and reference limits must be defined first |

This crosswalk preserves the source's proposed content without asserting unsupported falsification of the whole research program. Formal changes to any claim's canonical support state belong in the relevant versioned registries and independent reviews, **not** in this interpretive document.

## Verified implementation-path crosswalk

Inspected against the base revision identified above; paths may change in subsequent PRs.

| Historical statement | What is actually present | Status |
| --- | --- | --- |
| \`2_STARMAP.md\` projection in \`src/acsc/\` and \`src/projection/\` | \`src/acsc/projection.py\` exists; \`src/projection/\` does not | Partially implemented; do not equate a Python projection with a validated physical sky reconstruction |
| TDA in \`src/tda/\` | \`src/tda/\` exists | Software present; physical correspondence untested |
| Symbolic regression in \`src/symbolic_regression/\` | Directory exists | Exploratory tools, not demonstrated symbolic physical law |
| \`notebooks/hubble_tension_fit.ipynb\` | Does not exist in the canonical \`notebooks/\` directory | Historical pointer; not a runnable canonical validation |
| \`src/blender/\` and \`src/visualization/\` | Both directories exist | Visual or exploratory capability only |
| \`3_SMAT.md\` core in \`src/smat/\` or \`smat/\` | Neither directory exists | Proposed architecture, not implemented claim |
| \`notebooks/smat_prototype.ipynb\` | Not present in the canonical \`notebooks/\` directory | Historical pointer |
| \`src/pipeline/\` | Exists | No demonstrated SMAT integration from directory existence alone |
| Controlled notebooks | \`notebooks/00_registry_overview.ipynb\` through \`08_robustness.ipynb\` | Charter § controlled-notebook policy applies; individual CI passes are not physical support |

## Theory and experiment boundaries

1. Arithmetic curve invariants (conductor, discriminant, rational rank) do **not** arise automatically from elliptic-function solvability of general-relativistic evolution equations. A new physical derivation is required to connect them.
2. \`M1-INH-E1\` is a class-relative question about sufficiency of the *registered* elliptic evolution record. Its mathematical evidence needs independent verification; success limits sufficiency in the registered Szekeres–Szafron class, not all elliptic cosmology.
3. \`EXP-MAP-A01\` is a fixed, arithmetic-only rank-permutation test. Null rejection would not establish cosmic correlation, physical support, or BSD. Non-rejection is not proof of absence of every possible arithmetic effect.
4. \`P0-SF-v0.1\` is a finite, operationally closed five-candidate search frame. Exhaustion may justify scoped retirement but not a universal no-go theorem.
5. ECC and RTCH remain candidate theories; see [ECC/RTCH recovery gates](../../research/gates/ECC_RTCH_RECOVERY.md) and Charter §§25–27. A synthetic torus or recovered conventional limit cannot alone supply new physical support.
6. Historically invalid SDSS/H I matches and exploratory SFR scores do not become eligible by relabeling or documentation changes; original source provenance, leakage controls and independent replication are still mandatory.

## Corrections and versioning

- Leave earlier versions, failed calculations, historical claims and audit records accessible, with exact source references.
- If a physical or mathematical claim is reformulated, create a separately identified revision and new preregistration where the fixed hypothesis would otherwise be altered.
- Use [Negative Results Publication Protocol v0.1](NEGATIVE_RESULTS_PUBLICATION_PROTOCOL_v0.1.md) for terminal, reviewable positive **and negative** result reports.
- This document does **not** change registry status, controlled-execution eligibility, source hashes, frozen protocols, or reviewer approvals.
