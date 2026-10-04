"""Fail-closed loader for an explicitly configured Planck compressed source."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd


PLANCK_SOURCE_ENV = "STAR_PLANCK_COMPRESSED_PATH"


def _resolve_source_path(source_path=None):
    candidate = source_path or os.environ.get(PLANCK_SOURCE_ENV)
    if not candidate:
        raise FileNotFoundError(
            "Planck compressed source is not configured. Pass source_path=... "
            f"or set {PLANCK_SOURCE_ENV}. Repository placeholders and synthetic "
            "fallbacks are not accepted."
        )
    path = Path(candidate).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Planck compressed source is missing: {path}")
    return path


def load_planck_compressed(version: str = "main", source_path=None):
    """Load a provenance-resolved Planck compressed-likelihood table.

    The observational source is intentionally external to the wheel. Installed
    imports therefore do not depend on a repository-relative data directory.
    A caller must explicitly provide the source path or configure
    STAR_PLANCK_COMPRESSED_PATH before loading data.
    """
    if version != "main":
        raise ValueError(f"unsupported Planck compressed version: {version}")

    main_file = _resolve_source_path(source_path)
    df = pd.read_csv(
        main_file,
        sep=r"\s+",
        comment="#",
        header=None,
        engine="python",
    )
    if df.shape[1] < 3:
        raise ValueError(f"Unexpected format in {main_file}")

    df = df.iloc[:, :3].copy()
    df.columns = ["z", "mu", "sigma_mu"]
    for col in ("z", "mu", "sigma_mu"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df.empty:
        raise ValueError(f"Planck compressed source is empty: {main_file}")
    values = df[["z", "mu", "sigma_mu"]].to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError(f"Non-finite or non-numeric values found in {main_file}")
    if (df["sigma_mu"] <= 0).any():
        raise ValueError("Planck compressed uncertainties must be positive")
    return df.reset_index(drop=True)


class _LazyPlanckCompressed:
    """Backward-compatible lazy access to the explicitly configured source."""

    def __init__(self):
        self._frame = None

    def _load(self):
        if self._frame is None:
            self._frame = load_planck_compressed()
        return self._frame

    def __getitem__(self, key):
        return self._load()[key]

    def __getattr__(self, name):
        return getattr(self._load(), name)

    def __len__(self):
        return len(self._load())


PLANCK_COMPRESSED = _LazyPlanckCompressed()
