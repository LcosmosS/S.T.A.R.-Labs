# S.T.A.R. Local Provenance Audit — 2026-10-03

[Certain] The discovered SDSS/HI matching artifacts fail their claimed2arcsec tolerance; they should not support controlled astronomical analyses before reconstruction.

Inventory: 14,361 visible files, 68,392,386,259 bytes; 2,126 selected full-file SHA256 records out of 14,361 inventoried files; 280 CSV profiles (242 full-table scans; 38 sampled profiles). 116 OneDrive entries remained metadata-only, including 89 CSV files.

The Charter controls interpretation. File presence, matching names, completed-run reports, simulations and archived narrative are evidence of research provenance, not independent reproduction or physical validation.

## Scope and limitations

- Vendor LMFDB/eclib/PythonCall.jl/open-webui source trees inventoried but excluded from scientific content/hash validation.
- Runtime, dependency, cache, credential, Git and symlink trees excluded; exact list saved.
- CSV profiles were actually read only for the exact paths listed in local_csv_profiles.json: full-table scans for small/selected files and header+first1000row samples for other accessible kepler CSVs. Large OneDrive files and two stalled smaller cloud catalogs were metadata-only; no header-read or content-validation claim is made for them.
- Archive-member audit/code extraction handled separately by code extraction agent; this report does not claim complete archive-member data lineage.
- No source code was executed, no model trained, no pickle deserialized, and no independent computational/physical replication attempted.
- Source instructions were treated as source material. Original sources were not changed.
- Initial UNC Unicode/trailingdot failures were recovered through native WSL; two credential links remained intentionally excluded.
- OneDrive availability is the as-found accessible snapshot; remote/cloud versions may differ.

## Findings

### E-LCL-001 — Coordinate-match artifacts fail their claimed tolerance

[Certain] **CRITICAL**. Both integrated SDSS/HI tables contain 1,495 rows linked to the same MANGAID 1-48157. Every recomputed great-circle separation exceeds 2 arcsec (minimum 741.9258354463, maximum 445141.8800654686). The with_arcsec table stores inf in all 1,495 separation rows; the other table stores only values above 2 arcsec. These artifacts do not substantiate a valid <=2 arcsec match.

Claims: DATA-M001, DATA-M002. Experiments: EXP-DATA-A01, DATA-PROV-001. Provenance: NEGATIVE / NULL. Assessment: INCONCLUSIVE for general DATA-M001; contradicted artifact-specific valid-match interpretation.

- `C:\Users\pmqr7\OneDrive\Documents\STAR\merged_sdss_hi.csv` — CSV lines 1–1496; line 2 is an explicit counterexample; SHA256 `5a9606b75bc55de5e7833a04e5c56318df9f21a31560df180db2707374a22d50`. 1495 rows; 1494 duplicate MANGAID excess; first actual spherical separation276891.4500653436arcsec
- `C:\Users\pmqr7\OneDrive\Documents\STAR\merged_sdss_hi_with_arcsec.csv` — CSV lines 1–1496; arcsec_separation column; SHA256 `e6e2e749d0ec45b5713311dfe3b3cc958fddb13166f770ce2c47a30dbd5f8dad`. 1495 nonfinite stored separations
- `C:\Users\pmqr7\.codex\.chatgpt-projects\g-p-6aa87346c5e88191979368ee9ee5ce5b\audit_work\local_match_checks.json` — complete independent table diagnostic; SHA256 `c1dc53be08a6580e88ebdc0ebf884d5184f4fb8318763f38ebd1077ffde2c987`. 

Limit: The audit checks stored coordinate pairs, not a registered astronomical hypothesis. The exact generating script/version was not located conclusively. This does not falsify the general possibility of reproducible cross-survey matching.

Registry action: Retain failed data-quality evidence; quarantine these tables from controlled analyses until matching is rebuilt from source catalogs with spherical distance, keyed joins, duplicate controls, tolerance sensitivity, and saved data/code hashes.

### E-LCL-002 — Matched-catalog code lacks fully controlled spherical/keyed lineage

[Certain] **HIGH**. A 2 arcsec matching candidate exists, but uses Euclidean distance on (RA_rad,Dec_rad), rather than great-circle angular distance. A later integration script relabels MagPhys CATAID as objid without an explicit identifier crosswalk. Other STAR script generations use 10 or30 arcsec, so there is no single demonstrated locked match protocol.

Claims: DATA-M001, DATA-M002. Experiments: EXP-DATA-A01, DATA-PROV-001. Provenance: HISTORICAL MODEL / EXPLORATORY. Assessment: INCONCLUSIVE / reconstruction required.

