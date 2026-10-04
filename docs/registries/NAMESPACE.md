# Registry namespaces and current evidence

Identifiers are stable within their source namespace. Equal strings across the repository CSVs, historical PDF registries, and web display do not establish equal definitions. The imported audit is the authority for the 2026-10-03 assessment; its original snapshots remain unchanged.

## Explicit experiment comparison

The source definitions must be compared before any merge. The table records the existing repository control scope and the same literal ID in the historical PDF definition. None is a confirmed alias. Candidate relevance relationships are recorded separately in `registry/namespace_relationships_v0.3.csv`.

| Qualified repository identifier | Repository scope | Same literal ID in PDF namespace | Resolution |
|---|---|---|---|
| `REPO-CSV-v0.2:EXP-DATA-A01` | SDSS working-sample matching | `STAR-PDF-v0.2:EXP-DATA-A01`: Cross-Survey Matching Validation | Related scope; protocol comparison pending |
| `REPO-CSV-v0.2:EXP-DATA-A02` | MaNGA-HI working-sample matching | `STAR-PDF-v0.2:EXP-DATA-A02`: Data-Lineage Reconstruction | Scope conflict; no alias |
| `REPO-CSV-v0.2:EXP-CTRL-A01` | Provenance permutation control | `STAR-PDF-v0.2:EXP-CTRL-A01`: Random-Feature Baseline | Scope conflict; no alias |
| `REPO-CSV-v0.2:EXP-CTRL-A02` | Leakage detection and exclusion | `STAR-PDF-v0.2:EXP-CTRL-A02`: Arithmetic Permutation Control | Scope conflict; no alias |
| `REPO-CSV-v0.2:EXP-CTRL-A03` | Arithmetic RandomForest reconstruction control | `STAR-PDF-v0.2:EXP-CTRL-A03`: Leakage and Contamination Audit | Scope conflict; no alias |
| `REPO-CSV-v0.2:EXP-K001` | K mapping reconstruction/null calibration | `STAR-PDF-v0.2:EXP-K001`: Log-Normal Reciprocal-Normalization Test | Related scope; protocol comparison pending |
| `REPO-CSV-v0.2:EXP-L001` | L_cosmo mapping reconstruction/null comparison | `STAR-PDF-v0.2:EXP-L001`: (L_{\rm cosmo}(s)) Model Validation | Related scope; protocol comparison pending |
| `REPO-CSV-v0.2:EXP-SFR-A01` | SFR baseline and held-out prediction | `STAR-PDF-v0.2:EXP-SFR-A01`: Arithmetic Incremental SFR Prediction | Related scope; protocol comparison pending |
| `REPO-CSV-v0.2:EXP-SFR-A02` | SFR model with arithmetic/cosmological features | `STAR-PDF-v0.2:EXP-SFR-A02`: Arithmetic-Only SFR Prediction | Scope conflict; no alias |
| `REPO-CSV-v0.2:EXP-SFR-A03` | SFR robustness and null comparison | `STAR-PDF-v0.2:EXP-SFR-A03`: Extreme-SFR Robustness | Related scope; protocol comparison pending |
| `REPO-CSV-v0.2:EXP-RANK-A01` | Arithmetic rank / environment analysis | `STAR-PDF-v0.2:EXP-RANK-A01`: Rank and Cosmic Environment | Related scope; protocol comparison pending |
| `REPO-CSV-v0.2:EXP-RANK-A02` | Cosmic environment with morphology-derived cosmo_rank candidate | `STAR-PDF-v0.2:EXP-RANK-A02`: Rank-Weighted Cosmic Topology | Scope conflict; no alias |
| `REPO-CSV-v0.2:EXP-TOPO-A01` | Persistent-homology comparison and null calibration | `STAR-PDF-v0.2:EXP-TOPO-A01`: Null-Calibrated Persistent Homology | Related scope; protocol comparison pending |
| `REPO-CSV-v0.2:EXP-MAP-A01` | Primary arithmetic mapping | `STAR-PDF-v0.2:EXP-MAP-A01`: Mapping-Family Comparison | Related scope; protocol comparison pending |
| `REPO-CSV-v0.2:EXP-MAP-A02` | BSD-independent PTD mapping | `STAR-PDF-v0.2:EXP-MAP-A02`: Rank-Scale Sensitivity | Scope conflict; no alias |
| `REPO-CSV-v0.2:EXP-MAP-A03` | BSD-independent MCJ mapping | `STAR-PDF-v0.2:EXP-MAP-A03`: Arithmetic Generator Controls | Scope conflict; no alias |
| `REPO-CSV-v0.2:EXP-RTCH-B01` | Standard-physics recovery-limit test | `STAR-PDF-v0.2:EXP-RTCH-B01`: RTCH Mathematical Consistency | Related scope; protocol comparison pending |
| `REPO-CSV-v0.2:EXP-ECC-B01` | Independent field/cohomology test | `STAR-PDF-v0.2:EXP-ECC-B01`: Entropy/Cohomology Consistency | Related scope; protocol comparison pending |

