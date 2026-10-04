"""Planck chain loader and compatibility guard.

The tracked base_plikHM_TTTEEE_lowl_lowE_*.txt files are GetDist/CosmoMC
sample-chain tables, not three-column redshift/distance-modulus observations.
This module therefore exposes an explicit chain loader and refuses the legacy
"compressed z, mu, sigma_mu" interpretation.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd


PLANCK_CHAIN_ENV = "STAR_PLANCK_CHAIN_PATH"
DEFAULT_PLANCK_CHAIN_RELATIVE = Path(
    "data/planck/base_plikHM_TTTEEE_lowl_lowE_1.txt"
)
EXPECTED_CHAIN_COLUMNS = 95


def _resolve_chain_path(source_path=None):
    """Resolve an explicit chain path or the tracked checkout copy.

    Installed wheels intentionally do not bundle the multi-megabyte chain.
    When running from a source checkout, the tracked data/planck path is used
    if present. Outside a checkout, configure STAR_PLANCK_CHAIN_PATH or pass
    source_path explicitly.
    """
    candidate = source_path or os.environ.get(PLANCK_CHAIN_ENV)
    if candidate:
        path = Path(candidate).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Planck chain source is missing: {path}")
        return path

    checkout_candidate = (
        Path(__file__).resolve().parents[3] / DEFAULT_PLANCK_CHAIN_RELATIVE
    )
    if checkout_candidate.is_file():
        return checkout_candidate

    raise FileNotFoundError(
        "Planck chain source is not available. Pass source_path=..., set "
        f"{PLANCK_CHAIN_ENV}, or run from a checkout containing "
        f"{DEFAULT_PLANCK_CHAIN_RELATIVE}."
    )


def _chain_columns(n_columns):
    if n_columns < 3:
        raise ValueError(
            "Planck chain must contain weight, -log(posterior), and at least "
            "one sampled/derived parameter"
        )
    return [
        "weight",
        "minus_log_posterior",
        *[f"param_{index:03d}" for index in range(1, n_columns - 1)],
    ]


def load_planck_chain(
    source_path=None,
    *,
    expected_columns: int | None = EXPECTED_CHAIN_COLUMNS,
):
    """Load a Planck GetDist/CosmoMC sample-chain table.

    The first two columns are interpreted according to the GetDist chain
    convention as sample weight and -log(posterior). Remaining columns stay
    positional because this repository does not currently contain the matching
    .paramnames metadata needed to assign scientific parameter names safely.
    """
    source = _resolve_chain_path(source_path)

    frame = pd.read_csv(
        source,
        sep=r"\s+",
        comment="#",
        header=None,
        engine="python",
    )
    if frame.empty:
        raise ValueError(f"Planck chain source is empty: {source}")

    if expected_columns is not None and frame.shape[1] != int(expected_columns):
        raise ValueError(
            f"Planck chain has {frame.shape[1]} columns; "
            f"expected {int(expected_columns)}"
        )

    for column in frame.columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    values = frame.to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError(f"Non-finite or non-numeric values found in {source}")

    frame.columns = _chain_columns(frame.shape[1])
    if (frame["weight"] <= 0).any():
        raise ValueError("Planck chain weights must be strictly positive")

    return frame.reset_index(drop=True)


def load_planck_compressed(*args, **kwargs):
    """Reject the legacy three-column interpretation.

    This repository's base_plikHM_TTTEEE_lowl_lowE files are sample chains,
    not z/mu/sigma_mu observations. Use load_planck_chain instead.
    """
    raise RuntimeError(
        "base_plikHM_TTTEEE_lowl_lowE_*.txt is a Planck sample chain, not a "
        "three-column compressed z/mu/sigma_mu dataset. Use load_planck_chain()."
    )


class _LazyPlanckChain:
    def __init__(self):
        self._frame = None

    def _load(self):
        if self._frame is None:
            self._frame = load_planck_chain()
        return self._frame

    def __getitem__(self, key):
        return self._load()[key]

    def __getattr__(self, name):
        return getattr(self._load(), name)

    def __len__(self):
        return len(self._load())


class _RejectedCompressedView:
    def _raise(self):
        load_planck_compressed()

    def __getitem__(self, key):
        self._raise()

    def __getattr__(self, name):
        self._raise()

    def __len__(self):
        self._raise()


PLANCK_CHAIN = _LazyPlanckChain()
PLANCK_COMPRESSED = _RejectedCompressedView()
