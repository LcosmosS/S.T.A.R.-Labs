"""Regression tests for controlled-execution readiness gating."""

import csv

import pytest

from scripts.check_controlled_readiness import assess
from src.control.registry import RegistryError


def _write(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _registry_root(
    tmp_path,
    evidence_status,
    *,
    claim_ids="CLAIM-TEST",
    registered_claims=("CLAIM-TEST",),
    crosswalk_claims=("CLAIM-TEST",),
):
    registry = tmp_path / "registry"
    _write(
        registry / "experiment_registry_v0.2.csv",
        [
            "Experiment_ID",
            "Controlled_Execution_Eligible",
            "Mode",
            "Claim_IDs",
            "Namespace_Resolution",
            "Dataset_ID",
            "Parameter_Set_ID",
            "Null_ID",
        ],
        [
            {
                "Experiment_ID": "EXP-TEST",
                "Controlled_Execution_Eligible": "true",
                "Mode": "controlled",
                "Claim_IDs": claim_ids,
                "Namespace_Resolution": "explicit_non_alias",
                "Dataset_ID": "DATA-TEST",
                "Parameter_Set_ID": "PARAM-TEST",
                "Null_ID": "NULL-TEST",
            }
        ],
    )
    _write(
        registry / "claim_evidence_v0.2.csv",
        ["Claim_ID", "Controlled_Support_Eligible", "Physical_Support_Eligible"],
        [
            {
                "Claim_ID": claim_id,
                "Controlled_Support_Eligible": "false",
                "Physical_Support_Eligible": "false",
            }
            for claim_id in registered_claims
        ],
    )
    _write(
        registry / "claim_experiment_crosswalk_v0.2.csv",
        ["Claim_ID", "Experiment_ID"],
        [
            {"Claim_ID": claim_id, "Experiment_ID": "EXP-TEST"}
            for claim_id in crosswalk_claims
        ],
    )
    _write(
        registry / "dataset_registry_v0.1.csv",
        ["Dataset_ID", "Controlled_Execution_Eligible"],
        [{"Dataset_ID": "DATA-TEST", "Controlled_Execution_Eligible": "true"}],
    )
    _write(
        registry / "data_provenance_registry_v0.1.csv",
        ["Dataset_ID", "Provenance_Status", "Evidence_Status", "Integrity_Check"],
        [
            {
                "Dataset_ID": "DATA-TEST",
                "Provenance_Status": "verified",
                "Evidence_Status": evidence_status,
                "Integrity_Check": "SHA256=" + "a" * 64,
            }
        ],
    )
    _write(
        registry / "parameter_registry_v0.1.csv",
        ["Parameter_Set_ID", "Preregistration_Status"],
        [{"Parameter_Set_ID": "PARAM-TEST", "Preregistration_Status": "locked"}],
    )
    _write(
        registry / "null_registry_v0.1.csv",
        ["Null_ID", "Preregistration_Status"],
        [{"Null_ID": "NULL-TEST", "Preregistration_Status": "preregistered"}],
    )
    return tmp_path


@pytest.mark.parametrize("evidence_status", ["", "unknown", "exploratory", "invented"])
def test_readiness_rejects_missing_or_unaccepted_evidence_status(
    tmp_path, evidence_status
):
    root = _registry_root(tmp_path, evidence_status)
    claimed, failures = assess(root)

    assert claimed == ["EXP-TEST"]
    assert any("evidence status" in failure for failure in failures)


@pytest.mark.parametrize("evidence_status", ["controlled", "derived"])
def test_readiness_accepts_explicit_ready_evidence_statuses(tmp_path, evidence_status):
    root = _registry_root(tmp_path, evidence_status)
    claimed, failures = assess(root)

    assert claimed == ["EXP-TEST"]
    assert failures == []


def test_readiness_rejects_verified_provenance_without_sha256_integrity(tmp_path):
    root = _registry_root(tmp_path, "controlled")
    provenance = root / "registry" / "data_provenance_registry_v0.1.csv"
    _write(
        provenance,
        ["Dataset_ID", "Provenance_Status", "Evidence_Status", "Integrity_Check"],
        [
            {
                "Dataset_ID": "DATA-TEST",
                "Provenance_Status": "verified",
                "Evidence_Status": "controlled",
                "Integrity_Check": "",
            }
        ],
    )

    claimed, failures = assess(root)

    assert claimed == ["EXP-TEST"]
    assert any("no explicit SHA256" in failure for failure in failures)


def test_readiness_rejects_pending_namespace_resolution(tmp_path):
    root = _registry_root(tmp_path, "controlled")
    experiment = root / "registry" / "experiment_registry_v0.2.csv"
    _write(
        experiment,
        [
            "Experiment_ID",
            "Controlled_Execution_Eligible",
            "Mode",
            "Claim_IDs",
            "Namespace_Resolution",
            "Dataset_ID",
            "Parameter_Set_ID",
            "Null_ID",
        ],
        [
            {
                "Experiment_ID": "EXP-TEST",
                "Controlled_Execution_Eligible": "true",
                "Mode": "controlled",
                "Claim_IDs": "CLAIM-TEST",
                "Namespace_Resolution": "related_scope_protocol_review_pending_no_alias",
                "Dataset_ID": "DATA-TEST",
                "Parameter_Set_ID": "PARAM-TEST",
                "Null_ID": "NULL-TEST",
            }
        ],
    )

    claimed, failures = assess(root)

    assert claimed == ["EXP-TEST"]
    assert any("namespace resolution is not closed" in failure for failure in failures)


def test_readiness_rejects_missing_claim_binding(tmp_path):
    root = _registry_root(tmp_path, "controlled")
    experiment = root / "registry" / "experiment_registry_v0.2.csv"
    _write(
        experiment,
        [
            "Experiment_ID",
            "Controlled_Execution_Eligible",
            "Mode",
            "Claim_IDs",
            "Namespace_Resolution",
            "Dataset_ID",
            "Parameter_Set_ID",
            "Null_ID",
        ],
        [
            {
                "Experiment_ID": "EXP-TEST",
                "Controlled_Execution_Eligible": "true",
                "Mode": "controlled",
                "Claim_IDs": "",
                "Namespace_Resolution": "explicit_non_alias",
                "Dataset_ID": "DATA-TEST",
                "Parameter_Set_ID": "PARAM-TEST",
                "Null_ID": "NULL-TEST",
            }
        ],
    )

    claimed, failures = assess(root)

    assert claimed == ["EXP-TEST"]
    assert any("Claim_IDs must be explicitly bound" in failure for failure in failures)


@pytest.mark.parametrize(
    "claim_ids,message",
    [
        ("CLAIM-UNKNOWN", "unknown Claim_ID"),
        ("CLAIM-TEST;CLAIM-UNKNOWN", "unknown Claim_ID"),
        ("OTHER:CLAIM-TEST", "unknown Claim_ID"),
        ("CLAIM-TEST;", "contains an empty Claim_ID"),
        ("CLAIM-TEST;;CLAIM-TEST", "contains an empty Claim_ID"),
        ("CLAIM-TEST;CLAIM-TEST", "duplicate Claim_ID"),
    ],
)
def test_readiness_rejects_invalid_claim_ids(tmp_path, claim_ids, message):
    root = _registry_root(tmp_path, "controlled", claim_ids=claim_ids)

    claimed, failures = assess(root)

    assert claimed == ["EXP-TEST"]
    assert any(message in failure for failure in failures)


@pytest.mark.parametrize("claim_ids", ["CLAIM-OTHER", "CLAIM-TEST;CLAIM-OTHER"])
def test_readiness_rejects_known_claim_without_exact_crosswalk(tmp_path, claim_ids):
    root = _registry_root(
        tmp_path,
        "controlled",
        claim_ids=claim_ids,
        registered_claims=("CLAIM-TEST", "CLAIM-OTHER"),
    )

    claimed, failures = assess(root)

    assert claimed == ["EXP-TEST"]
    assert any(
        "missing claim/experiment crosswalk pair" in failure for failure in failures
    )


def test_readiness_accepts_multiple_registered_claim_pairs(tmp_path):
    root = _registry_root(
        tmp_path,
        "controlled",
        claim_ids="CLAIM-TEST; CLAIM-OTHER",
        registered_claims=("CLAIM-TEST", "CLAIM-OTHER"),
        crosswalk_claims=("CLAIM-TEST", "CLAIM-OTHER"),
    )

    claimed, failures = assess(root)

    assert claimed == ["EXP-TEST"]
    assert failures == []


@pytest.mark.parametrize(
    "filename", ["claim_evidence_v0.2.csv", "claim_experiment_crosswalk_v0.2.csv"]
)
def test_readiness_rejects_missing_claim_registry(tmp_path, filename):
    root = _registry_root(tmp_path, "controlled")
    (root / "registry" / filename).unlink()

    with pytest.raises(RegistryError, match="missing controlled registry file"):
        assess(root)


@pytest.mark.parametrize(
    "filename,content,message",
    [
        (
            "claim_evidence_v0.2.csv",
            "Claim_ID\nCLAIM-TEST\nCLAIM-TEST\n",
            "duplicate Claim_ID",
        ),
        (
            "claim_experiment_crosswalk_v0.2.csv",
            "Claim_ID\nCLAIM-TEST\n",
            "invalid registry headers",
        ),
    ],
)
def test_readiness_rejects_malformed_claim_registry(
    tmp_path, filename, content, message
):
    root = _registry_root(tmp_path, "controlled")
    (root / "registry" / filename).write_text(content, encoding="utf-8")

    with pytest.raises(RegistryError, match=message):
        assess(root)
