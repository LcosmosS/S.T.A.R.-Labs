# EXP-MAP-A01 primary execution evidence v0.1

This package preserves investigator-A's original primary transaction
`20261016T041335361140Z-e60fd05117fc`, recorded against source commit
[`1b0f2d7853608bfbab79cf2dc04b002f1f193eb2`](https://github.com/LcosmosS/S.T.A.R.-Labs/commit/1b0f2d7853608bfbab79cf2dc04b002f1f193eb2).
The recorded endpoint rejects the locked arithmetic rank-permutation null at
alpha 0.01. This is primary execution evidence. No independent reproduction,
ACSC validation, BSD result, cosmological result, or physical support is claimed.

## Received immutable package

The original archive was accessible at
`/home/kepler/EXP-MAP-A01-primary-execution.tar.gz` in the investigator's Ubuntu
WSL filesystem. It was copied into this package and checked against the SHA256
provided in the execution handoff:

```text
1a62bf4320a7465ff7308dffd9840e58ed9c68dad9267757c630ff621b60f9a8
```

The [original archive](EXP-MAP-A01-primary-execution.tar.gz) is 965,169 bytes.
Its [archive sidecar](EXP-MAP-A01-primary-execution.tar.gz.sha256) was added
during intake. The eight files under
[`20261016T041335361140Z-e60fd05117fc/`](20261016T041335361140Z-e60fd05117fc/)
are byte-for-byte copies of the archive members: `manifest.json`, its original
`manifest.sha256`, `execution_config.json`, `summary.json`,
`observed_projection.csv`, `null_statistics.csv`, `stdout.log`, and `stderr.log`.
Both logs are present and empty. No output was reconstructed from pasted text,
reserialized, regenerated, or substituted. The original manifest retains its
historical absolute paths and registry snapshots.

Raw manifest SHA256:

```text
8a85f37958b5a2337fea40b02a69c5a521e5e599a9a13987524e2d40f5608cdb
```

The archive's expected root, exact member set, regular-file types, all eight
raw file hashes, manifest sidecar, three output hashes/sizes, configuration,
and logs were checked. `.gitattributes` disables text conversion and filters
for these received bytes, including the two tracked empty logs.
The added README, verifier, archive sidecar, and verification receipt are intake
documentation outside the immutable run directory.

## Primary result and interpretation

The [saved summary](20261016T041335361140Z-e60fd05117fc/summary.json) records
64,687 source rows and 38,042 selected curve-number-1 isogeny representatives,
with a unique undirected k=10 base-neighbor graph containing 221,930 edges.
The endpoint is `T = -mean(abs(elevation_i - elevation_j))`; larger values
indicate greater local rank/elevation coherence on that fixed arithmetic graph.
The graph and observed endpoint were not recomputed during package intake.

The observed statistic is **-114.40183841751903**. Inspection of all **999**
saved null rows confirmed exact ordered realization indices 1 through 999,
finite values, and **zero** statistics greater than or equal to the observed
value. Their minimum is -118.45626999504348, maximum -117.1396386247916,
mean -117.83736063373787, and sample standard deviation 0.2217022855063595.
There are 608 distinct statistic values; repeated statistic values are retained.

The locked correction gives `p = (1 + 0) / (999 + 1) = 0.001`, the smallest
attainable p-value with this number of permutations, rather than zero. This
agrees with the saved `reject_null` decision at alpha 0.01 for the single
preregistered endpoint. No stronger tail probability is inferred.

The admissible interpretation is local arithmetic rank/elevation coherence
against `NULL-MAP-001`, which globally permutes the empirical rank multiset
while holding identities, discriminants, conductors, base coordinates, and
neighbor graph fixed. This does not test a survey-selection-matched
cosmological null or distinguish ACSC from other arithmetic structure. The
saved CSV alone does not independently prove that the recorded PRNG generated
each realization. Null permutations were not regenerated during this review.

The projection CSV contains 38,042 unique labels and isogeny classes, each
label equal to its class plus `1`. Every saved coordinate satisfies the locked
formula using the saved conductor, discriminant, and rank, within numerical
tolerance. These checks do not independently rederive the source cohort or
neighbor graph. The canonical ecdata source is referenced by its pinned gitlink
and manifest input hash; it is not an additional member of the original run
archive.

## Source, governance, and verification

The manifest records `mode=primary`, executor `investigator-A`, transaction
`completed`, both exit statuses zero, a clean pinned Git state before/after,
and passing post-run integrity. Its `reproduction` value is null. Those fields
remain statements recorded by the primary runner; hash verification does not
independently authenticate the execution history.

[Verification receipt](verification.json) records the actual archive/member
hashes, source/configuration/specification and seven registry file hashes
checked against raw Git objects at the pinned commit, all five registry row
hashes, environment/binding canonical hashes, null inspection, and projection
checks. The verifier imports no repository experiment or runner code and
performs no controlled transaction.

From the repository root, with Git and Python 3.12+ available:

```sh
python release_packages/EXP-MAP-A01-primary-execution-v0.1/verify_package.py
```

This read-only command prints a fresh receipt as JSON and exits nonzero on a
failed check. The pinned commit must be available in local Git history. The
[dedicated CI workflow](../../.github/workflows/a01_primary_evidence.yml) runs
the same saved-package inspection without initializing data submodules or
executing the experiment. Its success is package verification, not scientific
replication. The checked-in receipt describes local inspection and does not
claim a particular CI result.

The frozen scientific specification remains
[`EXP-MAP-A01-prereg-v1`](../../preregistrations/EXP-MAP-A01/protocol.md), with
`DATA-ARITHMETIC`, `PAR-MAP-001`, `NULL-MAP-001`, and `CLAIM-ACSC-001` in the
`REPO-CSV-v0.2` namespace. It is distinct from the broader same-string
`STAR-PDF-v0.2:EXP-MAP-A01` mapping-family comparison.
The [earlier release package](../EXP-MAP-A01-prereg-activation-repro-v0.1/README.md)
documents the historical preregistration/approved activation sequence and
remains unchanged. Its no-result statements describe that earlier package.

This PR changes no registry, eligibility, claim, preregistration, execution
specification, website snapshot, or historical package. Controlled-support and
physical-support flags remain false. An accountable independent rerun and its
separate manifest are still outstanding; this evidence intake does not perform
or claim that step. The Charter's review and evidence-promotion gates remain
in force.
