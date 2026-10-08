# CoCalc historical archive: independent receipt, review and quarantine gates
**Date:** 2026-10-08. **Governing authority:** `charter/STAR_Research_Charter_v0-2.pdf`.
**Classification:** historical source recovery, not source-release admission, controlled experimentation, preregistered validation or claim support.

## Directly inspected new uploads and archive
The researcher supplied an original conversational upload named `star_provenance_cocalc.zip`. The ZIP was inspected **without extracting or executing any member**. The original archive bytes must be retained intact, and a reviewer must independently check the digest against any Dropbox or historical copy before asserting byte identity.

| Source | Observed SHA-256 of uploaded bytes | Verification boundary |
| --- | --- | --- |
| `star_provenance_cocalc.zip` | `cf7d21d34b2f1fb01a6cd04e584eb0fb5b7078168cc80e5afd9e648b3cfdd98d` | Local upload checksum only; no upstream scientific lineage accepted |
| `STAR_Experiment_Crosswalk.pdf` | `ae22f956e36d1d66c84435c942794268e129bce1f6c7e3f69f1c8d4e2b5fc22f` | Historical STAR-PDF namespace |
| `STAR_Experiment_Registry_v0-2.pdf` | `6145d6878410e934c577fcdac7d90a18314b86cb7ea7b55af73903e045838992` | Historical STAR-PDF namespace |
| `STAR_Claim_Evidence Registry_v0-2.pdf` | `27a3ae4b95077ace559f105a9712ce91f46d46934942aa752edf6ed925c1ba94` | Historical STAR-PDF namespace |
| `S.T.A.R._Prepublication_Live_v0.1.docx` | `1b4acdccc35902d5985b7fd825788ac4ba994e13f59746687dde5b92b4df5e34` | Compiled manuscript; reports R&D and failures but is not independent replication |

The PDF and DOCX SHA values identify **the specific user-provided attachment bytes**. Google Drive contains title-corresponding native Google Docs for the v0.2 crosswalk and registries, but a title match does not establish binary identity to a PDF. Their textual high-level experiment definitions align; these Google Docs are not a substitute for source digests.

Archive contents: **196** entries; 97 `.py`, 77 `.csv`, 5 `.ipynb`, 8 `.png`, 5 `.log`, 2 nested `.zip`, 1 `.txt`, 1 `.partialupload-...`. Total uncompressed size ~114.76 MB. Members have no path traversal, absolute names or unsafe archive paths in this inspected ZIP; nested ZIPs **were not recursively trusted**.

Seven historical Python files fail syntax parsing under the review environment: `untitled4.py`, `untitled3.py`, `untitled55.py`, `untitled33.py`, `untitled11.py`, `untitled32.py`, `untitled20.py`. These failures remain negative provenance evidence, not files to auto-repair while claiming historical identity. All five notebooks contain prior execution outputs; retain originals immutable, and never count their printed results as controlled experiments.

The 71,597,692-byte entry `GalSpecExtra.csv.partialupload-wGpu9DYAMr` (SHA-256 `06acdaee0f046ee8d338ccfeee972c355e684596caaf5c9978b88e1cd878831b`) is **quarantined and never treated as `GalSpecExtra.csv`** without a complete independent source acquisition. `Paradox.ipynb` is 6,803,488 bytes with historical outputs; source member SHA-256 `8511df5b3d9d347a38372343a0ad6ad8eda422ea2971796d743fccd4ad407950`, not a controlled notebook. `ACSC-GLMPCT.zip` SHA-256 `d7e7b35ca6ab00e6ef50d234039007dfc8b1e6a3eb30f322da9ca34aedd95a40` is nested and has not been safely enumerated here.

Important script receipts:
- `acsc_ecc_hierarchy.py` SHA-256 `43bf47b111c3c842b3e44e98b7f5b428752d710d9cc3a80431435e5b1afe9c46`
- `first_principals.py` SHA-256 `f986b7dc0b211da67173105cee9f9f6dd382d838d788f2c0f0bf7738aaa68039`
- `2lmfdb.py` SHA-256 `b95af2f07da48b0bcd65225cebc95a732ed06b1e1bb876d18c5be777dee72eda`

