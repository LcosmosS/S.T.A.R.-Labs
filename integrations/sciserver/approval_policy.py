"""Offline verification of independently signed SciServer TOP 10 canary approvals.

No signer, remote submission, approval MCP tool, or CasJobs API is provided.
An operator key is *not* registered in this PR: trust enrollment is closed.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import query_policy, receipts

SCHEMA = "star-sciserver-human-approval-v0.2"
TRUST_SCHEMA = "star-sciserver-approver-trust-v0.2"
TRUST_FILE = Path(__file__).with_name("trusted_approvers.json")
MAX_BUNDLE_BYTES = 8192
SOURCE_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
HEX_RE = re.compile(r"^[0-9a-f]{64}$")
NONCE_RE = re.compile(r"^[0-9a-f]{32}$")
APPROVER_ID_RE = re.compile(r"^[a-z][a-z0-9_-]{2,47}$")
KEY_ID_RE = re.compile(r"^ed25519:[0-9a-f]{64}$")
UTC_TIME_RE = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
GRANT_FIELDS = frozenset({
    "schema_version", "decision", "nonce", "run_id", "query_id",
    "dataset_id", "context", "sql_sha256", "catalog_sha256",
    "mydb_destination", "planned_receipt_sha256", "plan_sha256",
    "source_commit_sha", "approver_id", "issued_at_utc", "expires_at_utc",
})


class ApprovalRejected(ValueError):
    """Cryptographic, contextual or lifecycle approval failure."""


def _canonical(obj: dict) -> bytes:
    return (json.dumps(obj, sort_keys=True, ensure_ascii=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")


def _read_file(path: Path, max_bytes: int) -> bytes:
    if os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
        raise ApprovalRejected("Approval validation requires POSIX/WSL2")
    path = Path(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > max_bytes:
            raise ApprovalRejected("Approval input must be a bounded regular file")
        with os.fdopen(fd, "rb") as file:
            fd = -1
            content = file.read(max_bytes + 1)
        if len(content) > max_bytes:
            raise ApprovalRejected("Approval input too large")
        return content
    finally:
        if fd >= 0:
            os.close(fd)


def _parse_json(raw: bytes) -> dict:
    try:
        data = json.loads(raw)
    except (UnicodeDecodeError, ValueError) as exc:
        raise ApprovalRejected("Invalid approval JSON") from exc
    if not isinstance(data, dict):
        raise ApprovalRejected("Approval must be a JSON object")
    return data


def _trusted_manifest() -> dict:
    """Read only the fixed, repository-shipped trust file; never caller-provided."""
    manifest = _parse_json(_read_file(TRUST_FILE, MAX_BUNDLE_BYTES))
    if set(manifest) != {"schema_version", "activation_enabled", "public_keys"}:
        raise ApprovalRejected("Unrecognized trust manifest fields")
    if manifest["schema_version"] != TRUST_SCHEMA:
        raise ApprovalRejected("Trust manifest version mismatch")
    if manifest["activation_enabled"] is not True:
        raise ApprovalRejected("No independently enrolled operator keys: disabled")
    keys = manifest["public_keys"]
    if not isinstance(keys, list) or len(keys) != 1:
        raise ApprovalRejected("Exactly one reviewed operator key is required")
    key = keys[0]
    if not isinstance(key, dict) or set(key) != {
        "approver_id", "key_id", "public_key_hex"
    }:
        raise ApprovalRejected("Malformed trust entry")
    if (not isinstance(key["approver_id"], str) or
            not APPROVER_ID_RE.fullmatch(key["approver_id"])):
        raise ApprovalRejected("Invalid operator identifier")
    if (not isinstance(key["public_key_hex"], str) or
            not HEX_RE.fullmatch(key["public_key_hex"])):
        raise ApprovalRejected("Invalid operator public key")
    public_bytes = bytes.fromhex(key["public_key_hex"])
    expected_key_id = "ed25519:" + hashlib.sha256(public_bytes).hexdigest()
    if key["key_id"] != expected_key_id:
        raise ApprovalRejected("Operator key fingerprint mismatch")
    return key


def _source_commit() -> str:
    """Bind the approval to a concrete checked-out repository commit."""
    try:
        run = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            cwd=query_policy.REPO_ROOT, capture_output=True,
            text=True, timeout=5, check=True,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ApprovalRejected("Unable to resolve source commit") from exc
    sha = run.stdout.strip()
    if not SOURCE_SHA_RE.fullmatch(sha):
        raise ApprovalRejected("Invalid repository commit")
    return sha


def _instant(value: object) -> datetime:
    if not isinstance(value, str) or not UTC_TIME_RE.fullmatch(value):
        raise ApprovalRejected("Timestamps must use UTC seconds and Z")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ApprovalRejected("Invalid approval timestamp") from exc


def _check_grant(
    grant: dict, *,
    plan: dict,
    planned_sha: str,
    catalog_sha: str,
    source_commit: str,
    approver_id: str,
    now: datetime,
) -> None:
    if set(grant) != GRANT_FIELDS:
        raise ApprovalRejected("Approval grant fields are not exact")
    expected = {
        "schema_version": SCHEMA,
        "decision": "approve_single_dr18_canary_submission",
        "run_id": plan["run_id"],
        "query_id": "DR18-CANARY-10",
        "dataset_id": "DATA-SDSS18-200K",
        "context": "DR18",
        "sql_sha256": plan["source_sql_sha256"],
        "catalog_sha256": catalog_sha,
        "mydb_destination": plan["mydb_destination"],
        "planned_receipt_sha256": planned_sha,
        "plan_sha256": hashlib.sha256(_canonical(plan)).hexdigest(),
        "source_commit_sha": source_commit,
        "approver_id": approver_id,
    }
    if any(grant.get(name) != value for name, value in expected.items()):
        raise ApprovalRejected("Signed grant does not match the exact reviewed plan")
    if not isinstance(grant["nonce"], str) or not NONCE_RE.fullmatch(grant["nonce"]):
        raise ApprovalRejected("Approval nonce must be 128-bit hex")
    issued = _instant(grant["issued_at_utc"])
    expires = _instant(grant["expires_at_utc"])
    if expires <= issued or expires - issued > timedelta(hours=24):
        raise ApprovalRejected("Approval validity must be at most 24 hours")
    if now < issued or now >= expires:
        raise ApprovalRejected("Approval not yet valid or expired")


def _validated_grant(
    run_id: str,
    bundle_path: Path,
    state_root: Path,
) -> tuple[dict, dict, dict]:
    """All checks use the fixed trust file, current Git HEAD, and frozen catalog."""
    events = receipts.read_events(state_root, run_id)
    if len(events) != 1 or events[0]["event_type"] != "planned":
        raise ApprovalRejected("Approval must apply to an unused planned run")
    planned = events[0]
    plan = planned["data"]
    if not isinstance(plan, dict) or plan.get("run_id") != run_id:
        raise ApprovalRejected("Plan does not match requested run")
    catalog = query_policy.load_catalog()
    row = catalog["queries"].get("DR18-CANARY-10")
    if (
        plan.get("schema_version") != query_policy.PLAN_SCHEMA
        or plan.get("query_id") != "DR18-CANARY-10"
        or plan.get("dataset_id") != row["dataset_id"]
        or plan.get("context") != row["context"]
        or plan.get("mode") != "canary"
        or plan.get("source_sql_path") != row["path"]
        or plan.get("source_sql_sha256") != row["approved_sha256"]
        or plan.get("catalog_sha256") != catalog["catalog_sha256"]
        or plan.get("max_rows") != 10
        or plan.get("expected_columns") != 18
        or plan.get("operator_approval_recorded") is not False
        or plan.get("remote_submission_enabled") is not False
        or plan.get("automatic_registry_promotion") is not False
        or plan.get("historical_dataset_replacement") is not False
    ):
        raise ApprovalRejected("Plan no longer matches frozen preparation policy")
    query_policy.validate_destination(
        run_id, "canary", plan["mydb_destination"]
    )
    trust = _trusted_manifest()  # Fails closed: no keys enrolled in this PR.
    bundle = _parse_json(_read_file(bundle_path, MAX_BUNDLE_BYTES))
    if set(bundle) != {"grant", "signature"}:
        raise ApprovalRejected("Invalid signed approval bundle shape")
    grant, signature = bundle["grant"], bundle["signature"]
    if not isinstance(grant, dict) or not isinstance(signature, dict):
        raise ApprovalRejected("Invalid approval types")
    if set(signature) != {"algorithm", "key_id", "signature_hex"}:
        raise ApprovalRejected("Invalid signature fields")
    if (signature["algorithm"] != "Ed25519" or
            signature["key_id"] != trust["key_id"] or
            not isinstance(signature["signature_hex"], str) or
            not re.fullmatch(r"[0-9a-f]{128}", signature["signature_hex"])):
        raise ApprovalRejected("Untrusted or invalid signature descriptor")
    _check_grant(
        grant, plan=plan, planned_sha=planned["record_sha256"],
        catalog_sha=catalog["catalog_sha256"],
        source_commit=_source_commit(), approver_id=trust["approver_id"],
        now=datetime.now(timezone.utc),
    )
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PublicKey,
        )
    except ImportError as exc:
        raise ApprovalRejected(
            "Install the optional sciserver-approval dependencies"
        ) from exc
    try:
        Ed25519PublicKey.from_public_bytes(
            bytes.fromhex(trust["public_key_hex"])
        ).verify(bytes.fromhex(signature["signature_hex"]), _canonical(grant))
    except (InvalidSignature, ValueError) as exc:
        raise ApprovalRejected("Approval signature is invalid") from exc
    return grant, bundle, planned


def verify_operator_approval(
    run_id: str, bundle_path: Path, *,
    state_root: Path = receipts.DEFAULT_STATE_ROOT,
) -> dict:
    """Validate a signed canary approval WITHOUT granting remote execution."""
    grant, bundle, planned = _validated_grant(run_id, bundle_path, state_root)
    return {
        "run_id": run_id,
        "grant_sha256": hashlib.sha256(_canonical(grant)).hexdigest(),
        "bundle_sha256": hashlib.sha256(_canonical(bundle)).hexdigest(),
        "planned_receipt_sha256": planned["record_sha256"],
        "signature_valid": True,
        "remote_submission_enabled": False,
    }


def record_operator_approval(
    run_id: str, bundle_path: Path, *,
    state_root: Path = receipts.DEFAULT_STATE_ROOT,
) -> dict:
    """Append signed evidence once; NEVER interpret a receipt as authorization.

    Any later submitter MUST re-verify the signature and cannot rely solely on
    an 'operator_approved' event (which local callers can also fabricate).
    """
    grant, bundle, planned = _validated_grant(run_id, bundle_path, state_root)
    evidence = {
        "signed_grant": grant,
        "signature": bundle["signature"],
        "bundle_sha256": hashlib.sha256(_canonical(bundle)).hexdigest(),
        "signature_verified_at_recording": True,
        "remote_submission_enabled": False,
    }
    return receipts.append_event(
        state_root, run_id, "operator_approved", evidence,
        expected_previous_sha256=planned["record_sha256"],
    )
