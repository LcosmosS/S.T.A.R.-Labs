"""Regression tests for explicit, fail-closed Planck source loading."""

import numpy as np
import pytest

from src.likelihoods.data.planck_compressed import (
    PLANCK_SOURCE_ENV,
    load_planck_compressed,
)


def test_planck_loader_requires_explicit_source(monkeypatch):
    monkeypatch.delenv(PLANCK_SOURCE_ENV, raising=False)
    with pytest.raises(FileNotFoundError, match="not configured"):
        load_planck_compressed()


def test_planck_loader_accepts_finite_positive_uncertainty(tmp_path):
    source = tmp_path / "planck.txt"
    source.write_text("0.1 38.0 0.2\n0.2 40.0 0.3\n", encoding="utf-8")

    frame = load_planck_compressed(source_path=source)

    assert list(frame.columns) == ["z", "mu", "sigma_mu"]
    assert frame.shape == (2, 3)
    assert np.isfinite(frame.to_numpy()).all()


@pytest.mark.parametrize(
    "row",
    [
        "inf 38.0 0.2\n",
        "0.1 -inf 0.2\n",
        "0.1 38.0 inf\n",
        "0.1 38.0 nan\n",
    ],
)
def test_planck_loader_rejects_nonfinite_values(tmp_path, row):
    source = tmp_path / "planck.txt"
    source.write_text(row, encoding="utf-8")

    with pytest.raises(ValueError, match="Non-finite"):
        load_planck_compressed(source_path=source)


def test_planck_loader_rejects_nonpositive_uncertainty(tmp_path):
    source = tmp_path / "planck.txt"
    source.write_text("0.1 38.0 0.0\n", encoding="utf-8")

    with pytest.raises(ValueError, match="positive"):
        load_planck_compressed(source_path=source)
