"""Regression tests for controlled-execution readiness gating."""

import csv

import pytest

from scripts.check_controlled_readiness import assess


def _write(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _registry_root(tmp_path, evidence_status):
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
                "Claim_IDs": "CLAIM-TEST",
                "Namespace_Resolution": "explicit_non_alias",
                "Dataset_ID": "DATA-TEST",
                "Parameter_Set_ID": "PARAM-TEST",
                "Null_ID": "NULL-TEST",
            }
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