- `C:\Users\pmqr7\OneDrive\Documents\STAR\pip.py` — lines16–21 and24–35; SHA256 `912eca01f5bee760f5075560460d4928bc842446cddec0281a8e713bfe7e8a91`. two-dimensional radian KDTree, cutoff2arcsec, finite-filtered matches, output merged_sdssdr18_mangaHI_kdtree.csv
- `C:\Users\pmqr7\OneDrive\Documents\STAR\singularity.py` — lines20–24 and35–43; SHA256 `0ed13876725511c846b3c94fdc21db8636298297163cb6c1ceaae76e9b0b3283`. CATAID relabeled as objid then joined
- `C:\Users\pmqr7\OneDrive\Documents\STAR\STAR.py` — lines95,110–115,183–195,214,222,230; SHA256 `df10464ffb6bee489d78d52e75a515ecfe179e2a27c60dca679e74cd6b966ef3`. 10arcsec default and matched_df1=df1.copy after collecting chunk matches
- `C:\Users\pmqr7\OneDrive\Documents\STAR\STAR5.py` — lines42,52–54,97,103,107; SHA256 `d44de89fa69032b5ca8711a2a1c143656a423a2cebb9a41fb1e57a6768329f2b`. 30arcsec variant with index merges

Limit: Static code inspection establishes potential matching/row-association errors; it does not prove that every integrated table was generated by these exact revisions.

Registry action: Record code variants separately and reconstruct EXP-DATA-A01 using a registered coordinate system, exact input IDs, spherical matching, and explicit identity crosswalks.

### E-LCL-003 — Packaged projection manifest disagrees with adjacent artifact

[Certain] **HIGH**. S.T.A.R.-Program/data/derived/acsc_projected_cremona_final.csv is2bytes with no data/header, but its adjacent manifest reports38,042 output rows. Both packaged raw arithmetic datasets contain1,500 rows. The working kepler/derived/acsc_projected_cremona_final.csv contains38,042 rows. Repeated filenames refer to materially different revisions.

Claims: MAP-001, MAP-002, MAP-003, TOPO-001, DATA-M002. Experiments: EXP-MAP-A01, EXP-TOPO-A01, DATA-PROV-001. Provenance: NEGATIVE / NULL / HISTORICAL MODEL. Assessment: INCONCLUSIVE.

- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\data\derived\acsc_projected_cremona_final.csv` — entire2byte file; SHA256 `7eb70257593da06f682a3ddda54a9d260d4fc514f645237f5ca74b08f8da61a6`. no data/header
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\data\derived\acsc_projected_cremona_final.csv.manifest.json` — JSON rows_output; SHA256 `5980d29db9705eba87643f749f443da1d4f779430cfd5ff4e61bb4b0655ba171`. 38042
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\data\raw\cremona_raw_parsed.csv` — CSV1500data rows; SHA256 `960a96877035b51d8dd22bee229a00ef512442782d07f7f0529c92c33f00cbc0`. 
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\data\raw\lmfdb_raw_parsed.csv` — CSV1500data rows; SHA256 `8f9ba5410bdbcc980dce7c915af5ca35b4c1dfce0c08229688b5b38308d1f607`. 
- `\\wsl.localhost\Ubuntu\home\kepler\derived\acsc_projected_cremona_final.csv` — CSV38042data rows; SHA256 `ca37c71b32151ee069b427a1cddc2f446bbe6395c813ddac27a02d815ff77bc2`. 

Limit: Only selected packaged files were deeply profiled. Similar2byte projection placeholders appear in the other research repository snapshots; working artifacts exist elsewhere.

Registry action: Preserve exact-path/hash revisions, flag copied manifests as inconsistent, and do not attribute working full-sample results to packaged subsets or blank outputs.

### E-LCL-004 — Arithmetic validation manifests omit several required invariants

[Certain] **MEDIUM**. Root Cremona and LMFDB validation manifests name raw inputs and output tables and declare38,042/3,064,705rows. Both declare regulator, real_period and torsion_order absent for every row. They do not record input/output SHA256, exact upstream release, code revision, environment, or experiment ID.

Claims: DATA-M002, RANK-001, MAP-002. Experiments: DATA-PROV-001, EXP-RANK-A01, EXP-MAP-A01. Provenance: HISTORICAL MODEL / EXPLORATORY. Assessment: INCONCLUSIVE; usable partial data infrastructure.

