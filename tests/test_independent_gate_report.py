"""Read-only snapshot and guard regression tests; no status promotion."""
import csv
import json
import shutil
from pathlib import Path

import pytest

from scripts.independent_gate_report import inspect, main

ROOT=Path(__file__).resolve().parents[1]


def test_source_registry_census_and_no_automatic_support():
    """Check registry integrity and consistency of execution and support flags."""
    r=inspect(ROOT)
    assert r["experiment_count"] >= 18
    assert r["registry_integrity_violations"] == []
    assert r["no_scientific_experiment_was_run"] is True
    assert r["planned"]+r["preregistered"] <= r["experiment_count"]
    assert all(not(x["status"]=="planned" and x["execution_eligible"])
               for x in r["entries"])
    assert all(not x["physical_support"] or x["controlled_support"]
               for x in r["entries"])


def test_dated_snapshot_contains_all_actual_source_ids_without_support_promotions():
    """Check the dated 18-experiment snapshot preserves its nonpromotion markers."""
    base=json.loads((ROOT/"research/independent_review/2026-10-09/experiment_gate_matrix.json").read_text())
    assert base["experiment_count"]==18
    assert len(base["experiments"])==18
    assert base["not_a_registry_transition"] is True
    assert base["status_counts"]=={"planned":17,"preregistered":1}
    assert all(x["action"]=="NO_AUTOMATIC_STATUS_MUTATION"
               and x["physical_support_at_baseline"] is False for x in base["experiments"])


def test_no_p0_candidate_terminals_fabricated():
    """Check all five candidates have recognized audit or terminal states."""
    from scripts.theory_search_states import is_terminal
    import csv
    with (ROOT/"registry/theory_candidate_registry_v0.1.csv").open(newline="",encoding="utf-8") as f:
        candidates=list(csv.DictReader(f))
    assert len(candidates)==5
    assert all(x["Audit_Status"] in {"REGISTERED_UNTESTED","PASSES_P0"} or is_terminal(x["Audit_Status"])
               for x in candidates)


def test_preregistration_sources_are_syntactically_locked_but_not_activated():
    """Definition locks never substitute for an accountable activation."""
    report=inspect(ROOT)
    a01=next(e for e in report["entries"] if e["experiment_id"]=="EXP-MAP-A01")
    assert a01["status"] in {"preregistered","executed","completed"}
    assert "parameter_not_preregistered" not in a01["blocking_gates"]
    assert "null_not_preregistered" not in a01["blocking_gates"]
    assert "dataset_source_provenance_not_verified" not in a01["blocking_gates"]
    # The report refuses to call a locked input physically supported on its own.
    assert report["no_scientific_experiment_was_run"] is True


ELIGIBILITY_FIELDS = (
    ("Controlled_Execution_Eligible", "execution_eligible"),
    ("Controlled_Support_Eligible", "controlled_support"),
    ("Physical_Support_Eligible", "physical_support"),
)


@pytest.fixture
def registry_with_flags(tmp_path):
    registry = tmp_path / "registry"
    registry.mkdir()
    for filename in (
        "dataset_registry_v0.1.csv",
        "parameter_registry_v0.1.csv",
        "null_registry_v0.1.csv",
    ):
        shutil.copyfile(ROOT / "registry" / filename, registry / filename)
    filename = "experiment_registry_v0.2.csv"
    with (ROOT / "registry" / filename).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        row = next(reader)
    row["Status"] = "preregistered"

    def write(values, omit=None):
        candidate = row.copy()
        candidate.update({field: "false" for field, _ in ELIGIBILITY_FIELDS})
        candidate.update(values)
        columns = [field for field in fields if field != omit]
        with (registry / filename).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
            writer.writeheader()
            writer.writerow(candidate)
        return tmp_path, row["Experiment_ID"]

    return write


@pytest.mark.parametrize("field, report_key", ELIGIBILITY_FIELDS)
@pytest.mark.parametrize("value", ["", " ", "yes", "1", "0", "tru", None])
def test_malformed_flags_report_integrity_error(
    registry_with_flags, capsys, field, report_key, value
):
    root, name = registry_with_flags({field: value})
    assert main(["--root", str(root)]) == 2
    report = json.loads(capsys.readouterr().out)
    assert len(report["registry_integrity_violations"]) == 1
    problem = report["registry_integrity_violations"][0]
    assert name in problem and field in problem
    assert "expected true or false" in problem
    assert report["entries"][0][report_key] is False


@pytest.mark.parametrize("field, report_key", ELIGIBILITY_FIELDS)
def test_missing_flag_reports_integrity_error(registry_with_flags, field, report_key):
    root, name = registry_with_flags({}, omit=field)
    report = inspect(root)
    assert report["registry_integrity_violations"] == [
        f"{name}: invalid {field} value None; expected true or false"
    ]
    assert report["entries"][0][report_key] is False


@pytest.mark.parametrize(
    "value, expected",
    [("true", True), ("false", False), (" TRUE ", True), (" FaLsE ", False)],
)
def test_valid_flags_preserve_boolean_interpretation(
    registry_with_flags, capsys, value, expected
):
    root, _ = registry_with_flags({field: value for field, _ in ELIGIBILITY_FIELDS})
    assert main(["--root", str(root)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["registry_integrity_violations"] == []
    for _, report_key in ELIGIBILITY_FIELDS:
        assert report["entries"][0][report_key] is expected
        assert report[report_key] == int(expected)
