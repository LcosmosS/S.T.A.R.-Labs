"""Off-path arithmetic/graph/null verification; synthetic inputs only."""
import importlib.util
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[1] / "research/independent_review/2026-10-16/verify_a03.py"
spec = importlib.util.spec_from_file_location("a03_reference_verification", PATH)
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)


def test_symbolic_discriminant_identity():
    reference.symbolic_identity()


def test_reference_algorithms_agree_on_synthetic_inputs():
    result = reference.fixture_checks()
    assert len(result["fixtures"]) == 3
    assert result["rejection_boundary_checked"] is True


def test_reference_detects_bad_graph(monkeypatch):
    monkeypatch.setattr(reference.production, "mcj_neighbor_edges", lambda frame: reference.np.zeros((1, 2), dtype=int))
    with pytest.raises(ValueError, match="brute-force graph mismatch"):
        reference.fixture_checks()


def test_reference_detects_bad_null_stream(monkeypatch):
    monkeypatch.setattr(reference.production, "_null_statistics_core", lambda *args, **kwargs: reference.np.zeros(3))
    with pytest.raises(ValueError, match="three-draw null disagrees"):
        reference.fixture_checks()


def test_brute_force_reference_refuses_actual_cohort_sized_input():
    with pytest.raises(ValueError, match="restricted to synthetic fixtures"):
        reference.reference_edges([None] * 65)


def test_singular_arithmetic_fails_reference():
    with pytest.raises(ValueError, match="singular reference curve"):
        reference.reference_invariants([0, 0, 0, 0, 0])