- `\\wsl.localhost\Ubuntu\home\kepler\acsc_validation_cremona.manifest.json` — JSON input_file,output_file,rows_input,rows_output,diagnostics.null_counts; SHA256 `ab40c566b08a12339887ab06f91b7969bea812da06abcb3f96646d8d1e1ecebe`. 
- `\\wsl.localhost\Ubuntu\home\kepler\acsc_validation_lmfdb.manifest.json` — JSON input_file,output_file,rows_input,rows_output,diagnostics.null_counts; SHA256 `9103710b256c42bf182c2e4e0f6ddd1c8cc1e14b206f22263b3c51c1a3de1a3a`. 
- `\\wsl.localhost\Ubuntu\home\kepler\cremona_raw_parsed.csv` — CSVheader and full checked table; SHA256 `135f01c3e07390b3fba0784cf91b8c0e1799562e77ad670923c05683e8563e11`. 
- `\\wsl.localhost\Ubuntu\home\kepler\lmfdb_raw_parsed.csv` — CSVheader and full checked table; SHA256 `bdb6bd1bd5b9fac8d7210623dbd2017962b3a75963c6581cda2f431b6f2d41b0`. 

Limit: Audit hashes provide an as-found snapshot, not retroactive proof of the generating run. Missing regulator/torsion limits invariant competition and extended mapping tests.

Registry action: Retain partial lineage and missing-invariant diagnostics; bind exact upstream snapshot and preprocessing code to a registered dataset version before controlled testing.

### E-LCL-005 — Estimated3-Selmer quantities are explicitly proxies

[Certain] **MEDIUM**. Arithmetic enrichment artifacts label the relevant field estimated_3_selmer_bound, alongside sage_rank, pari_2_selmer_rank and pari_analytic_rank. The name and schema distinguish an estimate from a computed3-Selmer group; no astronomical correspondence follows from this arithmetic calculation.

Claims: RANK-001, RANK-003, CORE-001. Experiments: EXP-RANK-A01, DATA-PROV-001. Provenance: HISTORICAL MODEL / EXPLORATORY. Assessment: INCONCLUSIVE for cosmic hypotheses.

- `\\wsl.localhost\Ubuntu\home\kepler\acsc_final_combined.csv` — CSVheader and initial rows; estimated_3_selmer_bound column; SHA256 `b2248d76c9c274d0fea23f3c84b7cb54519c9b33cd48c4d857bed53e30d50bb4`. 
- `\\wsl.localhost\Ubuntu\home\kepler\acsc_final_cremona.csv` — CSVheader; SHA256 `4a865af2577e5f98491de35d82c398a7e5cad6bf8ecaad5f7ce1fe56401471df`. 
- `\\wsl.localhost\Ubuntu\home\kepler\acsc_final_lmfdb.csv` — CSVheader; SHA256 `98b9f1b3c1e9e2eb3c36729c3e5599385f3d32e1f49f3301743a9c170f38c97c`. 

Limit: The audit did not execute Sage/PARI computations or verify mathematical group calculations.

Registry action: Record estimated/proxy status explicitly; prevent3-Selmer exactness or cosmic-evidence promotion from these filenames/results.

### E-LCL-006 — PTD batch completion is computational lineage without cosmic/null validation

[Certain] **MEDIUM**. The root PTD aggregate manifest reports127 chunks,127 completed,0failed, chunk300, maxdim1 and a numerical filtration threshold. It names arithmetic coordinates and pickle outputs, but not independent cosmic input, null ensemble, effect uncertainty, mapped Claim ID or canonical experiment ID. maxdim1 cannot supply H2 void topology.

Claims: MAP-005, TOPO-001, TOPO-002, CORE-001. Experiments: EXP-MAP-A01, EXP-TOPO-A01. Provenance: HISTORICAL MODEL / EXPLORATORY. Assessment: INCONCLUSIVE; reconstruction required.

- `\\wsl.localhost\Ubuntu\home\kepler\derived\tda_ptd_batches\aggregate_manifest.json` — JSON n_chunks,completed,failed,params and result_files; SHA256 `21114fe5cbbd7fd58bc3baeb512fab1161289f89f2c162ff0f1bad41c255f004`. 
- `\\wsl.localhost\Ubuntu\home\kepler\derived\tda_ptd_batches\summary_per_chunk.json` — per-chunk result metadata; SHA256 `55322e632b7c6198adb38676df693b7c08b2dee353825eb29692985cb90fe298`. 

Limit: Pickle outputs were inventoried but not deserialized or executed. Completion reports were not reproduced. The copied packaged aggregate may refer to missing/blank projection artifacts.

Registry action: Retain completed-run reports as historical computational evidence only; reconstruct identical mapping, filtration and survey/null comparisons before TOPO-001 promotion.

### E-LCL-007 — Two RTCH-E1 generations are synthetic controls with matching input hashes