The new `scripts/audit_cocalc_archive.py` produces an exact per-member SHA-256 JSON inventory. It checks for duplicate member names, unsafe paths, symlinks and size limits and inspects Python syntax and notebook output presence without executing code. Its output classification is always quarantine/unknown and its science/support booleans are always false. It does **not** prove an archive was created on a stated historical date or that an old notebook's published outputs are correct. Test fixtures cover these trust boundaries.

### Reproduction
```sh
python scripts/audit_cocalc_archive.py \
  /path/to/star_provenance_cocalc.zip \
  --output /tmp/star_cocalc_inventory_v1.json
pytest -q tests/test_audit_cocalc_archive.py
```
Do not auto-upload extracted CSVs, activate historical notebooks, or create Git LFS pointers from JSON receipts. A large original source file must be ingested as **real uploaded Git LFS bytes** on a separately reviewed branch with an independently verified object ID and working pointer hydration before any controlled use. Check a raw archive copy against its recorded SHA first; Dropbox file naming and reported size alone are insufficient.

## Critical ID/experiment-naming collision (not a contradiction that may be silently fixed)
The independently uploaded `STAR_Experiment_Registry_v0-2.pdf` and native Google Drive experiment registry describe **`STAR-PDF-v0.2:EXP-MAP-A03` as Fibonacci/Lucas-vs-other arithmetic-generator controls**. PRs #62 and #65 prospectively propose an **MCJ j-invariant rank-coherence** experiment under `REPO-CSV-v0.2:EXP-MAP-A03`. Neither specification can overwrite the other; the repository's namespace resolution must explicitly retain both original names and meanings.

Likewise `STAR-PDF-v0.2:EXP-MAP-A01` is broad mapping-family comparison, while `REPO-CSV-v0.2:EXP-MAP-A01` has an explicitly different, locked source, projection and primary statistic. `EXP-CTRL-A02` also carries different roles across documents. Protect explicit qualified IDs, and reject unqualified claims/registrations where collisions exist. These are historical/specification differences, not controlled experimental outcomes.

## Admission and PR gates
- [ ] Second reviewer recomputes raw archive and key member SHA-256 on an independent host and compares the actual Dropbox ZIP bytes (its copy was located by title) to the uploaded archive.
- [ ] Inventory **every** member with the installed auditor; reconcile names and hashes with `historical/r&d/docs/recovered_corpus_audit_2026-10-08`, preserving duplicates and all negative artifacts.
- [ ] Review nested ZIPs and historical notebooks in an isolated environment. Notebook outputs are prior artefacts, not allowed controlled reruns. Never execute unreviewed ZIP code in a production CI or notebook job.
- [ ] Record actual CasJobs SQL/release/job/export link; the recovered `SELECT TOP 200000` query includes STAR-class and negative-redshift rows, so no galaxy-only claim may be inferred.
- [ ] Acquire complete source `GalSpecExtra.csv` independently, with release/authorship/integrity receipt; quarantine the `.partialupload-` entry as irrevocably incomplete for controlled input.
- [ ] Independently review source ID meaning and original parameter/null definitions before promoting any candidate; preserve `REPO-CSV` versus `STAR-PDF` namespaces.
- [ ] Pass source and transformation CI on **actual selected bytes**, not filenames, file sizes or rendered PDFs. Only then consider a separate versioned dataset-registry update (never automatic support promotion).
- [ ] For sky overlays, a reviewed coordinate table's SHA proves display bytes, while upstream verification is an independent acquisition gate; controlled claim support requires preregistered tests and independent replication.

## Status and source-integrity pledge
This PR contains only a safe verifier, deterministic tests and this classification docket. **No original ZIP, CSV, notebook, plot or LFS object is committed here; no expired ChatGPT attachment is claimed re-uploaded.** `DATA-SDSS18-200K` and `DATA-MANGA-HI-ALL` retain unknown provenance pending independent acceptance. A01 and A03 frozen science decisions and all support flags remain untouched. Refer to independent review PR #69 and controlled A01 Issue #67.
