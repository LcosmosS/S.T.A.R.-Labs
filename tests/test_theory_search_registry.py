"""Regression tests for the closed P0 theory-search preregistration."""

from __future__ import annotations

import csv
import re
from pathlib import Path

from scripts.theory_search_states import (
    ALLOWED_CANDIDATE_STATUSES,
    TERMINAL_CANDIDATE_STATUSES,
    TERMINAL_FAILURE_STATUSES,
    TERMINAL_SUCCESS_STATUSES,
    UNRESOLVED_CANDIDATE_STATUSES,
    can_transition,
    is_terminal,
    is_unresolved,
)


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



def test_candidate_lifecycle_makes_passes_p0_unresolved():
    assert "REGISTERED_UNTESTED" in UNRESOLVED_CANDIDATE_STATUSES
    assert "PASSES_P0" in UNRESOLVED_CANDIDATE_STATUSES
    assert "PASSES_P0" not in TERMINAL_CANDIDATE_STATUSES
    assert not is_terminal("PASSES_P0")
    assert is_unresolved("PASSES_P0")

    assert TERMINAL_SUCCESS_STATUSES == {"PASSES_P1"}
    assert is_terminal("PASSES_P1")
    assert not is_unresolved("PASSES_P1")

    assert ALLOWED_CANDIDATE_STATUSES == (
        UNRESOLVED_CANDIDATE_STATUSES | TERMINAL_CANDIDATE_STATUSES
    )


def test_candidate_lifecycle_transitions_are_closed():
    assert can_transition("REGISTERED_UNTESTED", "PASSES_P0")
    assert can_transition("REGISTERED_UNTESTED", "NO_ENDOGENOUS_ELLIPTIC_SECTOR")
    assert not can_transition("REGISTERED_UNTESTED", "PASSES_P1")

    assert can_transition("PASSES_P0", "PASSES_P1")
    assert can_transition("PASSES_P0", "FAILS_P1")
    assert can_transition("PASSES_P0", "FAILS_STRUCTURE_SUFFICIENCY")
    assert not can_transition("PASSES_P0", "NO_ENDOGENOUS_ELLIPTIC_SECTOR")

    for status in TERMINAL_CANDIDATE_STATUSES:
        for target in ALLOWED_CANDIDATE_STATUSES - {status}:
            assert not can_transition(status, target)


def test_terminal_failure_states_require_failure_provenance_by_contract():
    assert "FAILS_P1" in TERMINAL_FAILURE_STATUSES
    assert "FAILS_STRUCTURE_SUFFICIENCY" in TERMINAL_FAILURE_STATUSES
    assert "PASSES_P1" not in TERMINAL_FAILURE_STATUSES


def test_preregistration_protocols_contain_no_ascii_control_characters():
    for relative in (
        "preregistrations/P0-ANSATZ-001/protocol.md",
        "preregistrations/M1-INH-E1/protocol.md",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        invalid = [
            ord(char)
            for char in text
            if ord(char) < 32 and char not in "\n\r\t"
        ]
        assert invalid == [], f"{relative} contains ASCII control characters: {invalid}"


def test_frozen_dynamics_keep_literal_tex_commands():
    text = (ROOT / "preregistrations/P0-ANSATZ-001/protocol.md").read_text(
        encoding="utf-8"
    )
    for token in (
        r"\rho",
        r"\nabla",
        r"\frac",
        r"\beta",
        r"\eta",
        r"\mu",
        r"\nu",
        r"\Lambda",
    ):
        assert token in text


def test_szekeres_elliptic_record_is_defined_before_e1a():
    text = (ROOT / "preregistrations/M1-INH-E1/protocol.md").read_text(
        encoding="utf-8"
    )
    record = text.index("## Registered elliptic-evolution data record")
    e1a = text.index("## M1-INH-E1a — exact reduction")
    e1b = text.index("## M1-INH-E1b — field-level insufficiency")

    assert record < e1a < e1b
    assert r"g_2(z)=\frac{K(z)^2}{12}" in text
    assert r"g_3(z)" in text
    assert r"\Delta_{\wp}(z)" in text
    assert r"\mathfrak E[S]" in text


def test_szekeres_kernel_test_is_explicitly_regular_and_nonexact():
    text = (ROOT / "preregistrations/M1-INH-E1/protocol.md").read_text(
        encoding="utf-8"
    )
    normalized = re.sub(r"\s+", " ", text)
    assert "locally constant rank" in normalized
    assert "tangent space" in normalized
    assert "differentiable local factorization" in normalized
    assert "does **not** by itself establish failure of exact sufficiency" in normalized
    assert "Exact observable insufficiency under E1c is established only" in normalized
