# Historical code log triage

The source collection at `historical/r&d/code_log/` preserves the complete supplied OneDrive code log folder, including final artifacts, earlier extraction-stage copies, and collection metadata. Individual code, notebook snippets, fences, and extracted text are copied byte-for-byte. No research code is executed or promoted into production.

The generated companions in `historical/r&d/code_log_triage/2026-10-03/` are separate from the preserved original source folder. CODE_TRIAGE.csv / JSON cover every final manifest artifact with its hash, source occurrences, source locators, extraction category, and disposition. PRESERVED_FILES.csv / JSON inventory every physical collection file, including earlier copies absent from final manifests. Earlier-copy source traces are recovered only through exact digests or exact text occurrences; unresolved upstream trace remains explicit and pending review.

All artifacts retain code_log_candidate status, historical_extracted origin, and pending_review review status. benchmark_evidence_status=superseded means only the located pre-correction arithmetic for y²=x³−1706x+6320 is superseded. Other curves, code behavior, and extraction fidelity remain unreviewed. AST parsing is only a prior syntax observation; it is not evidence validation.

The supplied corrected benchmark is N=150258963712, product(c_p)=2, Omega display 0.844725383566516, expected Sha=1. Existing Virgo.ipynb saved outputs corroborate those displayed numerical inputs; no calculation was rerun. Its final numerical test and bsd_period_normalization_test.py leave integer Sha certification unresolved. Sha=1 is not independently certified by this collection.

Both correction source files are separately preserved byte-for-byte at historical/r&d/code_log_triage/2026-10-03/correction_sources/ and digest-bound in CORRECTION_REFERENCES.json. They remain pending_review and are counted separately from the complete OneDrive folder intake.

The old half-period × Tamagawa4 product numerically equals full-period × Tamagawa2. Agreement of the resulting BSD RHS therefore does not validate its individual inputs. Period-dependent derived outputs require review/recomputation. Sources constructing [0,a,0,b,0] use different coefficient positions and are flagged model_mismatch / pending_review; short-model invariants are not substituted into those results.

EXISTING_REPO_TRIAGE records benchmark-specific historical script, notebook-cell and data-row locators without rewriting scientific code or historical saved outputs. No generic 587/1001057 replacement is performed. Named correction sources were found in /home/kepler; their paths, raw-file digests and saved-output locators are in CORRECTION_REFERENCES.json.

The original extraction coverage limits remain applicable: Drive hashes identify readable connector snapshots, not canonical binary files; PDF/OCR candidates can lose indentation or glyphs; the cloud-only Research-Analysis+Testing_pt.4.zip was metadata-only; omitted dependencies/media/plots remain recorded in the original manifests. Earlier copies with unresolved source traces are not counted as new confirmed extracted artifacts.

```json
{
  "final_manifest_artifacts": 8295,
  "final_source_occurrences": 27180,
  "final_artifact_status_counts": {
    "not_identified": 7938,
    "superseded": 108,
    "pending_review": 249
  },
  "final_model_mismatch_count": 7,
  "physical_files": 12633,
  "physical_bytes": 92754194,
  "physical_role_counts": {
    "earlier_extraction_copy": 4331,
    "collection_support_file": 7,
    "final_manifest_artifact": 8295
  },
  "physical_trace_counts": {
    "linked_to_complete_final_manifest": 2536,
    "recovered_from_readable_snapshot": 333,
    "collection_metadata": 7,
    "complete_final_manifest": 8295,
    "recovered_from_firstpass_manifest": 1462
  },
  "physical_old_arithmetic_scan_count": 12633,
  "physical_benchmark_status_counts": {
    "not_identified": 12065,
    "pending_review": 386,
    "superseded": 182
  },
  "earlier_copy_benchmark_status_counts": {
    "not_identified": 4120,
    "pending_review": 137,
    "superseded": 74
  },
  "correction_reference_files_preserved_separately": 2,
  "correction_reference_bytes": 84684,
  "existing_repo_files_triaged": 91,
  "existing_repo_status_counts": {
    "pending_review": 3,
    "mixed_scoped_dispositions": 1,
    "superseded": 87
  },
  "existing_repo_notebook_cells_triaged": 6,
  "research_code_execution_performed": false,
  "draft_only": false
}
```
