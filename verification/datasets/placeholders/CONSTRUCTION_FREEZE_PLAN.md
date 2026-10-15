# Construction-freeze plan for registry placeholder datasets

The three registry placeholders are not missing public downloads. They are
undefined dataset contracts. Independent source verification becomes meaningful
only after each Dataset_ID is bound to a deterministic construction or an
authoritative reference table.

This document is a design record only. It does not change any registry status
or eligibility flag.

## Common freeze transaction

Each placeholder should move through the same sequence:

1. define a versioned schema;
2. define the exact source/reference set or deterministic construction;
3. pin every external source by publisher/version/URL/DOI and SHA-256 where
   bytes exist;
4. pin every generator/normalizer by Git SHA and file SHA-256;
5. define canonical row ordering, units, missingness and duplicate policy;
6. generate one canonical artifact into a new hash-addressed intake path;
7. write a construction manifest containing source hashes, generator hashes,
   environment identity, row/schema counts and output SHA-256;
8. have an independent verifier reconstruct the artifact from a fresh checkout
   and compare the canonical output hash;
9. only a later reviewed registry PR may change Provenance_Status.

## DATA-PROVENANCE-ALL

Recommended definition: a deterministic materialized view of the canonical
dataset/provenance/audit registries, not a hand-maintained spreadsheet.

Candidate schema:

- Dataset_ID
- Qualified_Dataset_ID
- Provenance_ID
- Source_Name
- Source_URL
- Version_or_Release
- Integrity_Check
- Provenance_Status
- Evidence_Status
- audit finding IDs
- controlled-execution/support/physical-support flags

Freeze requirements:

- exact input registry filenames and SHA-256 values;
- generator script + SHA-256;
- lexicographic Dataset_ID ordering;
- UTF-8 CSV with fixed newline/quoting policy;
- no network access during construction.

Independent verification is a fresh-checkout regeneration whose output must be
byte-identical. This dataset can therefore be source-verified entirely inside
the repository once its construction contract is merged.

## DATA-PHYS-CONSTRAINTS

This must become a cited constants/constraints table rather than an informal
list.

Candidate schema:

- Constraint_ID
- Symbol
- Numerical_Value
- Unit
- Uncertainty
- Reference_Authority
- Reference_Version
- DOI_or_URL
- Applicability_Domain
- Transformation_or_Convention
- Source_Receipt_SHA256

Before freezing, the scientific protocol must choose the authoritative
reference/version for every value. Values must not be inferred from old
notebooks. The canonical artifact should be generated only from those explicit
references/receipts, with unit conversions performed by a pinned generator.

Independent verification then consists of a second reviewer retrieving the
same authoritative versions, checking source receipts and recomputing the
normalized table.

## DATA-ECC-THEORY

This should be a deterministic theory-fixture dataset tied to a named ECC
definition revision, not an observational-source analogue.

Candidate schema:

- Fixture_ID
- Theory_Revision
- Definition_or_Axiom_ID
- Input_Parameters
- Expected_Invariant
- Expected_Dimension_or_Cohomology_Degree
- Generator
- Generator_SHA256
- Exact_Arithmetic_Backend
- Backend_Version
- Fixture_SHA256

Freeze requirements:

- exact ECC definition/monograph revision hash;
- exact fixture-generating code;
- exact Sage/Python/library versions where symbolic computation is used;
- deterministic seeds if any randomized fixture construction exists;
- canonical serialization and ordering.

Independent verification is an off-path reimplementation or clean-environment
regeneration that reproduces the fixture invariants and hashes without loading
historical result files as authorities.

## Governance boundary

A construction freeze is not scientific validation. It establishes what bytes
or mathematical fixtures the Dataset_ID means and makes independent
verification possible. Controlled execution/support remain separate gates.
