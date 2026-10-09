"""MCJ prospective mathematical fixtures; no controlled full-cohort computation."""
from __future__ import annotations
import math
import numpy as np
import pandas as pd
import pytest

from src.experiments.exp_map_a03 import (
    ALPHA, B, K, SEED, MCJProtocolError, c4_from_ainvariants,
    controlled_calculation_is_disabled, decile_groups, fixture_null_statistics,
    mcj_neighbor_edges, project_arithmetic
)
from src.experiments.exp_map_a01 import _discriminant


def test_exact_arithmetic_and_principal_j_branch():
    positive = (0,0,1,-1,0)
    negative = (0,0,0,-1,1)
    assert _discriminant(positive) == 37
    assert c4_from_ainvariants(positive) == 48
    assert project_arithmetic(positive,37)[2] == 0.0
    assert _discriminant(negative) < 0
    assert c4_from_ainvariants(negative) > 0
    assert project_arithmetic(negative,37)[2] == math.pi
    assert math.isclose(project_arithmetic(positive,37)[1], math.log(48**3 / 37))
    assert project_arithmetic((0,0,1,0,1),37) is None  # j exactly 0



def test_singular_curve_aborts_before_j_zero_exclusion():
    # Both c4 and Delta vanish: cannot exclude a singular curve as j=0.
    with pytest.raises(MCJProtocolError, match="zero discriminant"):
        project_arithmetic((0, 0, 0, 0, 0), 11)
    # c4 is nonzero, yet Delta=0: no raw log(0) ValueError allowed.
    with pytest.raises(MCJProtocolError, match="zero discriminant"):
        project_arithmetic((0, 0, 0, -3, 2), 11)


def test_invalid_conductor_aborts_even_with_j_exactly_zero():
    with pytest.raises(MCJProtocolError, match="conductor must be positive"):
        project_arithmetic((0, 0, 1, 0, 1), 0)

def test_large_integer_logs_avoid_j_float_overflow():
    point = project_arithmetic((1,0,0,-10**120,10**80), 997)
    assert point is None or all(math.isfinite(v) for v in point)


def _fixture(n=24):
    return pd.DataFrame({
        "label": [f"{101+i}a1" for i in range(n)],
        "conductor": [101+i for i in range(n)],
        "x": [float(i % 6) for i in range(n)],
        "y": [float(i // 6) for i in range(n)],
        "z": [float((i % 3) * math.pi) for i in range(n)],
        "rank": [i % 4 for i in range(n)],
    })


def test_graph_rank_blind_and_duplicate_point_ties():
    f = _fixture()
    original = mcj_neighbor_edges(f)
    f["rank"] = list(reversed(f["rank"].tolist()))
    assert np.array_equal(mcj_neighbor_edges(f), original)
    f.loc[1,["x","y","z"]] = f.loc[0,["x","y","z"]]
    assert len(mcj_neighbor_edges(f)) > 0


def test_deciles_condition_rank_and_reproducible_fixture_null():
    f = _fixture()
    groups = decile_groups(f)
    assert len(groups) == 10
    assert sorted(np.concatenate(groups).tolist()) == list(range(len(f)))
    observed, first = fixture_null_statistics(f)
    obs2, second = fixture_null_statistics(f)
    assert observed == obs2
    assert np.array_equal(first,second)
    assert len(first) == 3
    assert (B, SEED, ALPHA, K) == (999, 4103, .005, 10)


def test_fail_closed_execution_and_protocol_mutations():
    with pytest.raises(MCJProtocolError,match="remains planned"):
        controlled_calculation_is_disabled()
    with pytest.raises(MCJProtocolError,match="k=10"):
        mcj_neighbor_edges(_fixture(),11)
    with pytest.raises(MCJProtocolError,match="short fixed-seed fixture"):
        fixture_null_statistics(_fixture(),draws=999)
    bad=_fixture().iloc[::-1].reset_index(drop=True)
    with pytest.raises(MCJProtocolError,match="not in frozen"):
        decile_groups(bad)
