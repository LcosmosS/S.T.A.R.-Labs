"""Regression tests for the closed P0 theory-search preregistration."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry"

EXPECTED_CANDIDATES = {
    "P0-T001",
    "P0-T002",
    "P0-T003",
    "P0-T004",
    "P0-T005",
}


def _rows(name: str) -> list[dict[str, str]]:
    with (REGISTRY / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def test_p0_search_frame_is_closed_and_nonexecuting():
    rows = _rows("theory_search_registry_v0.1.csv")
    assert len(rows) == 1
    search = rows[0]

    assert search["Search_ID"] == "P0-SF-v0.1"
    assert search["Claim_ID"] == "CLAIM-ACSC-MECH-001"
    assert search["Registry_Namespace"] == "THEORY-SEARCH-v0.1"
    assert search["Qualified_Search_ID"] == "THEORY-SEARCH-v0.1:P0-SF-v0.1"
    assert search["Status"] == "preregistered_closed"
    assert search["Candidate_Count"] == "5"
    assert set(search["Candidate_IDs"].split(";")) == EXPECTED_CANDIDATES
    assert search["Admission_Criteria_Frozen"] == "true"
    assert search["Observable_Embargo"] == "true"
    assert search["List_Immutable_After_Start"] == "true"
    assert search["Exhaustion_Rule"] == "N_unresolved=0"
    assert search["Universal_NoGo_Claim"] == "false"
    assert search["Controlled_Execution_Eligible"] == "false"
    assert search["Controlled_Support_Eligible"] == "false"
    assert search["Physical_Support_Eligible"] == "false"
    assert (ROOT / search["Protocol_Path"]).is_file()


def test_exactly_five_parent_theory_candidates_are_frozen():
    rows = _rows("theory_candidate_registry_v0.1.csv")
    assert len(rows) == 5
    assert {row["Candidate_ID"] for row in rows} == EXPECTED_CANDIDATES

    for row in rows:
        assert row["Search_ID"] == "P0-SF-v0.1"
        assert row["Registry_Namespace"] == "THEORY-SEARCH-v0.1"
        assert row["Qualified_Candidate_ID"] == (
            f"THEORY-SEARCH-v0.1:{row['Candidate_ID']}"
        )
        assert row["Admission_Status"] == "admitted"
        assert row["Audit_Status"] == "REGISTERED_UNTESTED"
        assert row["Failure_Gate"] == ""
        assert row["Failure_Mechanism"] == ""
        assert row["Audit_Record_Path"] == ""
        assert row["Terminal"] == "false"
        assert row["Representative_Source_DOI"]
        assert row["Independent_Motivation"]
        assert row["Ellipticity_Selection_Prohibited"] == "true"
        assert row["Observable_Selection_Prohibited"] == "true"
        assert row["Within_Class_Model_Shopping_Prohibited"] == "true"
        assert row["Controlled_Execution_Eligible"] == "false"
        assert row["Controlled_Support_Eligible"] == "false"
        assert row["Physical_Support_Eligible"] == "false"


def test_szekeres_obstruction_is_class_relative_and_nonexecuting():
    rows = _rows("theory_obstruction_registry_v0.1.csv")
    assert len(rows) == 1
    row = rows[0]

    assert row["Obstruction_ID"] == "M1-INH-E1"
    assert row["Claim_ID"] == "CLAIM-ACSC-MECH-002"
    assert row["Registry_Namespace"] == "THEORY-SEARCH-v0.1"
    assert row["Qualified_Obstruction_ID"] == "THEORY-SEARCH-v0.1:M1-INH-E1"
    assert row["Status"] == "planned"
    assert row["Substage_A"] == "planned"
    assert row["Substage_B"] == "planned"
    assert row["Substage_C"] == "planned"
    assert row["Universal_NoGo_Claim"] == "false"
    assert row["Controlled_Execution_Eligible"] == "false"
    assert row["Controlled_Support_Eligible"] == "false"
    assert row["Physical_Support_Eligible"] == "false"
    assert (ROOT / row["Protocol_Path"]).is_file()


def test_theory_claims_are_registered_without_physical_support():
    claims = {row["Claim_ID"]: row for row in _rows("claim_evidence_v0.2.csv")}

    for claim_id in ("CLAIM-ACSC-MECH-001", "CLAIM-ACSC-MECH-002"):
        assert claim_id in claims
        claim = claims[claim_id]
        assert claim["Controlled_Support_Eligible"] == "false"
        assert claim["Physical_Support_Eligible"] == "false"
