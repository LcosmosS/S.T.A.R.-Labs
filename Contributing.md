# Contributing to S.T.A.R. Labs

Start with the [collaboration invitation](release_packages/STAR-collaboration-invitation-v0.1/README.md)
and select one [task](release_packages/STAR-collaboration-invitation-v0.1/TASKS.md).
Criticism, counterexamples, null results and reproducibility failures are useful
contributions. The governing authority is the [full Charter PDF](charter/STAR_Research_Charter_v0-2.pdf);
the [Markdown digest](charter/RESEARCH_CHARTER_v0.2.md) is a reading aid.
Follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Propose a bounded contribution

Open a public issue or reply to the collaboration issue with the task ID,
your relevant expertise, proposed files, deliverable, independence/conflict
statement and validation plan. Use [this review report template](release_packages/STAR-collaboration-invitation-v0.1/REVIEW_REPORT_TEMPLATE.md).
Issue participation and a passing check do not grant authority to activate an
experiment, promote a claim, admit a sky overlay or enroll a signing key.
Report vulnerabilities privately under [SECURITY.md](SECURITY.md); do not post
credentials, tokens, private keys, personal data or exploit details in issues.
The audit records a security-contact ambiguity for maintainer resolution.

## Inspect a fixed revision first

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/LcosmosS/S.T.A.R.-Labs.git
cd S.T.A.R.-Labs
git switch --detach d69868e3c1d9ae70944deb239369e53a9ecc1e5b
git rev-parse HEAD
git status --short
```

This is the invitation's audited baseline, not a promise that main is unchanged.
For a contribution, fetch current main, inspect differences from that baseline,
then create your own branch. Do not edit main directly. Do not initialize every
submodule or download all LFS data by default. Git LFS pointers are not payloads;
fetch only the exact objects required by the chosen review. Record both the
pointer's declared digest and the actual downloaded payload digest.

## Software setup and checks

Python **3.12+** is required by `pyproject.toml`. Use a clean virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

Install additional tools explicitly when required by the selected tests; for
example, the dedicated offline SciServer approval job installs
`cryptography>=42,<47`. SageMath is required for the nine-notebook smoke job;
consult [.github/workflows/notebooks.yml](.github/workflows/notebooks.yml).
Dependency installation is software setup, not permission to execute research.

Documentation/gate review can use these read-only commands without installing
the full scientific environment:

```bash
python scripts/independent_gate_report.py
python scripts/independent_dataset_verification.py --format markdown
git diff --check
```

Saved A01 archive inspection is separate from rerunning its experiment:

```bash
python release_packages/EXP-MAP-A01-primary-execution-v0.1/verify_package.py
```

That verifier needs the recorded source commit available in Git history.
See its [package instructions](release_packages/EXP-MAP-A01-primary-execution-v0.1/README.md).
It does not independently authenticate the original execution or regenerate
the cohort, graph or permutations.

For software changes, run the tests relevant to the changed behavior, then the
required CI suite. `pytest -q` is the main software suite; some provenance tests
require specifically hydrated archival objects. A failure due to missing bytes
must be reported, not hidden or replaced with fabricated data. No blanket
historical notebook execution is part of onboarding. The canonical notebook
smoke set is only the nine files enumerated in `notebooks.yml`; do not run
`examples/full_cosmology_inference.ipynb` or historical scripts as a setup check.
Registered experiment transactions and live survey/database requests require
their separately reviewed scope and applicable authorization.

For web contributions, use Node 24 (matching CI), then follow
[web_tool/README.md](web_tool/README.md). After intentional README publication
changes, run `npm run registry:sync` and `npm run registry:check` inside
`web_tool`; inspect the generated diff. Only source metadata/digests should
change when canonical scientific records are unchanged. Required admitted-sky
source bytes must be hydrated before `sky:check` or a production build.

## Preserve the research record

- Keep namespace-qualified claim, experiment, dataset, parameter and null IDs.
  Same strings across PDF/audit/repository namespaces are not aliases.
- Preserve historical files, frozen release packages, source SQL, received logs,
  manifests, provenance and negative results byte-for-byte. Put corrections in
  dated companion records or a separate reviewed successor.
- Separate archival intake, registry reconciliation, quarantine changes and
  executable changes into reviewable commits or PRs. CI captures belong in
  artifacts; CI must not rewrite the research source of record.
- Distinguish source identity, software validation, primary execution,
  independent reproduction, execution eligibility, controlled support, physical
  support and display admission. No implicit promotion between these gates.
- Record dependencies, environment, seeds, hashes, all outcomes and limitations.
  Post-hoc choices cannot be retrospectively preregistered. Invalid protocol or
  missing data is ineligible/inconclusive, not a scientific negative finding.
- Preserve the disabled SciServer trust/catalog/submission settings. An operator
  private key must be generated and held outside Codex/MCP access. A future grant
  must bind the actual reviewed deployment commit after any squash merge;
  feature-branch approval does not transfer to a different commit.

## Submit a pull request

State the concrete problem, task ID, exact baseline/head commits, changed paths,
validation commands and outcomes, skipped or unavailable checks, and remaining
independent verification. Explain any scientific-status impact explicitly.
Keep generated evidence separate from software fixtures and screenshots.
A maintainer reviews scope and integrity; an accountable reviewer with relevant
expertise reviews any proposed scientific or authorization transition separately.
Inspect checks on the final PR head after every correction; local success and
old-head CI do not establish current-head CI success.

Use Black (88-column configuration in `pyproject.toml`) for changed Python code,
explicit Sage imports where needed, and meaningful docstrings. Do not reformat
frozen evidence. Documentation-only changes need link, citation and difference
checks rather than unnecessary notebook execution.

## Citation, licensing and credit

Follow [CITATION.cff](CITATION.cff) and the [citation guide](release_packages/STAR-collaboration-invitation-v0.1/CITATION_GUIDE.md).
The repository [MIT license](LICENSE) does not replace upstream catalog,
publication or third-party asset terms. Record source licenses and required
acknowledgments before redistribution. Credit contributions accurately; discuss
authorship based on actual contributions before submitting a manuscript.
Participation, review or a merged PR does not automatically confer co-authorship,
independence certification or endorsement. Track credit in the relevant PR and
review receipt; no nonexistent AUTHORS file or publication outcome is promised.
