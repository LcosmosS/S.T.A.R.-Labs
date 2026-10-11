"""Locked EXP-MAP-A03 fixtures; no controlled dataset execution."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.experiments.exp_map_a03 import (
    ALPHA, B, K, LOCKED_ANALYSIS_ROWS, LOCKED_J_ZERO_EXCLUSIONS,
    LOCKED_REPRESENTATIVES, LOCKED_SOURCE_ROWS, SEED, MCJProtocolError,
    _require_locked_config, c4_from_ainvariants, decile_groups,
    fixture_null_statistics, full_null_statistics, mcj_neighbor_edges,
    project_arithmetic,
)
from src.experiments.exp_map_a01 import _discriminant

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "preregistrations" / "EXP-MAP-A03" / "config.json"


def _config():
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def test_committed_config_is_exactly_locked():
    _require_locked_config(_config())
    assert (
        LOCKED_SOURCE_ROWS, LOCKED_REPRESENTATIVES, LOCKED_J_ZERO_EXCLUSIONS,
        LOCKED_ANALYSIS_ROWS, B, SEED, ALPHA, K,
    ) == (64687, 38042, 106, 37936, 999, 4103, 0.005, 10)


def test_exact_arithmetic_and_principal_j_branch():
    positive = (0, 0, 1, -1, 0)
    negative = (0, 0, 0, -1, 1)
    assert _discriminant(positive) == 37
    assert c4_from_ainvariants(positive) == 48
    assert project_arithmetic(positive, 37)[2] == 0.0
    assert _discriminant(negative) < 0
    assert c4_from_ainvariants(negative) > 0
    assert project_arithmetic(negative, 37)[2] == math.pi
    assert math.isclose(project_arithmetic(positive, 37)[1], math.log(48**3 / 37))
    assert project_arithmetic((0, 0, 1, 0, 1), 37) is None


def test_singular_curve_aborts_before_j_zero_exclusion():
    with pytest.raises(MCJProtocolError, match="zero discriminant"):
        project_arithmetic((0, 0, 0, 0, 0), 11)
    with pytest.raises(MCJProtocolError, match="zero discriminant"):
        project_arithmetic((0, 0, 0, -3, 2), 11)


def test_invalid_conductor_aborts_even_with_j_zero():
    with pytest.raises(MCJProtocolError, match="conductor must be positive"):
        project_arithmetic((0, 0, 1, 0, 1), 0)


def _fixture(n=24):
    return pd.DataFrame({
        "label": [f"{101+i}a1" for i in range(n)],
        "conductor": [101+i for i in range(n)],
        "x": [float(i % 6) for i in range(n)],
        "y": [float(i // 6) for i in range(n)],
        "z": [float((i % 3) * math.pi) for i in range(n)],
        "rank": [i % 4 for i in range(n)],
    })


def test_graph_is_rank_blind_and_duplicate_ties_are_deterministic():
    frame = _fixture()
    original = mcj_neighbor_edges(frame)
    frame["rank"] = list(reversed(frame["rank"].tolist()))
    assert np.array_equal(mcj_neighbor_edges(frame), original)
    frame.loc[1, ["x","y","z"]] = frame.loc[0, ["x","y","z"]]
    assert len(mcj_neighbor_edges(frame)) > 0


def test_deciles_and_short_fixture_are_reproducible():
    frame = _fixture()
    groups = decile_groups(frame)
    assert len(groups) == 10
    assert sorted(np.concatenate(groups).tolist()) == list(range(len(frame)))
    observed, first = fixture_null_statistics(frame)
    observed2, second = fixture_null_statistics(frame)
    assert observed == observed2
    assert np.array_equal(first, second)
    assert len(first) == 3


def test_full_999_draw_null_exists_and_is_reproducible_on_synthetic_fixture():
    frame = _fixture()
    edges = mcj_neighbor_edges(frame)
    first = full_null_statistics(frame, edges, _config())
    second = full_null_statistics(frame, edges, _config())
    assert len(first) == 999
    assert np.array_equal(first, second)
    assert np.isfinite(first).all()


def test_scientific_mutations_are_rejected():
    cfg = _config()
    cfg["endpoint"]["k"] = 11
    with pytest.raises(MCJProtocolError, match="does not exactly match"):
        _require_locked_config(cfg)
    cfg = _config()
    cfg["null"]["seed"] = 4104
    with pytest.raises(MCJProtocolError, match="does not exactly match"):
        _require_locked_config(cfg)
    cfg = _config()
    cfg["input"]["analysis_rows"] = 37935
    with pytest.raises(MCJProtocolError, match="does not exactly match"):
        _require_locked_config(cfg)
    with pytest.raises(MCJProtocolError, match="k=10"):
        mcj_neighbor_edges(_fixture(), 11)
    with pytest.raises(MCJProtocolError, match="short fixed-seed fixture"):
        fixture_null_statistics(_fixture(), draws=999)
    with pytest.raises(MCJProtocolError, match="not in frozen"):
        decile_groups(_fixture().iloc[::-1].reset_index(drop=True))
