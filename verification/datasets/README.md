# Independent dataset verification v0.1

This package inventories the nine canonical `DATA-*` records and provides
independent source-reconstruction procedures without changing canonical
provenance or scientific eligibility.

## Census

At the branch base there are **9 canonical datasets**.

- **4 have canonical provenance `unknown`** and need source/construction
  verification before they can be considered source-verified:
  `DATA-SDSS18-200K`, `DATA-PROVENANCE-ALL`,
  `DATA-PHYS-CONSTRAINTS`, and `DATA-ECC-THEORY`.
- **4 additional external observational datasets have publisher/source bytes
  marked `verified` but still need a separately recorded off-author
  re-verification/review receipt**:
  `DATA-MANGA-HI-ALL`, `DATA-SFR-MANGA-PIP3D`,
  `DATA-VIZIER-ALFALFA100`, and `DATA-COSMIC-ENV`.
- **1 dataset, `DATA-ARITHMETIC`, is already source-locked with controlled
  provenance** at a pinned JohnCremona/ecdata commit. Its later independent
  controlled-result reproduction is an experiment-level gate, not a missing
  dataset-source gate.

Thus **8 of 9 canonical datasets still need some dataset-level independent
verification/review work**, while only **4 of 9 currently lack verified source
provenance outright**.

This distinction is intentional. A publisher-byte hash can be verified without
the scientific transformation, selection, join, target definition, or result
being independently reproduced.

## Public-source methods

### SDSS DR18 200k — CasJobs

The historical 18-column sample is preserved with SHA-256
`9dca2008683fde4b0f7a90af5de85ee846a30a47f6f6fae3968c83dea06fa5d2`.
The recovered terminal SQL is stored verbatim in
[`casjobs/DATA-SDSS18-200K_historical_recovered.sql`](casjobs/DATA-SDSS18-200K_historical_recovered.sql).

The historical query has `TOP 200000` and **no `ORDER BY`**. Therefore a
fresh CasJobs execution cannot reproduce exact row membership. The independent
verification target is instead:

1. DR18 context and table/view availability;
2. exact 18-column schema;
3. the `PhotoObj` → `SpecObj` join on `s.bestobjid=p.objid`;
4. the recovered magnitude predicates;
5. row count and data-type sanity;
6. class/redshift distributions;
7. overlap of `(objid,specobjid)` pairs with the frozen historical CSV.

The deterministic probe SQL adds an explicit `ORDER BY p.objid,s.specobjid`\nfor repeatable current-DR18 comparison. It is **not** the historical dataset\nand must never replace the frozen source. Both executable probe/rerun recipes\nclear their MyDB destination tables first; the archival recovered SQL remains\nunchanged as provenance evidence.\n\nA separate `DATA-SDSS18-200K_membership_backcheck.sql` supports a stronger\nrow-level check: upload the frozen `(objid,specobjid)` pairs to\n`mydb.STAR_SDSS18_200K_IDS`, then verify that all pairs resolve through the\nDR18 `PhotoObj`/`SpecObj` relation and satisfy the recovered magnitude\npredicates. Passing that check establishes membership in the reconstructed\nquery-defined population at the checked DR18 context; it still does **not**\nrecover the original unordered `TOP 200000` selection decision, job ID, or\nexport checksum.\n
Current SDSS documentation describes DR18 SkyServer as using the BestDR18
database and exposes CasJobs for long asynchronous SQL jobs. Reviewers should
record the actual CasJobs context, job ID, submission/completion timestamps,
query text, export format, and exported-file SHA-256 in their receipt.

### ALFALFA alpha.100 — VizieR VOTable

The independent request is frozen in
[`vizier/DATA-VIZIER-ALFALFA100_request.json`](vizier/DATA-VIZIER-ALFALFA100_request.json).

A reviewer should re-fetch the complete corrected table directly from CDS
VizieR and verify:

- 31,502 rows;
- 25 fields;
- required field names and coordinate metadata;
- unique nonblank AGC IDs;
- 344 rows with both optical counterpart coordinates absent;
- H I quality counts 25,434 / 6,068;
- raw SHA-256 when the service emits byte-identical VOTable serialization.

If raw bytes differ but semantic invariants agree, the receipt must report the
hash mismatch and preserve the newly fetched bytes. It must not silently call
the old raw hash verified.

### Other SDSS/MaNGA publisher datasets

`DATA-MANGA-HI-ALL`, `DATA-SFR-MANGA-PIP3D`, and
`DATA-COSMIC-ENV` have direct publisher URLs and registered SHA-256 values.
The verifier can independently re-download these public FITS objects and
compare their bytes. This confirms source identity only; it does not approve
sample selection, joins, SFR targets, environment definitions, nulls, or
results.

### Internal/theory placeholders

VizieR and CasJobs are not appropriate for `DATA-PROVENANCE-ALL`,\n`DATA-PHYS-CONSTRAINTS`, or `DATA-ECC-THEORY`. They need an explicit\nconstruction/schema/reference package first. Until then they remain blocked\nrather than being assigned fabricated public sources. The proposed freeze\ntransaction and dataset-specific schema contracts are documented in\n[`placeholders/CONSTRUCTION_FREEZE_PLAN.md`](placeholders/CONSTRUCTION_FREEZE_PLAN.md).\n
## Commands

Static census and governance check:

```bash
python scripts/independent_dataset_verification.py --format markdown
```

Live public-source verification (VizieR plus direct publisher URLs):

```bash
python scripts/independent_dataset_verification.py \
  --live-public-sources \
  --receipt-out results/independent_dataset_verification.json
```

After an independent reviewer runs one of the CasJobs SQL files and downloads
the CSV:

```bash
python scripts/independent_dataset_verification.py \
  --casjobs-export /path/to/export.csv \
  --casjobs-mode deterministic-probe \
  --receipt-out results/casjobs_receipt.json
```

For a rerun of the historical SQL, use `--casjobs-mode historical-rerun`.
Neither mode is permitted to promote the canonical registry automatically.

## Governance boundary

This PR adds verification machinery and a census only. It does **not**:

- change `Provenance_Status` or `Evidence_Status`;
- change execution/support eligibility;
- claim the historical CasJobs membership is reproducible;
- admit ALFALFA to a web release;
- validate any cross-match or SFR/environment analysis;
- create a controlled scientific result.

A later, separately reviewed PR may ingest signed/off-author verification
receipts and propose registry changes.
