"""Read-only snapshot and guard regression tests; no status promotion."""
import json
from pathlib import Path
from scripts.independent_gate_report import inspect

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
