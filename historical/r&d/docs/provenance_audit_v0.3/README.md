# S.T.A.R. provenance audit — October 3, 2026

[Certain] The reviewed evidence contains material provenance and validation failures. The two inspected SDSS/HI match tables fail their stated angular tolerance; blank packaged projection outputs disagree with their adjacent manifests; synthetic demonstrations and globally preprocessed models do not establish independent empirical validation.

This is an evidence audit, not an independent execution of the research program. It records 20 findings: 16 local diagnostics and four targeted Drive documentary findings. Original research sources were preserved. Document directions were treated as research text; the user-requested Research Charter governed the audit interpretation.

## Updated registries

| Registry | Current records | Live document | Local PDF |
|---|---:|---|---|
| Claim/Evidence | 51 claims | [Open updated Google Doc](https://docs.google.com/document/d/12lTW636WXBJLbhsEhk5Zg5tRsfErnIgoZQRzP1NXTxc/edit) | STAR_Claim_Evidence_Registry_v0-3.pdf |
| Experiment | 25 canonical experiments | [Open updated Google Doc](https://docs.google.com/document/d/1c5rBqlaxPRYN4PwsYI8xXKQ0JelFBNjds30OPUj6Xms/edit) | STAR_Experiment_Registry_v0-3.pdf |
| Crosswalk | 51 claim rows | [Open updated Google Doc](https://docs.google.com/document/d/1hEcMq4nBUn0BxNJHi6dOblBHoIH2LJJangwiZl0e_Fw/edit) | STAR_Experiment_Crosswalk_v0-3.pdf |

Each live document retains its original baseline and now includes a current audit note and complete supplement. Every original native structural block was verified unchanged except shifted indices. The revised registry PDFs place the current supplement first and retain all 143 original registry pages afterward. Every retained PDF page content stream was verified identical. Ten original crosswalk experiment references remain unresolved; candidate aliases are unconfirmed. No experiment was silently marked complete or independently replicated.

## What to read

- **STAR_Provenance_Audit_v0-3.pdf** — readable findings, source locators, hashes, coverage and interpretation limits.
- **claim_updates.csv/json**, **experiment_updates.csv/json**, **crosswalk_updates.csv/json** — current per-record assessments and linked findings. The crosswalk JSON also contains unresolved reference records.
- **baseline_claims.json**, **baseline_experiments.json**, **baseline_crosswalk.json** — convenience copies of original definitions/relationships; original PDFs govern mathematical glyphs and complete layout.
- **local_findings.json/md**, **drive_findings.json/md** — detailed evidence, exact locators and interpretation limits. Local findings also include 10 selected dataset provenance records.
- **registry_consistency.json**, **native_registry_verification.json**, **pdf_verification.json** — completeness, source-preservation and render checks.
- **local_inventory.csv**, **local_csv_profiles.json**, **local_scope_exclusions.json** — 14,361 inventoried local files, 2,126 selected full-file inventory digests, 280 CSV profiles (242 full-table and 38 sampled). Profile/hash coverage does not certify every data value or historical execution.
- **drive_provenance_records.json** and **drive_text_snapshots/** — 288 readable Drive snapshots and digests. These snapshots precede the registry updates. The package-relative snapshot paths allow the saved bytes to be checked later.
- **controlling_sources.json** — exact hashes of the four supplied governing PDFs.
- **local_code_manifest.json**, **drive_code_manifest.json**, **code_extraction_summary.json**, **image_ocr_manifest.json** — extraction provenance and review flags.
- **deliverable_sha256.csv** — package-file digests, excluding the digest manifest itself.

## Extracted code

Open [the OneDrive code log](../code%20log/2026-10-03/README.md). It contains 8,295 saved artifacts: 603 raw scripts, 478 notebook cells and 149 explicit code fences, plus 7,065 document/OCR candidates separated for source review. Exact duplicates are deduplicated within each source class; 80 identical digests occur across the local/Drive classes with both source records retained. The manifests record 27,180 source occurrences.

All 8,295 saved code hashes were checked. 2,084 Python artifacts parse; parsing is not execution, dependency verification, scientific validation or replication. No extracted research code was executed. OCR candidates remain uncorrected and may contain indentation or glyph errors.

## Coverage limits

[Certain] The audit inventoried 14,361 local files and 291 accessible Drive root assets, including 288 readable document snapshots, an empty folder and two untranscribed media files. Semantic review prioritized the controlling claims and selected evidence; it did not independently verify every statement or all 68.4 GB of inventoried content.

116 OneDrive entries were retained as metadata only, including 89 CSVs. Some large cloud-backed files stalled during recall. The 4.1 GB Research-Analysis+Testing_pt.4.zip could not be read; 35 accessible ZIPs were inspected. Selected archive-member bytes are hashed, but some large containers lack whole-container digests. Dependencies, runtime/cache, credentials and third-party vendor code were excluded with recorded paths.

Drive binary/export downloads returned HTTP 403; complete readable connector snapshots were used. Their hashes identify fetched UTF-8 text, not canonical provider binaries, revisions, authorship or historical run inputs. Available revision history was inspected for four selected documents, not every source. Native Google Docs content/structure and native citations were verified through connector readback; their visual rendering was not verified. All 64 new local PDF pages were rendered and visually inspected.

[Certain] The most urgent research repairs are to rebuild and validate catalog matching, bind exact data/code/environment versions, reconstruct fold-local predictive pipelines, and replace invalid or underpowered null evidence with registered controls. The audit itself confers no new controlled, predictive or physical evidence.