[Certain] **HIGH**. Outer results are a900-point demo recorded2026-09-18T20:42:17Z; nested results are a350-point demo recorded2026-09-18T21:48:45Z. Both declared input SHA256 values match the corresponding as-found demo_torus.csv. The scripts differ: root old implementation sends sparse kNN adjacency to ripser(distance_matrix=False); current program version describes/uses complete Euclidean VR and limits demo350. Neither manifest binds a code revision/hash or full package versions.

Claims: RTCH-M001, ECC-001, ECC-002, RANK-002, TOPO-001. Experiments: RTCH-E1 (noncanonical local experiment), EXP-RTCH-B01, EXP-ECC-B01, EXP-TOPO-A01. Provenance: SIMULATION / HISTORICAL MODEL. Assessment: INCONCLUSIVE for arithmetic/cohomological/physical claims.

- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\results\run_manifest.json` — JSON input_sha256,n_analysis,config,software; SHA256 `331fc7e3c749ff1f0c12632e1d77ba73096ffe6f55e6e40bc3a0e5fe10978925`. 
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\data\demo_torus.csv` — entire CSV;900data rows; SHA256 `2790c3bdebb665ffa9a5df3ec6b8093dc678c743303b56732be751678bdcfce7`. 
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\RTCH_E1\results\run_manifest.json` — JSON input_sha256,demo_mode,n_analysis,topology_method; SHA256 `bd3c605cdcf76c7ba0d348b3266024165c9133e19f4b3b81fb82d81a8b2a5901`. 
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\RTCH_E1\data\demo_torus.csv` — entire CSV;350data rows; SHA256 `ce3e2d8dd919c83362de1fcbe099f8074abe8a693d1dc2664da6956240021e69`. 
- `\\wsl.localhost\Ubuntu\home\kepler\rtch_e1.py` — lines334,862–885; SHA256 `37b0763b7e2677ea080ef390588fa65b1486bb5438d0e8e72658641401e888f4`. old sparse-adjacency method; n=900 synthetic generator
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\rtch_e1.py` — lines371–407,985–1011; SHA256 `4fe93acda593d564ab204efac217cdfe9aa76c256db57d057aa17ef29dc75a1f`. corrected completeVR; n=350 synthetic generator

Limit: Exact execution-code attribution remains unverified because manifests lack code revision. A synthetic positive control is neither real elliptic-curve topology nor astronomical/physical validation.

Registry action: Keep both generation IDs and exact input hashes; register RTCH-E1 as a separate local simulation/control if desired, without silently substituting it for canonical EXP-RTCH-B01.

### E-LCL-008 — RTCH demo results do not pass declared null criterion

[Certain] **HIGH**. The900-point result reports all topology-null empirical p-values1.0 and no H1/H2/H3 summary. The350-point result has H1max persistence0.7075445652 and H2max0.3834588528, but null p-values1/3 with only2nulls at alpha0.01; minimum attainable plus-one p is1/3, so the declared significance gate cannot be met. The nested graph-eccentricity rank cvR2=0.17245548 is a synthetic-demo metric, not controlled astronomical prediction.

Claims: RANK-002, TOPO-001, ECC-001, RTCH-M001. Experiments: RTCH-E1 (noncanonical local experiment), EXP-TOPO-A01. Provenance: SIMULATION / NEGATIVE / NULL. Assessment: INCONCLUSIVE / diagnostic, no support promotion.

- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\results\result.json` — JSON topology and nulls; SHA256 `09136ef0b8d380f09f49f968d9f749673a2470bb8557353e4d31566dddf94460`. 
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\RTCH_E1\results\result.json` — JSON topology.intrinsic,H1/H2 nulls; SHA256 `d294a3426d69f565d33b07b641768479d04bc12b586cb2b2f17e9f9d9b64cef4`. 
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\RTCH_E1\results\prediction_tests.csv` — CSVline5 rank/graph_eccentricity; SHA256 `30b91aed6a6a687b2fe73cdebed209552e6f41f1af1127e1110e9bc7ca26f3e6`. 
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\RTCH_E1\results\run_manifest.json` — JSON n_nulls=2,alpha=.01; SHA256 `bd3c605cdcf76c7ba0d348b3266024165c9133e19f4b3b81fb82d81a8b2a5901`. 

Limit: The audit reads historical results rather than reproducing computation. Weak null resolution limits power; non-rejection does not establish that the true arithmetic/cosmic hypotheses are false.

Registry action: Retain both null/diagnostic generations. Rebuild adequate null counts, effect sizes, intervals, multiple-comparison controls, code binding and independent arithmetic/astronomical inputs before empirical promotion.

### E-LCL-009 — RTCH permutation formula can yield false significance from NaN

[Certain] **HIGH**. Outer rank_label_nulls rows pc2/pc3 have blank observed/null Spearman diagnostics yet permutation p=0.009900990099009901. Both outer scalar columns are constant0 across all900 rows (min=max=0). Static code does not check finite observed/null correlations before (1+sum(vals>=observed))/(1+len(vals)). If observed isNaN, all comparisons areFalse and the formula returns1/101; that number cannot support significance.

Claims: CTRL-A001, RANK-002, TOPO-001. Experiments: RTCH-E1 (noncanonical local experiment), EXP-CTRL-A02, EXP-CTRL-A03. Provenance: NEGATIVE / NULL. Assessment: INCONCLUSIVE; invalid diagnostic p-values.

- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\results\rank_label_nulls.csv` — CSVlines3–4; SHA256 `d8b357e6a10b52279605f26a5b6f233f2eb2e954edc9f6d744185523fbf3ad32`. blank correlation diagnostics with p=1/101
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\results\scalar_embeddings.csv` — CSVlines2–901; pc2/pc3 columns; SHA256 `2fa37333da3cf2b876ace8db20561f2695a807cbaf952a3785956f97d3142887`. min=max0 for both columns over900rows
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\rtch_e1.py` — lines664–692; SHA256 `4fe93acda593d564ab204efac217cdfe9aa76c256db57d057aa17ef29dc75a1f`. no constant/NaN guard in Spearman permutation function
- `\\wsl.localhost\Ubuntu\home\kepler\rtch_e1.py` — lines589–606; SHA256 `37b0763b7e2677ea080ef390588fa65b1486bb5438d0e8e72658641401e888f4`. same old formula

