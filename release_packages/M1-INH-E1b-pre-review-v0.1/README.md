# M1-INH-E1b pre-review proof package v0.1

**Purpose:** frozen external-review target for the candidate class-relative M1-INH-E1b insufficiency theorem.
**Source PR:** #81.
**Source commit before package assembly:** `8c589c3c82f3fb946a027c02db5799228dda5ff3`.
**Evidence state:** exact symbolic certificate reproduced; external independent proof review pending.
**Registry effect:** none. This package changes no protocol, experiment eligibility, theory status, support flag, or physical-support claim.

## Contents
- `M1-INH-E1b_submission_bundle_v0.1.md` — theorem statement, exact domain/conventions, scope limits, replication invitation.
- `m1_inh_e1b_metric_first_audit_v4.py` — canonical metric-first SymPy verifier.
- `m1_inh_e1b_metric_first_audit_v4.json` — preserved verifier certificate.
- `M1-INH-E1b_metric_first_proof_record.md` — full proof record and invariant argument.
- `execution_provenance.md` — execution provenance, including retained negative notebook history.
- `M1-INH-E1b_submission_bundle_v0.1_reader.pdf` — optional Pandoc-rendered convenience PDF for human reading only; non-canonical and deliberately excluded from `SHA256SUMS`.
- `SHA256SUMS` — SHA-256 digest of every substantive, hash-locked component.

## Optional reader PDF

`M1-INH-E1b_submission_bundle_v0.1_reader.pdf` is generated from the canonical Markdown submission bundle with Pandoc for **human reading only**. It is a convenience rendering, **not part of the hash-locked certificate**, is deliberately **not listed in `SHA256SUMS`**, and must **not replace or supersede the Markdown sources**. If the PDF and Markdown differ, the Markdown source controls.

Generation command used by this branch:

```bash
pandoc M1-INH-E1b_submission_bundle_v0.1.md \\
  -f markdown+tex_math_single_backslash \\
  --pdf-engine=pdflatex \\
  -V geometry:margin=0.85in \\
  -V fontsize=10pt \\
  -V colorlinks=true \\
  -V linkcolor=blue \\
  -V urlcolor=blue \\
  -o M1-INH-E1b_submission_bundle_v0.1_reader.pdf
```

The PDF may be regenerated or replaced for readability without changing certificate identity. Only the canonical Markdown, verifier/certificate/proof/provenance sources, and their recorded hashes define the locked review artifact.

## Canonical verifier
`10ccfa264f475fd7bd6d490c80c8862a174730567ee51c0d759b87939b93e6bb`  `m1_inh_e1b_metric_first_audit_v4.py`

The verifier hash above independently recomputes to the SHA-256 embedded in the canonical certificate.

## Scope lock
This package is **not** M1-INH-E1a; **not** M1-INH-E1c; **not** a terminal P0-T001 failure; and **not** physical ACSC support, cosmological correspondence evidence, BSD proof, or experimental activation. Public circulation, a repository tag, an archive deposit, or a rerun of the same source does not constitute external mathematical review.

## Independent review request
Re-implement from the two explicit metric tensors without importing the supplied Einstein tensor, density, shear eigenspace, or invariant. Check all Einstein-tensor components and sign conventions, full positive-density regularity domain, complete frozen elliptic branch record, curvature reconstruction of dust/shear structures, and the zero-versus-positive invariant obstruction. Publish source, environment, exact hashes, failures as well as successes, and a scoped verdict. Counterexamples and falsification are explicitly solicited.

Any future registry promotion remains governed by the separate independent-review process on `main`; this package cannot satisfy or bypass that gate.
