# SciServer v0.2 — Phase 2 human-authorization boundary (verification only)

**Status: NOT ACTIVATED. No operator key is enrolled; all signed approvals fail
closed. No remote CasJobs job submission, MyDB creation, or live canary occurs
in this PR.**

## Authority model

The existing `integrations/sciserver/query_policy.py` remains unchanged.
`require_submission_authorization()` still unconditionally raises
`PermissionError`; the existing read-only MCP `server.py` remains unchanged.
This PR adds the standalone, **offline-only** module `approval_policy.py`:

- `verify_operator_approval(run_id, signed_bundle_file, state_root=...)`:
  returns a validation summary but does not write an approval receipt.
- `record_operator_approval(run_id, signed_bundle_file, state_root=...)`:
  checks the same signature and atomically appends one `operator_approved`
  event to the existing local hash chain. It makes **no remote calls**.

The signature mechanism uses Ed25519. The code does **not** implement or
expose signing, key generation, a remote-execution adapter, generic SQL,
a token source, or an MCP approval tool.

## Independent trust and key enrollment

`integrations/sciserver/trusted_approvers.json` is an explicit review
checkpoint. **This PR commits `activation_enabled=false` and an empty key
list.** Thus the verification API cannot approve anything in the deployed
branch. This is intentional, not a missing automated step.

For genuine independence, a designated human operator must generate and
retain the Ed25519 **private key on a separately administered device/account**
that the Codex/MCP process cannot access. The operator must separately review
and register ONLY the corresponding hex-encoded 32-byte **public key**, its
SHA-256-derived `ed25519:<digest>` key ID, and the operator identifier in a
dedicated, reviewed trust-enrollment PR. That PR must independently authorize
the change from `activation_enabled=false` to `true`.

A public key being checked into a repository is not, by itself, a security
boundary if the running agent can modify its trusted copy. The eventual
submission process must use a separately trusted runtime/checked-out release
or externally pinned trust-manifest digest and an independently controlled
approval/signing environment. Any verifier or input which allows a caller
to substitute an arbitrary trust-manifest path is prohibited.

Do not upload, print, commit or paste the private signing key. A reviewer
must not ask Codex to generate or operate the signing key.

## Signed approval bundle (v0.2)

The signed bundle has exactly two fields:
`{"grant": {...}, "signature": {...}}`.
The signature object contains `algorithm="Ed25519"`,
`key_id="ed25519:<sha256-of-public-key>"` and
`signature_hex="<128-lowercase-hex-chars>"`.

The `grant` object has exactly these fields:

- `schema_version="star-sciserver-human-approval-v0.2"`;
- `decision="approve_single_dr18_canary_submission"`;
- `nonce`: independently generated 16 random bytes as 32 lowercase hex;
- `run_id`, `query_id="DR18-CANARY-10"`,
  `dataset_id="DATA-SDSS18-200K"`, `context="DR18"`;
- `sql_sha256`, `catalog_sha256`, `mydb_destination`;
- `planned_receipt_sha256`, `plan_sha256`;
- `source_commit_sha` (exact 40-hex SHA of the checked-out reviewer-approved
  source commit), `approver_id`;
- `issued_at_utc`, `expires_at_utc` in whole-second `Z` UTC format.

The signature covers this entire `grant` encoded as sorted-key
ASCII JSON using separators `(",", ":")`, with `ensure_ascii=True`
and **one final newline byte**. The field
`plan_sha256 = SHA256(canonical_plan_json)` uses the identical encoding.

The verifier rejects unknown keys, missing fields, mismatched run ID/SQL
hash/catalog/context/destination/dataset/plan receipt/source commit,
expired or future-dated grants, a lifespan over 24 hours, invalid signatures,
and attempts to approve a run after its initial `planned` event.
The nonce is bound to the unique run ID by the signature; a recorded approval
cannot be applied to another run.

A locally appended `operator_approved` event is **not** an authorization
by itself. The existing receipt machinery allows untrusted local code to
write such an event, and an attacker with filesystem write permission can
rewrite an unanchored history. A later live submission process MUST
independently re-verify signed approval material, review the signed source
commit, ensure one-time consumption and MyDB destination absence, and fail
closed on network ambiguity. Signature validation in this PR does not
perform these later steps.

## Deliberately disabled paths

No async CasJobs job is submitted. No SQL query is run by the new module.
No approval is accepted while no operator trust anchor is enrolled.
The v0.2 global catalog and both per-query `submission_enabled` flags
remain `false`. The deterministic 200K probe remains blocked.
There is no database-write MCP interface, no automatic scientific registry
promotion, no modification to the frozen historical LFS CSV or source SQL.
The first live TOP 10 canary needs a **separate, explicit human authorization
and reviewed PR after trust enrollment and verification**.

## Tests

```bash
python -m pip install "cryptography>=42,<47"
python -m pytest -q tests/integrations/test_sciserver_approval.py
python -m pytest -q tests/integrations/test_sciserver_policy.py
git diff --check
```

Tests generate disposable private keys in temporary in-process fixtures ONLY;
none are persisted or shipped. No credentials and no network are used. The
test fixture mocks trust enrollment, never changes the committed disabled
trust manifest.