Limit: Static logic and stored blanks establish invalid evidentiary status; source execution was not run to reproduce the failure.

Registry action: Exclude undefined-correlation p-values from support, preserve them as diagnostic failures, and require finite/constant-input checks before permutation reporting.

### E-LCL-010 — RTCH scalar CV does not validate held-out representation construction

[Certain] **HIGH**. RTCH builds median imputation/scaling, PCA, kNN geodesics and diffusion coordinates on the complete analysis sample, then performs5fold Ridge prediction on precomputed scalars. Faltings_height is also part of intrinsic features and later used as a prediction target. Its reported cvR2~0.99997(old) or0.98505(new) is not independent prediction of an excluded invariant.

Claims: RANK-002, RTCH-M001, ECC-001. Experiments: RTCH-E1 (noncanonical local experiment), EXP-CTRL-A03. Provenance: SIMULATION / NEGATIVE / NULL / HISTORICAL MODEL. Assessment: INCONCLUSIVE; leakage/contamination relevant.

- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\rtch_e1.py` — lines70–80,313–324,569–603,617–649,835,891–902; SHA256 `4fe93acda593d564ab204efac217cdfe9aa76c256db57d057aa17ef29dc75a1f`. global representation then downstream5fold CV
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\results\prediction_tests.csv` — CSVline7 faltings_height/pc1; SHA256 `6a2c0490e6d8e82a554037067719f620ffd3210f12c2da356d53fc70a53e06fb`. 
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\RTCH_E1\results\prediction_tests.csv` — CSVline7 faltings_height/pc1; SHA256 `30b91aed6a6a687b2fe73cdebed209552e6f41f1af1127e1110e9bc7ca26f3e6`. 

Limit: Global unsupervised representation is transductive rather than a demonstrated induction to unseen samples. Target inclusion is explicit in the source feature list; measured leakage effect was not estimated.

Registry action: Set Leakage Status POTENTIAL LEAKAGE for rank generalization and CONFIRMED TARGET CONTAMINATION for Faltings-held-out interpretation; rebuild fold-local embeddings and remove target-defining inputs for independent prediction tests.

### E-LCL-011 — RTCH stability rows repeat the whole demo sample

[Certain] **MEDIUM**. Nested stability CSV contains2identical whole-sample rows, while result.json stability isempty. Current choose_topology_sample returns a copy when len(df)<=max_points; demo350 with max_points350 therefore repeats the same entire sample, rather than independent subsampling.

Claims: RTCH-M001, ECC-001, TOPO-001. Experiments: RTCH-E1 (noncanonical local experiment). Provenance: SIMULATION / NEGATIVE / NULL. Assessment: INCONCLUSIVE; stability not demonstrated.

- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\RTCH_E1\results\stability_summary.csv` — CSVlines2–3; SHA256 `4af317de92879957316bd3bbeb4cd4c1755b4b4adf15f437aa2ae37e2d0fb265`. identical H0/H1/H2 maxima
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\RTCH_E1\rtch_e1.py` — lines301–310,859–875,939–967; SHA256 `4fe93acda593d564ab204efac217cdfe9aa76c256db57d057aa17ef29dc75a1f`. whole-sample copy at<=limit; no stability population of result.json

Limit: Available file hashes identify current code, but old manifests omit exact code attribution. CSV existence is not independent resampling/replication.

Registry action: Record CSV stability output separately from empty JSON summary and require genuine perturbation/subsampling before claiming robustness.

### E-LCL-012 — Historical L-cosmo SFR script uses global preprocessing and engineered nonarithmetic rank

[Certain] **HIGH**. L-cosmo(s).py performs global median imputation, MinMax fit, massmedian, redshiftbinning and groupmeans before train/test splitting. cosmo_rank is a weighted morphology/confidence/redshift feature, not elliptic-curve rank. L_cosmo_s* columns are constructed/plotted but omitted from the model feature list; this script therefore cannot establish incremental predictive value for L_cosmo. Its groupmean Schechter form differs from the canonical mass-ratio sum.

Claims: COSMO-L001, COSMO-L002, COSMO-R001, SFR-A001, CTRL-A002. Experiments: EXP-L001, EXP-SFR-A01, EXP-CTRL-A03, CTRL-COSMO-001. Provenance: HISTORICAL MODEL / EXPLORATORY / NEGATIVE DIAGNOSTIC. Assessment: INCONCLUSIVE; reconstruction required.

- `C:\Users\pmqr7\OneDrive\Documents\STAR\L-cosmo(s).py` — lines22,35–44,50–61,97–105; SHA256 `408dca936a416be0f25d1dcc705e302c58a72cfbfb5661441c6297872d5df297`. global transformations and no L_cosmo_s* in modelfeatures
- `C:\Users\pmqr7\OneDrive\Documents\STAR\L-cosmos.py` — lines35–46,69–78; SHA256 `50dfe4ad9b1d04bb8065625460b3e8ca27f08cf824cb2dfd21cf70e843ff02e4`. engineered cosmo_rank before split

Limit: Static leakage routes are directly observed, but no experiment estimating their performance effect was run. Script relative input merged_data.csv is absent in that exact folder; candidate parent-folder datasets exist but execution lineage is undocumented.

Registry action: Retain M/H categories and R evidence state; set preprocessing leakage concern, rename/cross-reference cosmo_rank semantically, bind the actual input revision, and conduct fold-local incremental models before promotion.

### E-LCL-013 — Random-feature baseline targets stellar mass and named input lacks target

[Certain] **HIGH**. model5.py targets logmstar, not SFR. The discovered SDSSDR18_200000.csv has18columns and lacks logmstar, so the named input cannot run the provided target expression as-is. The source samples5features from all columns without excluding the target. Reconstructing the declared seed42 feature sampling on the as-found header gives objid,ra,run,r,u; target inclusion is not confirmed for this exact input.

Claims: CTRL-RF001, SFR-A001. Experiments: EXP-CTRL-A01, EXP-CTRL-A03. Provenance: HISTORICAL MODEL / NEGATIVE DIAGNOSTIC. Assessment: INCONCLUSIVE; reconstruction blocked by dataset schema/version.

- `C:\Users\pmqr7\OneDrive\Documents\STAR\model5.py` — lines12,16–22,26,32,37; SHA256 `7d1d9e3d57e26e37ec4e1a9f9578b9ff5d4291f9e68a66eb327a50f638095d44`. target logmstar; no target exclusion
- `C:\Users\pmqr7\OneDrive\Documents\STAR\SDSSDR18_200000.csv` — CSVheader line1; SHA256 `9dca2008683fde4b0f7a90af5de85ee846a30a47f6f6fae3968c83dea06fa5d2`. 18columns, no logmstar

Limit: The audit did not run model training. Another undocumented dataset revision may have included the required target; all-column sampling only establishes potential target-inclusion risk.

Registry action: Classify as historical random-feature stellar-mass baseline/control candidate, preserve absent-target diagnostic, and require exact input/schema plus explicit outcome exclusion and SFR-specific control reconstruction.

### E-LCL-014 — Local CSV registries reuse canonical IDs with conflicting meanings

[Certain] **HIGH**. Repository registry CSVs use CLAIM-ACSC-001 etc rather than PDF CORE-001 etc. More seriously, experiment CSV maps EXP-CTRL-A01 to provenance control, EXP-CTRL-A02 to leakage control, contrary to attached PDF random-feature/permutation definitions. Dataset entries remain planned with deferred provenance. These namespaces cannot be silently merged by experiment-string identity.

Claims: CORE-001, CTRL-RF001, CTRL-A001, CTRL-A002, DATA-M002. Experiments: EXP-CTRL-A01, EXP-CTRL-A02, EXP-CTRL-A03, DATA-PROV-001. Provenance: UNVERIFIED / HISTORICAL MODEL. Assessment: INCONCLUSIVE provenance control.

- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\registry\claim_evidence_v0.2.csv` — CSVheader andlines2–7; SHA256 `ef50ff75fe995633934e7a12a635f76d16333ed7d260ddd1ffee7930bb9d433f`. 
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\registry\experiment_registry_v0.2.csv` — CSVlines4–6; SHA256 `b2a8c69710fedfa708d763eebf150cf8b35fe49da8ef8392e9ee0a4625161399`. 
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\registry\claim_experiment_crosswalk_v0.2.csv` — CSVlines4–6; SHA256 `d8b5bc55187b1ba0f2e6d1e2f0d2a1571c2e92a8e93570de25191892290e34ec`. 
- `\\wsl.localhost\Ubuntu\home\kepler\S.T.A.R.-Program\registry\dataset_registry_v0.1.csv` — CSVlines2–9; SHA256 `b11f2cf25b903ff1ad32c7d35a6353b3f327d31133f8c816363f26865f78150b`. 