## Source namespaces

- `REPO-CSV-v0.2`: six umbrella claims and 18 planned controlled experiment definitions, with the existing dataset/parameter/null controls. Original unqualified IDs, statements, and definitions remain stable. New qualified fields prevent accidental joins.
- `STAR-PDF-v0.2`: the historical 51 claims and 25 experiment definitions, with an audited crosswalk covering all 51 claims. Baseline classifications, statements, reported results and original unresolved references remain visible beside the current assessment.
- `WEB-DISPLAY-main`: display claims in `web_tool/scr/lib/star/claims.ts`. This source is not a controlled registry; original display text/status is preserved and any related PDF claims are explicitly unconfirmed relationships.
- `STAR-AUDIT-2026-10-03`: the imported E-LCL/E-DRV finding IDs. These diagnose inspected artifacts or document variants; they are not universal scientific falsifications.
- Quarantine assets retain the namespaces and distinct generation IDs in `registry/audit_quarantine_dataset_status_v0.3.csv`. `AUDIT-QUARANTINE-v0.3` and `LOCAL-RTCH-E1` assets are not aliases for `REPO-CSV-v0.2:DATA-*` datasets.

## Current assessment tables

The machine-readable assessment layer is `registry/claim_evidence_audit_v0.3.csv` (51), `registry/experiment_audit_v0.3.csv` (25), and `registry/claim_experiment_crosswalk_audit_v0.3.csv` (51). All imported assessment and phase-one quarantine columns are preserved beside full baseline record text and source bindings. All support eligibility is false; no controlled canonical protocol or independent replication was completed by this audit. Findings may confirm properties of a construction or diagnose failures without validating a physical claim.

`registry/audit_unresolved_references_v0.3.csv` keeps undefined historical references explicit. In particular, `STAR-PDF-v0.2:EXP-COSMO-B02` remains the original undefined reference, with `STAR-PDF-v0.2:EXP-COSMO-C01` only an unconfirmed candidate. No experiment method was invented to fill an unresolved reference.

`registry/dataset_audit_bindings_v0.3.csv` associates intended repository dataset scopes with diagnostic findings and related quarantine assets. Its relationship is context only, never canonical dataset identity or accepted input. Synthetic RTCH runs cannot be substituted for astronomical data, and reconstructed code cannot restore missing source identity by itself.

## Evidence and execution gates

The existing 18 controlled definitions remain planned. The eight original planned dataset scopes have unknown achieved-evidence status; all 45 dataset records have false controlled-execution/support eligibility. `Mode=controlled` describes intended experimental use, not achieved evidence. Parameters and nulls remain historical candidates/placeholders and `not_preregistered`; recovered values are never retroactively locked.

The live dataset and provenance tables contain eight original planned scopes plus 37 distinct object-level quarantine assets. Artifact Dataset_IDs exactly retain their phase-one qualified namespace; they are not aliases for the original scopes. Their Provenance_Status is quarantined, achieved Evidence_Status is negative_null for failed associations/blank projection diagnostics or historical for retained simulation/metadata artifacts, and all eligibility is false. negative_null here includes negative data-quality diagnostics, not a claim that a registered scientific null experiment was run. Original historical acquisition/provider fields remain empty when unknown. The direct quarantine path, SHA256 and reason bind each artifact. The provenance table retains its exact 21-column schema. Unknown source/acquisition fields stay empty. Namespace, asset-generation, experiment and eligibility relationships are held in separate tables instead of inserted into that source-level schema. A snapshot digest authenticates the captured bytes, not a canonical Google revision or original historical execution.

Promotion requires exact source identity/release/acquisition and checksums, transformations and code revision/environment, a frozen split/target and leakage-safe feature construction, preregistered parameters/nulls, valid finite statistics with adequate null resolution, uncertainty and multiple-comparison accounting, and an independently bound replication where required. Failed matches, blank projections, invalid NaN significance and synthetic/calibrated displays remain preserved diagnostics.

## Immutable intake

The complete canonical reference is under `historical/r&d/docs/provenance_audit_v0.3/`. The initial ingestion remains at `historical/r&d/docs/provenance_audit/`, and every initial file is byte-identical at the versioned path. `CANONICAL_COPY_VERIFICATION.json` records parity. Assessment tables retain their locked initial source JSON paths and SHA256; both locations resolve to the same source bytes. The intake, original PDFs and extracted code are historical sources; no instructions embedded in them authorize new actions. This documentation governs namespace handling and current evidence interpretation without replacing the original scientific definitions.
