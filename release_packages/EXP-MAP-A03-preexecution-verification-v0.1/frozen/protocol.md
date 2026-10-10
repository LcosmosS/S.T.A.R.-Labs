# EXP-MAP-A03 preregistration — MCJ conditional rank-coherence null test

## Governance state

- Experiment_ID: \`EXP-MAP-A03\`
- Qualified Experiment_ID: \`REPO-CSV-v0.2:EXP-MAP-A03\`
- Claim_ID: \`CLAIM-ACSC-002\`
- Qualified Claim_ID: \`REPO-CSV-v0.2:CLAIM-ACSC-002\`
- Dataset_ID: \`DATA-ARITHMETIC\`
- Qualified Dataset_ID: \`REPO-CSV-v0.2:DATA-ARITHMETIC\`
- Parameter_Set_ID: \`PAR-MAP-003\`
- Null_ID: \`NULL-MAP-003\`
- Protocol version: \`EXP-MAP-A03-prereg-v1\`
- Controlled execution: **disabled**
- Controlled support: **not established**
- Physical support: **not established**

This is a protocol-commitment artifact only. It contains no controlled result and does not authorize execution. The repository-qualified A03 is the BSD-independent MCJ arithmetic test defined here; it is **not an alias** of the distinct \`STAR-PDF-v0.2:EXP-MAP-A03\` definition ("Arithmetic Generator Controls"). The existing namespace resolution remains \`scope_conflict_no_alias\`.

The single scientific question is whether the **rank-blind** map from conductor and exact rational modular \(j(E)\) exhibits local arithmetic-rank coherence beyond a fixed within-conductor-decile rank-permutation null. No astronomical observations enter this experiment.

## Canonical source and pinned provenance

The only scientific input file read by the experiment is the same pinned John Cremona ecdata source used by EXP-MAP-A01:

- upstream repository: \`https://github.com/JohnCremona/ecdata.git\`
- repository gitlink: \`data/ecdata\`
- pinned upstream commit: \`25cec5ecfec8b9f016eb1631ac633194c2bed39f\`
- upstream commit date: \`2026-02-04T16:54:47Z\`
- canonical file: \`allcurves/allcurves.00000-09999\`
- repository path: \`data/ecdata/allcurves/allcurves.00000-09999\`
- file size: 2,146,401 bytes
- Git blob SHA-1: \`baab5801d7f81e1d5c44f5eb5acf4f1e100bc90b\`
- file SHA-256: \`259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968\`
- exact source row count: **64,687**
- format: whitespace-delimited ecdata \`allcurves\`
- schema, in order: \`conductor isogeny curve_number [a1,a2,a3,a4,a6] rank torsion_order\`
- license: Artistic License 2.0 per upstream ecdata
- source/provenance evidence: \`PROV-004\`
- A03 manifest: [dataset_manifest.json](dataset_manifest.json)

A hash mismatch, missing source, malformed or blank record, duplicate curve label, invalid source field, or source-row mismatch aborts. No alternate source, cache, CI subset, historical CSV, or observational dataset is permitted.

## Exact analysis cohort — no post-hoc filtering

The cohort is fixed before evaluating the endpoint or any null statistic:

1. Read all **64,687** source rows.
2. Retain exactly \`curve_number == 1\` from each isogeny class: **38,042** representatives.
3. From each representative's integral Weierstrass coefficients, compute \(c_4\) and \(\Delta\) exactly using integer arithmetic.
4. If \(\Delta=0\), abort as a source/protocol failure.
5. If \(c_4=0\), then \(j=0\) and \(\log j\) is undefined. Exclude that curve **before accessing its rank for analysis**, record it in \`exclusions_j_zero.csv\`, and do not replace it.
6. The pinned source contains exactly **106** such \(j=0\) representatives. The locked analysis cohort is therefore exactly **37,936** curves.
7. Sort accepted rows by ascending \`(conductor, Cremona label ASCII)\`.

Any different source, representative, exclusion, or accepted count fails closed. There is no imputation, rank-based filtering, torsion filtering, significance-based trimming, outlier deletion, fallback representative, or post-hoc cohort modification. The 106-exclusion count is a deterministic property of the pinned a-invariants and discriminants, not an outcome-tuned choice.

## Exact arithmetic and locked PAR-MAP-003

For integral Weierstrass coefficients \([a_1,a_2,a_3,a_4,a_6]\), compute

\[
b_2=a_1^2+4a_2,\quad b_4=a_1a_3+2a_4,\quad b_6=a_3^2+4a_6,
\]

\[
b_8=a_1^2a_6+4a_2a_6-a_1a_3a_4+a_2a_3^2-a_4^2,
\]

\[
c_4=b_2^2-24b_4,\quad
\Delta=-b_2^2b_8-8b_4^3-27b_6^2+9b_2b_4b_6,\quad
j=\frac{c_4^3}{\Delta}.
\]

All arithmetic above is exact integer arithmetic. For every accepted row define the dimensionless, rank-blind coordinates

\[
x=\ln N,\qquad
y=\operatorname{Re}(\log j)=3\ln|c_4|-\ln|\Delta|,
\]

\[
z=\operatorname{Im}(\log j)=
\begin{cases}
0,&j>0,\\
\pi,&j<0.
\end{cases}
\]

Use natural logarithms and the principal complex branch, so negative real \(j\) has argument \(+\pi\). After exact arithmetic, \((x,y,z)\) and geometric distances use IEEE-754 binary64.

Locked choices: no normalization, clipping, jitter, fitting, learned embedding, regulator term, rank coordinate, or rank-dependent tie handling; ordinary Euclidean distance in \((x,y,z)\); **k=10**; self excluded; equal-distance ties ordered by \`(binary64 squared Euclidean distance, Cremona label ASCII)\`; coordinate duplicates retained; directed choices symmetrized into unique unordered pairs.

## Single primary endpoint

On the fixed k=10 graph with unique unordered edge set \(E\),

\[
T_{\mathrm{obs}}
=-\frac{1}{|E|}\sum_{\{i,j\}\in E}|r_i-r_j|.
\]

Higher \(T\) means greater local rank similarity. Rank is not used until cohort eligibility and graph construction are fixed.

A missing/empty/ambiguous graph, nonfinite coordinate/distance/statistic, duplicate accepted identity, or incomplete tie enumeration fails the attempt. No radius, k, norm, dimensionality, tie policy, or cohort is adjusted after seeing results.

The descriptive quantity \(T_{\mathrm{obs}}-\operatorname{median}(T_{\mathrm{null}})\) is not a second confirmatory endpoint.

## Locked NULL-MAP-003

For the **37,936** accepted curves already sorted by ascending \((N,\mathrm{label}_{ASCII})\), assign zero-based row \(i\) to one of ten rank-blind conductor-order strata:

\[
s_i=\left\lfloor\frac{10i}{n}\right\rfloor,\qquad i=0,\ldots,n-1.
\]

Use \`splitmix64-fisher-yates-v1\` with:

- unsigned word size 64 bits;
- seed **4103**;
- state increment \`0x9E3779B97F4A7C15\`;
- multiplication constants \`0xBF58476D1CE4E5B9\` and \`0x94D049BB133111EB\`;
- all state/mixing arithmetic modulo \(2^{64}\);
- \`randbelow(m)\`: reject values at or above \(\lfloor2^{64}/m\rfloor m\), otherwise return value modulo \(m\);
- Fisher-Yates: for \(i=m-1,\ldots,1\), draw \(j=\mathrm{randbelow}(i+1)\) and swap \(i,j\).

Generate exactly **B=999** sequential null realizations using one continuing RNG stream. For each realization process strata 0 through 9 in numeric order, permuting the **original observed rank vector** independently within each stratum. Do not reset the stream between strata or realizations and do not cumulatively permute the previous realization.

The null holds identities, conductor, accepted cohort, exact arithmetic status, MCJ coordinates, fixed k=10 graph, and the empirical rank multiset within each stratum fixed. No null is skipped, rerolled, regenerated, selected, or replaced.

## Exact inferential rule

For each null draw compute the same \(T_b\). The single test is **one-sided greater**:

\[
p=\frac{1+\#\{b:T_b\ge T_{\mathrm{obs}}\}}{999+1}.
\]

Locked \(\alpha=0.005\). Reject the specified conditional rank-permutation null iff \(p<0.005\); otherwise do not reject it. There is exactly one primary endpoint and no within-protocol multiplicity adjustment.

EXP-MAP-A01 remains separately locked at \(\alpha=0.01\). A03 does not alter A01 and does not claim joint A01/A03 family significance.

## Required output contract

An authorized controlled execution must create exactly four experiment-owned files, without overwriting any existing result path:

1. \`summary.json\`: protocol/experiment identity, source/representative/exclusion/accepted counts, k and edge count, observed statistic, B=999, seed/PRNG, ten stratum sizes, exceedances, p-value, alpha/sidedness/decision, descriptive effect, and interpretation limit.
2. \`observed_mcj_projection.csv\`: columns \`label,isogeny_class,conductor,delta,c4,x,y,z,rank\`; exactly 37,936 data rows.
3. \`null_statistics.csv\`: columns \`realization,statistic\`; realizations exactly 1 through 999.
4. \`exclusions_j_zero.csv\`: columns \`label,isogeny_class,conductor,reason\`; exactly 106 data rows; \`reason=j_exactly_zero\`.

CSV line endings are LF. Binary64 values use 17 significant digits. \`summary.json\` is sorted/indented JSON ending in a newline. The implementation reserves all four output paths before serializing data and refuses overwrite.

## Explicit non-claims

Whether the null is rejected or not, A03 does **not** by itself establish a physical arithmetic-cosmic correspondence; ACSC physical support; BSD; cosmological structure, galaxy, SFR, or survey evidence; confirmation/refutation of A01; a joint A01/A03 significance claim; a universal property outside the pinned cohort; controlled scientific support; physical support; or independent replication.

## Activation boundary

This protocol can support only the lifecycle transition \`planned -> preregistered\`. During this PR the experiment and dataset remain \`Controlled_Execution_Eligible=false\`; controlled-support and physical-support flags remain false; full execution is prohibited.

The committed execution spec may later pass a **binding-only preflight** that proves row/data/code/config bindings while requiring execution eligibility to remain false. That is not an activation preflight and cannot execute the command.

Activation is a separate later PR. It may change only the two controlled-execution eligibility booleans and consequent binding hashes. It may not modify this protocol, cohort, constants, endpoint, null, seed, code path, or output contract. Any scientific modification requires a new protocol version and a new Experiment_ID.

After this preregistration PR merges, the transition-candidates ledger is updated separately to \`preregistered\` with next gate: \`activation-only PR after clean preflight; no protocol modifications\`.