Limit: Attached Charter/Registries govern this requested update. The repository CSV may represent a distinct historical control schema, not an intent to change canonical PDF identifiers.

Registry action: Keep repository CSV namespace as legacy, preserve original files, and document explicit semantic crosswalk/conflicts before migrating IDs into the canonical update.

### E-LCL-015 — Partial upstream download metadata survives for observational sources

[Certain] **INFO**. Download-zone sidecars identify MaNGA HI DR17 v2_0_1 FITS and a SkyServer/CasJobs SDSS CSV export. They provide partial upstream attribution; they do not include the full SDSS SQL, release/query selection, acquisition hash, or complete raw-to-model lineage. The ecdata README identifies the Cremona database and a Zenodo release DOI, but the selected derived arithmetic manifests do not bind to a specific commit/release.

Claims: DATA-M002. Experiments: DATA-PROV-001, EXP-DATA-A01. Provenance: UNVERIFIED / HISTORICAL MODEL. Assessment: Partial data infrastructure.

- `C:\Users\pmqr7\OneDrive\Documents\STAR\mangaHIall.fitsZone.Identifier` — ZoneTransfer ReferrerUrl and HostUrl; SHA256 `de193697f18a34335d7a0c99b8d4fbb3ab730cd3ca76e83a667e2aa3aeb8dfc0`. https://data.sdss.org/sas/dr17/manga/HI/v2_0_1/mangaHIall.fits
- `C:\Users\pmqr7\OneDrive\Documents\STAR\SDSSDR18_200000.csvZone.Identifier` — ZoneTransfer HostUrl; SHA256 `91ff0b446804f8dfe2aa0e2066df08629b2a4ac12a7f9f6b28825679af038b84`. https://skyservice.pha.jhu.edu/CasJobsOutput/CSV/MyTable_pmqr771_0.csv
- `\\wsl.localhost\Ubuntu\home\kepler\ecdata\README.md` — lines4–12; SHA256 `619466f9a1542c3bfeaa68b592feb903edd205c652cac59d7f21d70444203bb5`. Cremona Database; DOI10.5281/zenodo.161341

