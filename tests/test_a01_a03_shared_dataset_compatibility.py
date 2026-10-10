"""Synthetic registry-state tests; never run either registered endpoint."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from src.control.registry import RegistrySnapshot, record_sha256, execution_gate_failures
from src.control.shared_dataset_compatibility import (
    A01_ACTIVE_EXPERIMENT_SHA256,
    DATASET_A01_ACTIVE_SHA256,
    DATASET_INACTIVE_SHA256,
    a03_bindings_compatible,
    a03_shared_dataset_transition_is_compatible,
)

ROOT = Path(__file__).resolve().parents[1]
A03_SPEC = json.loads((ROOT / "controlled_execution/specs/EXP-MAP-A03.json").read_text())


def state(*, a01_active=False, dataset_active=False):
    """Return an isolated, shallow-copied registry snapshot for mutation tests."""
    snapshot = RegistrySnapshot.load(ROOT)
    snapshot = copy.deepcopy(snapshot)
    snapshot.experiments["EXP-MAP-A01"]["Controlled_Execution_Eligible"] = (
        "true" if a01_active else "false"
    )
    snapshot.datasets["DATA-ARITHMETIC"]["Controlled_Execution_Eligible"] = (
        "true" if dataset_active else "false"
    )
    return snapshot, snapshot.resolve("EXP-MAP-A03")


def test_original_frozen_a03_state_needs_no_compatibility_override():
    """The pre-activation exact binding remains the standard case."""
    snapshot, resolved = state()
    assert resolved.record_hashes["dataset"] == DATASET_INACTIVE_SHA256
    assert a03_bindings_compatible(A03_SPEC, resolved, snapshot)
    assert not a03_shared_dataset_transition_is_compatible(A03_SPEC, resolved, snapshot)


def test_hash_locked_a01_only_activation_preserves_a03_binding():
    """A01's exact two-flag transition must not authorize A03 execution."""
    snapshot, resolved = state(a01_active=True, dataset_active=True)
    assert record_sha256(snapshot.experiments["EXP-MAP-A01"]) == A01_ACTIVE_EXPERIMENT_SHA256
    assert resolved.record_hashes["dataset"] == DATASET_A01_ACTIVE_SHA256
    assert a03_shared_dataset_transition_is_compatible(A03_SPEC, resolved, snapshot)
    assert a03_bindings_compatible(A03_SPEC, resolved, snapshot)
    assert not execution_gate_failures(
        resolved, require_execution_eligibility=False
    )
    failures = execution_gate_failures(resolved)
    assert any("experiment is not controlled-execution eligible" in x for x in failures)


@pytest.mark.parametrize("a01_active,dataset_active", [(True, False), (False, True)])
def test_partial_activation_never_grants_dataset_binding_exception(a01_active, dataset_active):
    """Reject partial toggles and protect frozen historical A03 binding."""
    snapshot, resolved = state(a01_active=a01_active, dataset_active=dataset_active)
    assert not a03_shared_dataset_transition_is_compatible(A03_SPEC, resolved, snapshot)


@pytest.mark.parametrize("field,value", [
    ("Status", "executed"),
    ("Controlled_Support_Eligible", "true"),
    ("Current_Audit_Assessment", "unauthorized change"),
])
def test_a01_unreviewed_status_or_metadata_change_is_not_compatible(field, value):
    """The active A01 row must match its exact pre-reviewed SHA-256."""
    snapshot, resolved = state(a01_active=True, dataset_active=True)
    snapshot.experiments["EXP-MAP-A01"][field] = value
    assert not a03_bindings_compatible(A03_SPEC, resolved, snapshot)


@pytest.mark.parametrize("field,value", [
    ("Provenance_Status", "unknown"),
    ("Current_Audit_Assessment", "unauthorized change"),
    ("Controlled_Support_Eligible", "true"),
])
def test_dataset_drift_beyond_exact_execution_bit_fails_closed(field, value):
    """Reject any extra change to the shared dataset's canonical record."""
    snapshot, resolved = state(a01_active=True, dataset_active=True)
    snapshot.datasets["DATA-ARITHMETIC"][field] = value
    assert not a03_bindings_compatible(A03_SPEC, resolved, snapshot)


def test_a03_execution_or_frozen_binding_change_is_never_compatible():
    """Never elevate A03 or silently replace its immutable spec baseline."""
    snapshot, resolved = state(a01_active=True, dataset_active=True)
    snapshot.experiments["EXP-MAP-A03"]["Controlled_Execution_Eligible"] = "true"
    assert not a03_bindings_compatible(A03_SPEC, resolved, snapshot)
    snapshot, resolved = state(a01_active=True, dataset_active=True)
    forged = copy.deepcopy(A03_SPEC)
    forged["registry_bindings"]["dataset"] = DATASET_A01_ACTIVE_SHA256
    assert not a03_shared_dataset_transition_is_compatible(forged, resolved, snapshot)
