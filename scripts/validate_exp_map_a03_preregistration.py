"""Validate the locked EXP-MAP-A03 preregistration without executing it."""
from __future__ import annotations

import json
from pathlib import Path

from src.control.execution import PreflightError, preflight_controlled_experiment
from src.control.registry import RegistrySnapshot, file_sha256
from src.experiments.exp_map_a03 import (
    LOCKED_ANALYSIS_ROWS,
    LOCKED_J_ZERO_EXCLUSIONS,
    LOCKED_REPRESENTATIVES,
    LOCKED_SOURCE_ROWS,
    load_locked_arithmetic,
)


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "controlled_execution" / "specs" / "EXP-MAP-A03.json"
CONFIG = ROOT / "preregistrations" / "EXP-MAP-A03" / "config.json"
MANIFEST = ROOT / "preregistrations" / "EXP-MAP-A03" / "dataset_manifest.json"
PROTOCOL = ROOT / "preregistrations" / "EXP-MAP-A03" / "protocol.md"
SOURCE = ROOT / "data" / "ecdata" / "allcurves" / "allcurves.00000-09999"
SOURCE_SHA256 = "259f3846329395b371e8079c77a6f1097adaebc98a054974573e241416efa968"


def validate() -> None:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    protocol = PROTOCOL.read_text(encoding="utf-8")

    assert spec["experiment_id"] == config["experiment_id"] == "EXP-MAP-A03"
    assert config["claim_ids"] == ["CLAIM-ACSC-002"]
    assert config["dataset_id"] == "DATA-ARITHMETIC"
    assert config["parameter_set_id"] == "PAR-MAP-003"
    assert config["null_id"] == "NULL-MAP-003"
    assert spec["config"] == config

    snapshot = RegistrySnapshot.load(ROOT)
    resolved = snapshot.resolve("EXP-MAP-A03")
    assert resolved.experiment["Status"] == "preregistered"
    assert resolved.experiment["Claim_IDs"] == "CLAIM-ACSC-002"
    assert ("CLAIM-ACSC-002", "EXP-MAP-A03") in resolved.claim_experiments
    assert resolved.experiment["Namespace_Resolution"] == "scope_conflict_no_alias"
    assert resolved.experiment["Controlled_Execution_Eligible"] == "false"
    assert resolved.dataset["Controlled_Execution_Eligible"] == "false"
    assert resolved.experiment["Controlled_Support_Eligible"] == "false"
    assert resolved.experiment["Physical_Support_Eligible"] == "false"
    assert resolved.dataset["Controlled_Support_Eligible"] == "false"
    assert resolved.dataset["Physical_Support_Eligible"] == "false"
    assert resolved.provenance["Provenance_Status"] == "verified"
    assert resolved.provenance["Evidence_Status"] == "controlled"
    assert SOURCE_SHA256 in resolved.provenance["Integrity_Check"]
    assert resolved.parameter["Preregistration_Status"] == "locked"
    assert resolved.null["Preregistration_Status"] == "locked"
    assert spec["registry_bindings"] == resolved.record_hashes

    assert config["input"]["source_rows"] == LOCKED_SOURCE_ROWS == 64687
    assert config["input"]["representative_rows"] == LOCKED_REPRESENTATIVES == 38042
    assert config["input"]["j_zero_exclusions"] == LOCKED_J_ZERO_EXCLUSIONS == 106
    assert config["input"]["analysis_rows"] == LOCKED_ANALYSIS_ROWS == 37936
    assert config["endpoint"]["k"] == 10
    assert config["null"]["realizations"] == 999
    assert config["null"]["seed"] == 4103
    assert config["null"]["algorithm"] == "splitmix64-fisher-yates-v1"
    assert config["inference"]["alpha"] == 0.005
    assert config["inference"]["sidedness"] == "one_sided_greater"
    assert config["inference"]["primary_endpoint_count"] == 1
    assert config["outputs"] == spec["output_paths"]
    assert config["controls"] == {
        "controlled_execution_eligible": False,
        "controlled_support_eligible": False,
        "physical_support_eligible": False,
        "no_run_without_separate_activation": True,
    }

    assert manifest["artifact"]["sha256"] == SOURCE_SHA256
    assert manifest["artifact"]["expected_rows"] == 64687
    assert manifest["cohort"]["representative_rows"] == 38042
    assert manifest["cohort"]["expected_j_zero_exclusions"] == 106
    assert manifest["cohort"]["expected_analysis_rows"] == 37936
    assert manifest["cohort"]["post_hoc_filtering"] is False
    assert "no post-hoc filtering" in protocol.lower()
    assert "Controlled_Execution_Eligible=false" in protocol

    assert SOURCE.is_file(), "pinned ecdata submodule is not hydrated"
    assert file_sha256(SOURCE) == SOURCE_SHA256
    assert SOURCE.stat().st_size == 2146401
    frame, exclusions = load_locked_arithmetic(SOURCE, config)
    assert len(frame) == 37936
    assert len(exclusions) == 106
    assert list(exclusions.columns) == ["label", "isogeny_class", "conductor", "reason"]
    assert set(exclusions["reason"]) == {"j_exactly_zero"}

    prepared = preflight_controlled_experiment(
        ROOT,
        SPEC,
        require_execution_eligibility=False,
    )
    assert prepared.resolved.record_hashes == spec["registry_bindings"]
    assert prepared.resolved.experiment["Controlled_Execution_Eligible"] == "false"
    assert prepared.resolved.dataset["Controlled_Execution_Eligible"] == "false"

    try:
        preflight_controlled_experiment(ROOT, SPEC)
    except PreflightError as exc:
        assert "not controlled-execution eligible" in str(exc)
    else:
        raise AssertionError("normal execution preflight must remain closed for A03")

    print(
        "PASS: EXP-MAP-A03 preregistration bindings and deterministic 37,936-row "
        "cohort verified; binding-only preflight passes; execution remains disabled."
    )


if __name__ == "__main__":
    validate()
