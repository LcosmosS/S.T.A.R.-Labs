from typing import Sequence, List, Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd

def _safe_log10(x: np.ndarray, floor: float = 1.0) -> np.ndarray:
    """Compute log10 of absolute values with a floor to avoid -inf."""
    x = np.asarray(x, dtype=float)
    # replace non-finite and zeros with floor
    mask = ~np.isfinite(x) | (x == 0)
    out = np.empty_like(x)
    out[mask] = np.log10(float(floor))
    out[~mask] = np.log10(np.abs(x[~mask]))
    return out

def _scale_to_range(arr: np.ndarray, out_min: float, out_max: float) -> np.ndarray:
    """Linearly scale arr to [out_min, out_max]. If constant, return midpoint."""
    arr = np.asarray(arr, dtype=float)
    if arr.size == 0:
        return arr
    mn = np.nanmin(arr)
    mx = np.nanmax(arr)
    if not np.isfinite(mn) or not np.isfinite(mx) or mn == mx:
        return np.full_like(arr, 0.5 * (out_min + out_max))
    scaled = (arr - mn) / (mx - mn)
    return out_min + scaled * (out_max - out_min)

def _saturating_rank_map(ranks: np.ndarray, v0: float = 1.0) -> np.ndarray:
    """Map integer ranks to a bounded real axis using arctan-like saturation.
    v0 controls the scale where saturation begins.
    """
    r = np.asarray(ranks, dtype=float)
    # replace NaN with 0
    r = np.nan_to_num(r, nan=0.0)
    # use arctan to bound values between -pi/2 and pi/2, then rescale to [0,1]
    mapped = np.arctan(r / float(v0)) / (0.5 * np.pi)
    # mapped in [0,1); ensure finite
    mapped = np.clip(mapped, 0.0, 1.0)
    return mapped

def project(records: Sequence[Dict[str, Any]],
            method: str = "primary",
            Amax: float = 1.0,
            Nmax: float = 1.0,
            V0: float = 1.0) -> np.ndarray:
    """
    Convert a sequence of record dicts into Nx3 coordinates.

    Parameters
    - records: sequence of dict-like objects with keys 'delta', 'conductor', 'rank'
    - method: 'primary'|'ptd'|'mcj' (kept for API compatibility; same mapping here)
    - Amax, Nmax, V0: scaling parameters used in mapping

    Returns
    - coords: numpy array shape (n,3)
    """
    if records is None:
        return np.zeros((0, 3), dtype=float)

    # Convert to DataFrame for robust column handling
    df = pd.DataFrame.from_records(records)
    n = len(df)
    if n == 0:
        return np.zeros((0, 3), dtype=float)

    # Ensure columns exist
    for col in ["delta", "conductor", "rank"]:
        if col not in df.columns:
            df[col] = np.nan

    # Coerce numeric
    df["delta"] = pd.to_numeric(df["delta"], errors="coerce")
    df["conductor"] = pd.to_numeric(df["conductor"], errors="coerce")
    df["rank"] = pd.to_numeric(df["rank"], errors="coerce")

    # X: log10|delta| scaled to [0, Amax]
    logd = _safe_log10(df["delta"].to_numpy(), floor=1.0)
    x = _scale_to_range(logd, 0.0, float(Amax))

    # Y: log10(conductor) scaled to [0, Nmax]; treat conductor<=1 as floor
    cond = df["conductor"].to_numpy()
    cond_safe = np.where(np.isfinite(cond) & (cond > 0), cond, 1.0)
    logn = _safe_log10(cond_safe, floor=1.0)
    y = _scale_to_range(logn, 0.0, float(Nmax))

    # Z: rank mapped via saturating transform and scaled to [0,1] then to [0,1]*V0
    rank_map = _saturating_rank_map(df["rank"].to_numpy(), v0=float(V0))
    z = rank_map * float(V0)

    coords = np.vstack([x, y, z]).T
    # If method variants are needed, you can branch here; for now return same coords
    return coords