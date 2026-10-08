# M1-INH-E1b — candidate constructive-pair evidence

**Authority:** [governing research charter PDF](../../../charter/STAR_Research_Charter_v0-2.pdf) (repository-relative link from this folder: see absolute link below), [charter v0.2 text](../../../../charter/RESEARCH_CHARTER_v0.2.md), and frozen [M1-INH-E1 protocol](../../protocol.md).

**Governing PDF:** [STAR_Research_Charter_v0-2.pdf](https://github.com/LcosmosS/S.T.A.R.-Labs/blob/main/charter/STAR_Research_Charter_v0-2.pdf). The PDF is authoritative if a summary or accompanying record differs.

**Evidence classification (descriptive, not registry status):**
\`METRIC_FIRST_SYMBOLICALLY_REPRODUCED — EXTERNAL_REVIEW_AND_GENERAL_E1a_PENDING\`.

## Included artifacts

- \`m1_inh_e1b_metric_first_audit_v4.py\`: canonical metric-first SymPy verifier.
- \`m1_inh_e1b_metric_first_audit_v4.json\`: preserved local certificate, generated using SymPy 1.14.0. Check the embedded source SHA-256 before relying on it.
- \`M1-INH-E1b_metric_first_proof_record.md\`: mathematical exposition of the explicit pair, regular domain, metric-first curvature, shear projector, invariant and boundaries.
- \`execution_provenance.md\`: verbatim user-reported command outputs, the four distinct source hashes, and previously encountered notebook failures.
- \`E1a_handoff.md\`: next required **general** Einstein-to-Weierstrass reduction, not a completed result.
- \`development-history/\`: earlier verifier variants and their historical certificates, retained for provenance only; four passing versions are *not* four independent scientific replications.

## Reproduction

From the repository root, in a disposable checkout, run:

\`\`\`bash
python -m pip install 'sympy==1.14.0'
python preregistrations/M1-INH-E1/evidence/metric-first/m1_inh_e1b_metric_first_audit_v4.py
sha256sum preregistrations/M1-INH-E1/evidence/metric-first/m1_inh_e1b_metric_first_audit_v4.py
\`\`\`

Expected SHA-256:

\`\`\`text
10ccfa264f475fd7bd6d490c80c8862a174730567ee51c0d759b87939b93e6bb
\`\`\`

The script writes a JSON certificate beside its source when invoked as a file. **Do not confuse the repository's preserved certificate with a fresh run**; retain new execution logs separately and compare the source hash. It uses exact SymPy simplification rather than a numerical tolerance. The generic Ricci tensor is constructed before substitution; rotational reduction to the meridian occurs after differentiation in both transverse coordinates. Spatial embedding checks are separate from the Ricci calculation. Positive density is proved by domain inequalities rather than inferred from a single sampled point.

## Scientific boundaries

The candidate pair uses common \(M=1+z,\ K=0,\ f=z,\ \Lambda=3\), expanding-branch data and nonzero Weierstrass discriminant, with spatial sectors \(A=C=1/2\) and \(A=e^z/2,\ C=e^{-z}/2\), respectively. Both satisfy the frozen constraint. A curvature-derived dust density and a shear-projector invariant distinguish the solutions on an open domain.

This work is a **class-relative field-level obstruction candidate**, not a general GR+dust no-go theorem. It does not complete E1a, does not test an E1c observable, does not change P0-T001, and grants no ACSC mechanism, controlled-execution or physical support.

**Frozen protocol and registries are not modified by this evidence-only PR.** The October-3 audit snapshot is unaffected. External mathematical review and completion of general E1a remain prerequisites for any gate change.

### Imported-record clarification

The preserved proof record was authored before the canonical v4 naming and describes a development-stage Gram expectation correction. Consult \`execution_provenance.md\` for the later notebook coordinate-identity failures, and use **v4** as the reproducible entry point. This README does not retroactively rewrite that historic document.
