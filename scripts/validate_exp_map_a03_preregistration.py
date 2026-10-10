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


def require(condition: bool, message: str = "") -> None:
    if not condition:
        raise AssertionError(message)


def validate() -> None:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    protocol = PROTOCOL.read_text(encoding="utf-8")

    require(spec["experiment_id"] == config["experiment_id"] == "EXP-MAP-A03")
    require(config["claim_ids"] == ["CLAIM-ACSC-002"])
    require(config["dataset_id"] == "DATA-ARITHMETIC")
    require(config["parameter_set_id"] == "PAR-MAP-003")
    require(config["null_id"] == "NULL-MAP-003")
    require(spec["config"] == config)

    snapshot = RegistrySnapshot.load(ROOT)
    resolved = snapshot.resolve("EXP-MAP-A03")
    require(resolved.experiment["Status"] == "preregistered")
    require(resolved.experiment["Claim_IDs"] == "CLAIM-ACSC-002")
    require(("CLAIM-ACSC-002", "EXP-MAP-A03") in resolved.claim_experiments)
    require(resolved.experiment["Namespace_Resolution"] == "scope_conflict_no_alias")
    require(resolved.experiment["Controlled_Execution_Eligible"] == "false")
    require(resolved.dataset["Controlled_Execution_Eligible"] == "false")
    require(resolved.experiment["Controlled_Support_Eligible"] == "false")
    require(resolved.experiment["Physical_Support_Eligible"] == "false")
    require(resolved.dataset["Controlled_Support_Eligible"] == "false")
    require(resolved.dataset["Physical_Support_Eligible"] == "false")
    require(resolved.provenance["Provenance_Status"] == "verified")
    require(resolved.provenance["Evidence_Status"] == "controlled")
    require(SOURCE_SHA256 in resolved.provenance["Integrity_Check"])
    require(resolved.parameter["Preregistration_Status"] == "locked")
    require(resolved.null["Preregistration_Status"] == "locked")
    require(spec["registry_bindings"] == resolved.record_hashes)

    require(config["input"]["source_rows"] == LOCKED_SOURCE_ROWS == 64687)
    require(config["input"]["representative_rows"] == LOCKED_REPRESENTATIVES == 38042)
    require(config["input"]["j_zero_exclusions"] == LOCKED_J_ZERO_EXCLUSIONS == 106)
    require(config["input"]["analysis_rows"] == LOCKED_ANALYSIS_ROWS == 37936)
    require(config["endpoint"]["k"] == 10)
    require(config["null"]["realizations"] == 999)
    require(config["null"]["seed"] == 4103)
    require(config["null"]["algorithm"] == "splitmix64-fisher-yates-v1")
    require(config["inference"]["alpha"] == 0.005)
    require(config["inference"]["sidedness"] == "one_sided_greater")
    require(config["inference"]["primary_endpoint_count"] == 1)
    require(config["outputs"] == spec["output_paths"])
    require(
        config["controls"]
        == {
            "controlled_execution_eligible": False,
            "controlled_support_eligible": False,
            "physical_support_eligible": False,
            "no_run_without_separate_activation": True,
        }
    )

    require(manifest["artifact"]["sha256"] == SOURCE_SHA256)
    require(manifest["artifact"]["expected_rows"] == 64687)
    require(manifest["cohort"]["representative_rows"] == 38042)
    require(manifest["cohort"]["expected_j_zero_exclusions"] == 106)
    require(manifest["cohort"]["expected_analysis_rows"] == 37936)
    require(manifest["cohort"]["post_hoc_filtering"] is False)
    require("no post-hoc filtering" in protocol.lower())
    require("Controlled_Execution_Eligible=false" in protocol)

    require(SOURCE.is_file(), "pinned ecdata submodule is not hydrated")
    require(file_sha256(SOURCE) == SOURCE_SHA256)
    require(SOURCE.stat().st_size == 2146401)
    frame, exclusions = load_locked_arithmetic(SOURCE, config)
    require(len(frame) == 37936)
    require(len(exclusions) == 106)
    require(
        list(exclusions.columns) == ["label", "isogeny_class", "conductor", "reason"]
    )
    require(set(exclusions["reason"]) == {"j_exactly_zero"})

    prepared = preflight_controlled_experiment(
        ROOT,
        SPEC,
        require_execution_eligibility=False,
    )
    require(prepared.resolved.record_hashes == spec["registry_bindings"])
    require(prepared.resolved.experiment["Controlled_Execution_Eligible"] == "false")
    require(prepared.resolved.dataset["Controlled_Execution_Eligible"] == "false")

    try:
        preflight_controlled_experiment(ROOT, SPEC)
    except PreflightError as exc:
        require("not controlled-execution eligible" in str(exc))
    else:
        raise AssertionError("normal execution preflight must remain closed for A03")

    print(
        "PASS: EXP-MAP-A03 preregistration bindings and deterministic 37,936-row "
        "cohort verified; binding-only preflight passes; execution remains disabled."
    )


if __name__ == "__main__":
    validate()
