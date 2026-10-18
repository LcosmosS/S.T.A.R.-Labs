"""Human-approval security boundary tests; temporary keys, no network."""
import copy
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from integrations.sciserver import approval_policy as ap
from integrations.sciserver import query_policy, receipts


def stamp(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


@pytest.fixture
def context(tmp_path, monkeypatch):
    root = tmp_path / "runs"
    prepared = query_policy.prepare_casjobs_run(
        "DR18-CANARY-10", state_root=root
    )
    private = Ed25519PrivateKey.generate()
    public = private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    trust = {
        "approver_id": "offline-operator",
        "key_id": "ed25519:" + hashlib.sha256(public).hexdigest(),
        "public_key_hex": public.hex(),
    }
    monkeypatch.setattr(ap, "_trusted_manifest", lambda: trust)
    monkeypatch.setattr(ap, "_source_commit", lambda: "a" * 40)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    plan = prepared["plan"]
    grant = {
        "schema_version": ap.SCHEMA,
        "decision": "approve_single_dr18_canary_submission",
        "nonce": "d" * 32,
        "run_id": plan["run_id"],
        "query_id": plan["query_id"],
        "dataset_id": plan["dataset_id"],
        "context": plan["context"],
        "sql_sha256": plan["source_sql_sha256"],
        "catalog_sha256": plan["catalog_sha256"],
        "mydb_destination": plan["mydb_destination"],
        "planned_receipt_sha256": prepared["receipt_sha256"],
        "plan_sha256": hashlib.sha256(ap._canonical(plan)).hexdigest(),
        "source_commit_sha": "a" * 40,
        "approver_id": trust["approver_id"],
        "issued_at_utc": stamp(now - timedelta(minutes=2)),
        "expires_at_utc": stamp(now + timedelta(minutes=20)),
    }
    path = tmp_path / "signed_bundle.json"

    def sign(grant_data=None, signing_key=None, key_id=None):
        body = copy.deepcopy(grant if grant_data is None else grant_data)
        key = signing_key or private
        bundle = {
            "grant": body,
            "signature": {
                "algorithm": "Ed25519",
                "key_id": key_id or trust["key_id"],
                "signature_hex": key.sign(ap._canonical(body)).hex(),
            },
        }
        path.write_text(json.dumps(bundle), encoding="utf-8")
        return path

    sign()
    return {
        "root": root, "prepared": prepared, "plan": plan,
        "grant": grant, "private": private,
        "trust": trust, "path": path, "sign": sign,
        "now": now,
    }


def verify(ctx):
    return ap.verify_operator_approval(
        ctx["plan"]["run_id"], ctx["path"], state_root=ctx["root"]
    )


def test_trust_enrollment_shipped_disabled():
    manifest = json.loads(ap.TRUST_FILE.read_text(encoding="utf-8"))
    assert manifest == {
        "schema_version": ap.TRUST_SCHEMA,
        "activation_enabled": False,
        "public_keys": [],
    }
    with pytest.raises(ap.ApprovalRejected, match="disabled"):
        ap._trusted_manifest.__wrapped__() if hasattr(
            ap._trusted_manifest, "__wrapped__"
        ) else ap._trusted_manifest()


def test_valid_signed_grant_verifies_but_submission_remains_disabled(context):
    result = verify(context)
    assert result["signature_valid"] is True
    assert result["remote_submission_enabled"] is False
    assert result["planned_receipt_sha256"] == context["prepared"]["receipt_sha256"]
    with pytest.raises(PermissionError):
        query_policy.require_submission_authorization(result)


def test_signed_grant_recorded_once_without_execution(context):
    c = context
    first = ap.record_operator_approval(
        c["plan"]["run_id"], c["path"], state_root=c["root"]
    )
    assert first["event_type"] == "operator_approved"
    assert first["data"]["remote_submission_enabled"] is False
    assert first["data"]["signature_verified_at_recording"] is True
    assert first["data"]["signed_grant"]["run_id"] == c["plan"]["run_id"]
    assert len(receipts.read_events(c["root"], c["plan"]["run_id"])) == 2
    with pytest.raises(ap.ApprovalRejected, match="unused planned"):
        ap.record_operator_approval(
            c["plan"]["run_id"], c["path"], state_root=c["root"]
        )
    with pytest.raises(PermissionError):
        query_policy.require_submission_authorization(first)


def test_public_signing_key_does_not_escape_test(context):
    assert context["path"].is_file()
    assert not (Path(__file__).parent / "approver-private.pem").exists()


@pytest.mark.parametrize("name,replacement", [
    ("query_id", "DR18-DETERMINISTIC-200K"),
    ("context", "MyDB"),
    ("dataset_id", "DATA-OTHER"),
    ("sql_sha256", "0" * 64),
    ("catalog_sha256", "1" * 64),
    ("mydb_destination", "mydb.MyTable"),
    ("run_id", "b" * 32),
    ("planned_receipt_sha256", "0" * 64),
    ("plan_sha256", "f" * 64),
    ("source_commit_sha", "b" * 40),
    ("approver_id", "other-operator"),
    ("decision", "approve_any_query"),
])
def test_signed_but_modified_authority_is_rejected(context, name, replacement):
    grant = dict(context["grant"], **{name: replacement})
    context["sign"](grant)
    with pytest.raises(ap.ApprovalRejected, match="exact reviewed plan"):
        verify(context)


def test_signature_tampering_fails(context):
    data = json.loads(context["path"].read_text())
    data["signature"]["signature_hex"] = "0" * 128
    context["path"].write_text(json.dumps(data))
    with pytest.raises(ap.ApprovalRejected, match="signature is invalid"):
        verify(context)


def test_untrusted_signer_fails(context):
    other = Ed25519PrivateKey.generate()
    context["sign"](signing_key=other)
    with pytest.raises(ap.ApprovalRejected, match="signature is invalid"):
        verify(context)


def test_wrong_key_fingerprint_fails(context):
    context["sign"](key_id="ed25519:" + "0" * 64)
    with pytest.raises(ap.ApprovalRejected, match="signature descriptor"):
        verify(context)


@pytest.mark.parametrize("key", [
    "expires_at_utc", "issued_at_utc"
])
def test_expired_or_future_grants_fail(context, key):
    grant = dict(context["grant"])
    if key == "expires_at_utc":
        grant["expires_at_utc"] = stamp(context["now"] - timedelta(seconds=1))
    else:
        grant["issued_at_utc"] = stamp(context["now"] + timedelta(minutes=1))
    context["sign"](grant)
    with pytest.raises(ap.ApprovalRejected, match="not yet valid or expired"):
        verify(context)


def test_overlong_grant_lifetime_fails(context):
    grant = dict(context["grant"])
    grant["expires_at_utc"] = stamp(context["now"] + timedelta(days=2))
    context["sign"](grant)
    with pytest.raises(ap.ApprovalRejected, match="24 hours"):
        verify(context)


@pytest.mark.parametrize("field", ["nonce", "signature"])
def test_missing_fields_fail_closed(context, field):
    if field == "nonce":
        data = json.loads(context["path"].read_text())
        del data["grant"]["nonce"]
    else:
        data = json.loads(context["path"].read_text())
        del data["signature"]
    context["path"].write_text(json.dumps(data))
    with pytest.raises(ap.ApprovalRejected):
        verify(context)


def test_approval_file_symlink_rejected(context):
    real = context["path"]
    alias = real.parent / "alias.json"
    alias.symlink_to(real)
    with pytest.raises(OSError):
        ap.verify_operator_approval(
            context["plan"]["run_id"], alias, state_root=context["root"]
        )


def test_approval_file_large_rejected(context):
    context["path"].write_bytes(b" " * (ap.MAX_BUNDLE_BYTES + 1))
    with pytest.raises(ap.ApprovalRejected, match="bounded"):
        verify(context)


def test_forged_local_approval_event_cannot_authorize_remote(context):
    c = context
    receipts.append_event(
        c["root"], c["plan"]["run_id"], "operator_approved",
        {"forged_by_agent": True},
        expected_previous_sha256=c["prepared"]["receipt_sha256"],
    )
    with pytest.raises(ap.ApprovalRejected, match="unused planned"):
        verify(c)
    with pytest.raises(PermissionError):
        query_policy.require_submission_authorization()


def test_replay_for_another_plan_fails(context, tmp_path):
    other = query_policy.prepare_casjobs_run(
        "DR18-CANARY-10", state_root=context["root"]
    )
    with pytest.raises(ap.ApprovalRejected, match="exact reviewed plan"):
        ap.verify_operator_approval(
            other["plan"]["run_id"], context["path"],
            state_root=context["root"],
        )


def test_reviewed_commit_is_required(context, monkeypatch):
    monkeypatch.setattr(ap, "_source_commit", lambda: "c" * 40)
    with pytest.raises(ap.ApprovalRejected, match="exact reviewed plan"):
        verify(context)


def test_signature_enrollment_disabled_even_with_bundle(context, monkeypatch):
    monkeypatch.setattr(ap, "_trusted_manifest",
                        lambda: (_ for _ in ()).throw(
                            ap.ApprovalRejected("No independently enrolled operator keys: disabled")
                        ))
    with pytest.raises(ap.ApprovalRejected, match="disabled"):
        verify(context)


def test_trust_manifest_rejects_self_enrollment(context, monkeypatch):
    # No runtime input accepts a different trust path or a supplied public key.
    assert "trust_path" not in ap.verify_operator_approval.__code__.co_varnames
    assert "public_key" not in ap.verify_operator_approval.__code__.co_varnames
    assert not hasattr(ap, "sign_approval")
    assert not hasattr(ap, "submit_approved_job")