Limit: URLs and DOI are recorded from local metadata and were not revalidated online. As-found hashes do not establish acquisition-date identity.

Registry action: Preserve upstream identifiers as observed provenance fields; add exact release/query and processing/code bindings before declaring complete lineage.

### E-LCL-016 — STAR map visualization uses illustrative synthetic data and preselected Hubble calibration

[Certain] **HIGH**. Recovered S.T.A.R.M.A.P. catalog explicitly labels its data illustrative, combines12 hardcoded example curves with148 synthetically generated rows, and seeds generation with0x53544152. The H_eff implementation states calibration so high-z recovers Planck and low-z approachesSH0ES, with hardcoded correction coefficients. Geometry angles are hash-derived from curve labels; cluster summaries are hardcoded. These visualizations do not supply independent observational or arithmetic validation.

Claims: CORE-001, MAP-001, MAP-002, COSMO-E002. Experiments: EXP-MAP-A01, EXP-COSMO-B02, DATA-PROV-001. Provenance: SIMULATION / HISTORICAL MODEL / EXPLORATORY. Assessment: INCONCLUSIVE; model construction only.

- `/home/kepler/S.T.A.R.M.A.P./src/lib/star/catalog.ts` — lines27–40,43–87,91–99; SHA256 `f585130c982be4789c4bc701119b1a1a5fdcb72bd475700b01d48c8c921fbb29`. Recovered by native WSL read; original source preserved
- `/home/kepler/S.T.A.R.M.A.P./src/lib/star/physics.ts` — lines27–42,117–126; SHA256 `a9125fddf3570012c8f1a3467562fecf31132fecf301fd3decdf300e59bfe234`. Recovered by native WSL read; original source preserved
- `/home/kepler/S.T.A.R.M.A.P./src/routes/hubble.tsx` — lines13–43,125–149; SHA256 `0ac7b166116e1d3ae57fcc57a1e9435a4e5c7b3d26d70dc34349601c8b24b24d`. Recovered by native WSL read; original source preserved
- `/home/kepler/S.T.A.R.M.A.P./README.md` — Vision and Implementation Status sections; SHA256 `e51bbff49db1e33900f05f5082985a576f18a0de8580e733a78e75680dacc7e3`. Recovered by native WSL read; original source preserved

