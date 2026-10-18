# Validation record — collaboration invitation v0.1

This record concerns documentation, citations, archive inspection, offline
software policy and web presentation. It does not claim an independent human
review, an experiment rerun, proof validation, survey reacquisition or deployment.
The audited baseline is `d69868e3c1d9ae70944deb239369e53a9ecc1e5b`; the actual
published invitation revision is the PR head, and after merge its merge commit.

## Local validation (2026-10-18)

Environment: Linux/WSL, Python 3.12.3, isolated pytest 9.1.1 and cryptography
46.0.7; final web checks use Node 24.22.0 with the existing npm lockfile. The
initial web pass also succeeded on supported Node 22.23.2. The Node wrapper's
install hook was blocked by local npm policy, so the direct Node 24 binary was
installed in an isolated tool directory and verified before the final checks.
No repository dependency or lockfile was changed. These local tool versions
are recorded observations, not a claim of a fully identical CI environment.

| Check | Actual outcome | Meaning / limit |
| --- | --- | --- |
| Full tracked tree inventory | 15,960 entries: 15,957 blobs and three pinned gitlinks; 108 hashed review inputs | Inventory and surface review, not exhaustive proof/source correctness |
| Charter PDF digest and text inspection | SHA-256 `9a63284900d5349f1d307160929b2542885e4c751439b785369b722d349a5c03` | Governing authority preserved |
| `cffconvert --validate -i CITATION.cff` | Valid CFF 1.2.0 metadata | Schema validation; authorship/ORCID identity not independently authenticated |
| `python -m pytest -q tests/integrations/test_sciserver_approval.py tests/integrations/test_sciserver_policy.py tests/test_charter_documentation_integrity.py tests/test_exp_map_a01_release_package.py` | 62 passed; 18 subtests passed | Offline temporary fixtures and archive/documentation guards; no credentials, remote job or operator key enrollment |
| `python scripts/independent_gate_report.py` | Exit 0; 18 experiments, 16 planned, two preregistered, one execution eligible, no controlled/physical support | Read-only declared-state census |
| `python scripts/independent_dataset_verification.py --format markdown` | Exit 0; nine non-quarantined datasets, four unknown source-provenance records | No `--live-public-sources`, CasJobs export or upload. Existing invalid-escape SyntaxWarnings are reported, not hidden or fixed in this scope. |
| `python release_packages/EXP-MAP-A01-primary-execution-v0.1/verify_package.py` | Exit 0; real 965,169-byte archive, eight members, source bindings and saved-result checks pass | Source commit fetched into local history. Execution authenticity remains unverified; cohort/graph/permutations are not regenerated. |
| Selective ALFALFA LFS hydration | Actual source VOTable SHA-256 `654217f9b3414856c1a8b09071c81eb834a0b0fbc6ec3aea9777e01fdaea1079` | Fresh checkout hydration from repository LFS for the web gate; not an independent publisher download or science/display reauthorization |
| `npm ci` | Locked web dependency installation succeeded; install audit reported zero vulnerabilities | Package audit is not a security certification |
| `npm test` | 296 passed, zero failed, four existing skips | Skips concern absent host-supplied `.grok/skills/og` instructions/references; no scientific tests inferred from them |
| `npm run build` | Registry, research, hydrated sky checks and production build passed | Local build, not publication or deployed-site parity |
| `npm run typecheck` | Passed | Static software check |
| `npm run registry:sync` and build freshness gate | Passed; only README source hash/size and aggregate digest change | Canonical tables, publications and scientific semantics unchanged |
| Change allowlist and protected tree comparison | Passed | Charter, registries, historical/frozen packages, science code/tests, protocols, integration/trust settings, SQL, source data and workflows unchanged |
| Consumed image inspection | Both images decoded/visually inspected; current hashes equal their lineage record | Accurate existing summary graphics retained; no generated scientific figure or screenshot substitution |

## Browser and link checks

The affected flow is README publication metadata → generated read-only snapshot
→ shared repository-status rendering. It has no new API, database write or
external service call. Existing browser checks passed on development and the
production build at desktop 1280×800 and mobile 390×844: visible content,
zero console/page errors, no horizontal overflow or development/build baseline
divergence. All four screenshots were visually inspected. The existing research
browser smoke passed at both sizes across `/research`, `/projection` and
`/registry`, verifying the updated source digest, publication links and declared
gates; both provenance-detail screenshots were also inspected.

The production preview served `/og.jpg` with exactly the traced 162,507 bytes and
SHA-256 `1a737c65a2dae2b027ffa5da101de5b92f3c48e2a0c503311ed719197521322f`.
The first browser launch needed missing NSPR/NSS/ALSA libraries; these were
unpacked into an isolated temporary directory before the successful checks.
A metadata probe incorrectly expected an absolute loopback social-card URL;
the source deliberately omits public-host image metadata on loopback. A subsequent
simulated public Host header was rejected with HTTP 403 by preview host checks.
Those checks were preserved. Public-host metadata behavior has existing unit
coverage, but a live hosted social-card metadata response was not verified here.

The 142 local documentation/image links checked successfully. Hosted Vercel revision, live sky tiles,
authenticated SciServer behavior and durable storage round trips are outside
this validation. The existing sky browser smoke uses a deterministic Aladin API
spy and cannot establish availability of external sky imagery.

All local Markdown links in changed documentation and the package are checked
against actual checkout paths, including percent-encoded targets and images.
Package checksums cover every package member except the checksum file itself.
Reviewed difference checks additionally require the entire scientific/historical
control surface to remain unchanged and the snapshot's semantic content to
match baseline after removing only README hash/size and aggregate digest.

## Remote checks and explicit limits

At audit time the baseline main commit had successful GitHub runs including
S.T.A.R. CI, Tests, CodeQL, STARMAP, notebook smoke, sky pipeline, A03 reference
verification and the image build. These are **baseline** observations and do
not establish this PR's checks. Read the final PR-head check URLs/results in
the PR description/discussion; a later correction invalidates older-head status.
Dedicated path-filtered SciServer workflows may not be triggered by this
documentation PR; their existing offline tests were run locally as shown above.
No workflow was manually dispatched by this task.

The full Python/Sage suite and nine notebook smoke jobs were not run locally;
remote CI coverage and its exact commit must be reported separately. No
scientific transaction or historical program was executed locally. DOI resolver
access failed for the four repository-recorded archive IDs; no Zenodo deposit
metadata or bytes were authenticated. Review identity, authorship independence,
private-key isolation and actual runtime trust enforcement remain unverified.
See [REVIEW.md](REVIEW.md) for the remaining specialist and operational gaps.
