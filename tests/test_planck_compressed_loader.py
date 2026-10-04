"""Regression tests for Planck chain semantics."""

import numpy as np
import pytest

from src.likelihoods.data.planck_compressed import (
    EXPECTED_CHAIN_COLUMNS,
    PLANCK_CHAIN_ENV,
    load_planck_chain,
    load_planck_compressed,
)


def _write_chain(path, *, rows=2, columns=EXPECTED_CHAIN_COLUMNS):
    values = np.arange(1, rows * columns + 1, dtype=float).reshape(rows, columns)
    values[:, 0] = np.arange(1, rows + 1, dtype=float)
    values[:, 1] = 1395.0 + np.arange(rows, dtype=float)
    np.savetxt(path, values)
    return values


def test_planck_chain_loader_preserves_all_positional_columns(tmp_path):
    source = tmp_path / "chain.txt"
    original = _write_chain(source)

    frame = load_planck_chain(source_path=source)

    assert frame.shape == original.shape
    assert frame.columns[0] == "weight"
    assert frame.columns[1] == "minus_log_posterior"
    assert frame.columns[-1] == "param_093"
    assert np.isfinite(frame.to_numpy()).all()


def test_planck_chain_loader_can_use_declared_environment_path(tmp_path, monkeypatch):
    source = tmp_path / "chain.txt"
    _write_chain(source)
    monkeypatch.setenv(PLANCK_CHAIN_ENV, str(source))

    frame = load_planck_chain()

    assert len(frame) == 2


@pytest.mark.parametrize(
    ("column", "value"),
    [
        (0, np.inf),
        (1, -np.inf),
        (2, np.nan),
    ],
)
def test_planck_chain_loader_rejects_nonfinite_values(tmp_path, column, value):
    source = tmp_path / "chain.txt"
    values = _write_chain(source)
    values[0, column] = value
    np.savetxt(source, values)

    with pytest.raises(ValueError, match="Non-finite"):
        load_planck_chain(source_path=source)


def test_planck_chain_loader_rejects_nonpositive_weight(tmp_path):
    source = tmp_path / "chain.txt"
    values = _write_chain(source)
    values[0, 0] = 0.0
    np.savetxt(source, values)

    with pytest.raises(ValueError, match="weights"):
        load_planck_chain(source_path=source)


def test_planck_chain_loader_rejects_wrong_column_count(tmp_path):
    source = tmp_path / "chain.txt"
    _write_chain(source, columns=3)

    with pytest.raises(ValueError, match="expected 95"):
        load_planck_chain(source_path=source)


def test_legacy_compressed_interpretation_is_rejected():
    with pytest.raises(RuntimeError, match="sample chain"):
        load_planck_compressed()