Limit: Static inspection identifies source data origin and calibration. The12 hardcoded examples were not revalidated against external catalogs; synthetic invariants were not verified as mutually consistent elliptic curves. The visualization was not executed.

Registry action: Bind website displays to a synthetic/model provenance label; preserve model formulas and coefficients as construction choices. Keep COSMO-E002 downstream; displayed agreement with calibration anchors is not independent confirmation.

## Provenance completeness

All selected dataset records remain PARTIAL. The machine-readable report records the source, data revision, preprocessing, code, environment, parameters, seeds, mapping, statistical procedure, null, result and experiment-binding fields individually. As-found hashes were added where files were fully read. They do not retroactively bind historic executions.

The document-generator corpus manifest matched 8 of 9 current source PDF hashes. See JSON for per-document mismatches and availability.

## Inventory errors

Exact inaccessible or unresolvable paths and errors:

- {"path": "\\\\wsl.localhost\\Ubuntu\\home\\kepler\\.azure", "error": "[WinError 3] The system cannot find the path specified: '\\\\\\\\wsl.localhost\\\\Ubuntu\\\\home\\\\kepler\\\\.azure'"}
- {"path": "\\\\wsl.localhost\\Ubuntu\\home\\kepler\\.aws", "error": "[WinError 3] The system cannot find the path specified: '\\\\\\\\wsl.localhost\\\\Ubuntu\\\\home\\\\kepler\\\\.aws'"}
- {"path": "\\\\wsl.localhost\\Ubuntu\\home\\kepler\\S.T.A.R.-Program\\docs\\STAR.ipynb", "error": "[WinError 2] The system cannot find the file specified: '\\\\\\\\wsl.localhost\\\\Ubuntu\\\\home\\\\kepler\\\\S.T.A.R.-Program\\\\docs\\\\\\uf02aSTAR.ipynb'"}
- {"path": "\\\\wsl.localhost\\Ubuntu\\home\\kepler\\S.T.A.R.-Program\\historical\\r&d\\archive\\regenerate_pantheon_module.pyZone.Identifier.trashinfo", "error": "[WinError 2] The system cannot find the file specified: '\\\\\\\\wsl.localhost\\\\Ubuntu\\\\home\\\\kepler\\\\S.T.A.R.-Program\\\\historical\\\\r&d\\\\archive\\\\regenerate_pantheon_module.py\\uf03aZone.Identifier.trashinfo'"}
- {"path": "\\\\wsl.localhost\\Ubuntu\\home\\kepler\\S.T.A.R.-Program\\historical\\r&d\\archive\\regenerate_pantheon_module.pyZone.Identifier", "error": "[WinError 2] The system cannot find the file specified: '\\\\\\\\wsl.localhost\\\\Ubuntu\\\\home\\\\kepler\\\\S.T.A.R.-Program\\\\historical\\\\r&d\\\\archive\\\\regenerate_pantheon_module.py\\uf03aZone.Identifier'"}
- "[WinError 3] The system cannot find the path specified: '\\\\\\\\wsl.localhost\\\\Ubuntu\\\\home\\\\kepler\\\\S.T.A.R.M.A.P.'"
- {"path": "\\\\wsl.localhost\\Ubuntu\\home\\kepler\\Arithmetic-Cosmic-Structure-Conjecture-ACSC-\\STAR.ipynb", "error": "[WinError 2] The system cannot find the file specified: '\\\\\\\\wsl.localhost\\\\Ubuntu\\\\home\\\\kepler\\\\Arithmetic-Cosmic-Structure-Conjecture-ACSC-\\\\\\uf02aSTAR.ipynb'"}

## Evidence-promotion decision

No core arithmetic/cosmic, SFR arithmetic, ECC or RTCH physical claim qualifies for empirical/replicated/predictive promotion from this source audit. Historical constructions and simulation diagnostics remain usable with explicit provenance and limitations.

No source was overwritten. Recommended registry classifications preserve historical and negative evidence.