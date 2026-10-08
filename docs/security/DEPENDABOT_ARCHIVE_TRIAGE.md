# Archived environment Dependabot triage — 2026-10-08

Alerts #106–#110 refer to three immutable environment records under
`historical/r&d/docs/recovered_corpus_audit_2026-10-08/environment_dependency_revisions/`.
They preserve earlier dependency revisions, including vulnerable package versions;
they are not the requirements installed by current CI or Docker builds. Recovery
intake verifies their hashes without installing or executing their contents.

Do not update these files in place. Their bytes are bound by
[upstream_environment_integrity.json](../../historical/r&d/docs/recovered_corpus_audit_2026-10-08/upstream_environment_integrity.json).
All eight original/revision records were checked against their saved hashes and sizes.
The archived versions remain unsafe to install: review and create a separate patched
environment before any future reconstruction. Dismissal does not patch an archive
or authorize its execution.

The reported advisories are fixed in
[scikit-learn 1.5.0](https://github.com/advisories/GHSA-jw8x-6495-233v) and
[tqdm 4.66.3](https://github.com/tqdm/tqdm/security/advisories/GHSA-g7vv-2v7x-gj9p).
Root `requirements.txt` already pins those patched versions. A separate active
manifest, `RTCH_E1/requirements.txt`, allowed `scikit-learn>=1.4`; this change raises
the minimum to `>=1.5.0`. Experiment eligibility and scientific results are unchanged.

The five reviewed archive-only alerts qualify for the GitHub dismissal reason
`not_used`, with an alert-specific comment recording the file hash and this review.
Keep Dependabot monitoring enabled. Do not treat update exclusions, renamed files,
or this document as proof that an alert was closed. The machine-readable record
below reports the actual verified GitHub state after triage.

See [dependabot_archive_triage_2026-10-08.json](dependabot_archive_triage_2026-10-08.json)
for every alert, source path, SHA-256, advisory, and verified remote status.
