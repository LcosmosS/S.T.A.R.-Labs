"""Deterministic arithmetic-to-coordinate projection primitives."""

from typing import Sequence, Dict, Any
import numpy as np
import pandas as pd

def _safe_log10(x, floor=1.0):
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    mask = ~np.isfinite(x) | (x == 0)
    out[mask] = np.log10(float(floor))
    out[~mask] = np.log10(np.abs(x[~mask]))
    return out

def _scale_to_range(arr, out_min, out_max):
    arr = np.asarray(arr, dtype=float)
    if arr.size == 0:
        return arr
    mn, mx = np.nanmin(arr), np.nanmax(arr)
    if not np.isfinite(mn) or not np.isfinite(mx) or mn == mx:
        return np.full_like(arr, 0.5 * (out_min + out_max))
    return out_min + (arr - mn) / (mx - mn) * (out_max - out_min)

def _saturating_rank_map(ranks, v0=1.0):
    r = np.nan_to_num(np.asarray(ranks, dtype=float), nan=0.0)
    return np.clip(np.arctan(r / float(v0)) / (0.5 * np.pi), 0.0, 1.0)

def project(records: Sequence[Dict[str, Any]], method="primary",
            Amax=1.0, Nmax=1.0, V0=1.0):
    """Project arithmetic records deterministically into R^3.

    The method parameter is retained for compatibility. Distinct registered
    mapping definitions should be implemented as separate named mappings rather
    than silently sharing an implementation.
    """
    if records is None:
        return np.zeros((0, 3), dtype=float)
    df = pd.DataFrame.from_records(records)
    if df.empty:
        return np.zeros((0, 3), dtype=float)
    for col in ("delta", "conductor", "rank"):
        if col not in df:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")
    x = _scale_to_range(_safe_log10(df["delta"].to_numpy()), 0.0, float(Amax))
    cond = np.where(np.isfinite(df["conductor"]) & (df["conductor"] > 0), df["conductor"], 1.0)
    y = _scale_to_range(_safe_log10(cond), 0.0, float(Nmax))
    z = _saturating_rank_map(df["rank"].to_numpy(), float(V0)) * float(V0)
    return np.column_stack([x, y, z])

class ArithmeticProjector:
    def __init__(self, method="primary", Amax=1.0, Nmax=1.0, V0=1.0):
        self.method, self.Amax, self.Nmax, self.V0 = method, Amax, Nmax, V0
    def project(self, records):
        return project(records, self.method, self.Amax, self.Nmax, self.V0)
    def embed_to_cosmic(self, coords, seed=0, noise_scale=0.0, depth_scale=1.8):
        """Optional reproducible embedding; noise is explicit and disabled by default."""
        embedded = np.asarray(coords, dtype=float).copy()
        if noise_scale:
            rng = np.random.default_rng(seed)
            embedded += rng.normal(0.0, noise_scale, embedded.shape)
        if embedded.ndim == 2 and embedded.shape[1] >= 3:
            embedded[:, 2] *= float(depth_scale)
        return embedded
