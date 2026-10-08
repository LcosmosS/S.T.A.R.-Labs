"""
acsc.projection
Primary and alternative projection maps from elliptic-curve invariants to R^3.

Expect input rows/dicts with keys:
  - delta (minimal discriminant, integer)
  - conductor (N, integer)
  - rank (r, integer)
  - regulator (R, float)
  - real_period (Q, float)
  - torsion_order (T, integer)

All functions return numpy arrays of shape (3,) for a single curve or (n,3) for arrays.
"""

from typing import Dict, Iterable, Tuple
import numpy as np

# --- Utilities --------------------------------------------------------------

def _safe_log10(x, eps=1e-12):
    x = np.asarray(x, dtype=float)
    return np.log10(np.maximum(np.abs(x), eps))

# --- Primary projection (rank-normalized spherical embedding) ---------------

def primary_projection(records: Iterable[Dict],
                       Amax: float = 1e12,
                       Nmax: float = 1e6,
                       V0: float = 1.0) -> np.ndarray:
    """
    Rank-normalized primary projection (¢_prim).
    records: iterable of dict-like objects with required keys (see module docstring).
    Returns: ndarray shape (n,3)
    """
    recs = list(records)
    n = len(recs)
    coords = np.zeros((n, 3), dtype=float)

    for i, r in enumerate(recs):
        delta = r.get("delta", 1)
        N = r.get("conductor", 1)
        rank = int(r.get("rank", 0))
        R = float(r.get("regulator", 1.0))
        Q = float(r.get("real_period", 1.0))
        T = int(r.get("torsion_order", 1))

        # radial coordinate V_E (rank-normalized)
        Wr = 2 * rank * (rank + 1)
        # avoid division by zero
        denom = max(1, rank)
        radial = V0 * (T * np.log(max(Q, 1e-12) / 2.0) * (R ** (1.0 / denom))) * np.exp(Wr)

        # angular coordinates (wrapped logs)
        theta = np.mod(_safe_log10(delta) / np.log10(max(Amax, 10.0)), 2 * np.pi)
        phi = np.mod(np.pi * _safe_log10(N) / np.log10(max(Nmax, 10.0)), np.pi)

        # spherical -> cartesian
        x = radial * np.sin(theta) * np.cos(phi)
        y = radial * np.sin(theta) * np.sin(phi)
        z = radial * np.cos(theta)

        coords[i, :] = (x, y, z)

    return coords

# --- Alternative projection PTD ---------------------------------------------

def projection_ptd(records: Iterable[Dict]) -> np.ndarray:
    """
    PTD alternative: (log|delta|, log(conductor), log(1+|torsion|))
    """
    recs = list(records)
    n = len(recs)
    coords = np.zeros((n, 3), dtype=float)
    for i, r in enumerate(recs):
        coords[i, 0] = _safe_log10(r.get("delta", 1))
        coords[i, 1] = np.log1p(max(int(r.get("conductor", 1)), 0))
        coords[i, 2] = np.log1p(abs(int(r.get("torsion_order", 0))))
    return coords

# --- Alternative projection MCJ ---------------------------------------------

def projection_mcj(records: Iterable[Dict]) -> np.ndarray:
    """
    MCJ alternative: (log(conductor), log(j-invariant proxy), log(1+regulator))
    Note: j-invariant is not always available; use a placeholder or precomputed j if present.
    """
    recs = list(records)
    n = len(recs)
    coords = np.zeros((n, 3), dtype=float)
    for i, r in enumerate(recs):
        N = max(int(r.get("conductor", 1)), 1)
        j = r.get("j_invariant", None)
        if j is None:
            # fallback proxy: ratio of discriminant to conductor (signed)
            j_proxy = float(r.get("delta", 1)) / float(N)
        else:
            j_proxy = float(j)
        coords[i, 0] = np.log1p(N)
        coords[i, 1] = _safe_log10(j_proxy)
        coords[i, 2] = np.log1p(float(r.get("regulator", 0.0)))
    return coords

# --- Batch dispatcher -------------------------------------------------------

def project(records: Iterable[Dict], method: str = "primary", **kwargs) -> np.ndarray:
    """
    Dispatch to a projection method. method in {"primary","ptd","mcj"}.
    """
    method = method.lower()
    if method == "primary":
        return primary_projection(records, **kwargs)
    elif method == "ptd":
        return projection_ptd(records)
    elif method == "mcj":
        return projection_mcj(records)
    else:
        raise ValueError(f"Unknown projection method: {method}")

