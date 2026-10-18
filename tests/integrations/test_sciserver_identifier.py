
"""Regression tests for SciServer identifier fidelity."""

import pandas as pd
import pytest

from integrations.sciserver.server import exact_objid


EXPECTED = "1237645876861272071"


def test_exact_integer():
    value = 1237645876861272071

    assert exact_objid(value) == EXPECTED


def test_exact_string():
    assert exact_objid(EXPECTED) == EXPECTED


def test_dataframe_column_preserves_identifier():
    df = pd.DataFrame({
        "objid": pd.Series(
            [1237645876861272071],
            dtype="int64",
        ),
        "ra": [336.439637],
        "dec": [-0.837205],
        "g": [14.36237],
    })

    result = exact_objid(df["objid"].iat[0])

    assert result == EXPECTED


def test_floating_point_identifier_rejected():
    with pytest.raises(TypeError):
        exact_objid(1.237645876861272e18)


def test_scientific_notation_rejected():
    with pytest.raises(ValueError):
        exact_objid("1.237645876861272e+18")


def test_boolean_rejected():
    with pytest.raises(TypeError):
        exact_objid(True)


def test_negative_identifier_rejected():
    with pytest.raises(ValueError):
        exact_objid("-1237645876861272071")


def test_null_identifier_rejected():
    with pytest.raises(TypeError):
        exact_objid(None)
