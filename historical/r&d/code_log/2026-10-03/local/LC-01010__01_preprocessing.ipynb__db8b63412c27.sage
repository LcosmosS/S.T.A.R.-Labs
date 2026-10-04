# write alt_mappings.py and quantile.py into acsc/
from pathlib import Path

alt_code = r'''from typing import Sequence, Dict, Any
import numpy as np
import pandas as pd

def _safe_log10(arr, floor=1.0):
    a = np.asarray(arr, dtype=float)
    mask = ~np.isfinite(a) | (a == 0)
    out = np.empty_like(a)
    out[mask] = np.log10(float(floor))
    out[~mask] = np.log10(np.abs(a[~mask]))
    return out

def _scale(arr, lo, hi):
    a = np.asarray(arr, dtype=float)
    if a.size == 0:
        return a
    mn = np.nanmin(a); mx = np.nanmax(a)
    if not np.isfinite(mn) or not np.isfinite(mx) or mn == mx:
        return np.full_like(a, 0.5*(lo+hi))
    s = (a - mn) / (mx - mn)
    return lo + s*(hi-lo)

def _saturate(arr, v0=1.0):
    r = np.nan_to_num(np.asarray(arr, dtype=float), nan=0.0)
    mapped = np.arctan(r/float(v0)) / (0.5*np.pi)
    return np.clip(mapped, 0.0, 1.0)

def _j_to_complex(jvals):
    # Map complex or real j-invariant to two real axes: log|Re(j)| and log|Im(j)| (Im may be 0)
    j = np.asarray(jvals, dtype=complex)
    re = np.real(j)
    im = np.imag(j)
    # floor small values to avoid -inf
    re_log = _safe_log10(np.where(np.isfinite(re) & (np.abs(re)>0), re, 1.0))
    im_log = _safe_log10(np.where(np.isfinite(im) & (np.abs(im)>0), im, 1.0))
    return re_log, im_log

def _records_to_df(records):
    df = pd.DataFrame.from_records(records)
    # ensure columns exist
    for c in ["delta","conductor","rank","regulator","real_period","torsion_order","j_invariant"]:
        if c not in df.columns:
            df[c] = pd.NA
    # coerce numeric where appropriate
    df["delta"] = pd.to_numeric(df["delta"], errors="coerce")
    df["conductor"] = pd.to_numeric(df["conductor"], errors="coerce")
    df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
    df["regulator"] = pd.to_numeric(df["regulator"], errors="coerce")
    df["real_period"] = pd.to_numeric(df["real_period"], errors="coerce")
    df["torsion_order"] = pd.to_numeric(df["torsion_order"], errors="coerce")
    return df

def map_ptd(records: Sequence[Dict[str,Any]], Amax: float=1.0, Nmax: float=1.0, V0: float=1.0):
    """
    PTD mapping:
      X = scaled log10(|delta|)
      Y = scaled log10(real_period)  (if missing, fallback to log10(1+regulator))
      Z = log(1 + torsion_order) mapped via saturating transform
    """
    df = _records_to_df(records)
    n = len(df)
    if n == 0:
        return np.zeros((0,3), dtype=float)

    # X: discriminant
    x_log = _safe_log10(df["delta"].to_numpy(), floor=1.0)
    x = _scale(x_log, 0.0, float(Amax))

    # Y: prefer real_period; fallback to regulator
    rp = df["real_period"].to_numpy()
    rp_fallback = df["regulator"].to_numpy()
    # choose rp where finite else fallback
    y_source = np.where(np.isfinite(rp), rp, np.where(np.isfinite(rp_fallback), rp_fallback, 1.0))
    y_log = _safe_log10(y_source, floor=1.0)
    y = _scale(y_log, 0.0, float(Nmax))

    # Z: torsion -> log(1+T) then saturate
    T = df["torsion_order"].to_numpy()
    T_safe = np.where(np.isfinite(T), T, 0.0)
    z_raw = np.log1p(np.abs(T_safe))
    z = _saturate(z_raw, v0=float(V0)) * float(V0)

    coords = np.vstack([x,y,z]).T
    return coords

def map_mcj(records: Sequence[Dict[str,Any]], Amax: float=1.0, Nmax: float=1.0, V0: float=1.0):
    """
    MCJ mapping:
      X = scaled log10(conductor)
      Y = scaled log|Re(j)| (from j-invariant)
      Z = scaled log|Im(j)|  (captures modular position)
    If j_invariant missing, fallback to small constant.
    """
    df = _records_to_df(records)
    n = len(df)
    if n == 0:
        return np.zeros((0,3), dtype=float)

    # X: conductor
    cond = df["conductor"].to_numpy()
    cond_safe = np.where(np.isfinite(cond) & (cond>0), cond, 1.0)
    x_log = _safe_log10(cond_safe, floor=1.0)
    x = _scale(x_log, 0.0, float(Amax))

    # j-invariant handling
    jcol = df["j_invariant"].to_numpy()
    # try to parse numeric or complex strings; if not, treat as NaN
    # assume jcol may already be numeric or complex
    try:
        j_complex = np.array([complex(v) if (v is not None and not (pd.isna(v))) else complex(1.0) for v in jcol])
    except Exception:
        # fallback: treat all as 1.0
        j_complex = np.full(n, complex(1.0))

    re_log, im_log = _j_to_complex(j_complex)
    y = _scale(re_log, 0.0, float(Nmax))
    z = _scale(im_log, 0.0, float(V0))

    coords = np.vstack([x,y,z]).T
    return coords'''
quant_code = r'''import numpy as np
import json
from pathlib import Path

class QuantileAligner:
    def __init__(self):
        self._fitted = False
        self._quantiles = None
        self._axis_maps = None

    def fit(self, ref_coords: np.ndarray, n_quantiles: int = 200):
        ref_coords = np.asarray(ref_coords, dtype=float)
        if ref_coords.ndim != 2 or ref_coords.shape[1] != 3:
            raise ValueError("ref_coords must be (n,3)")
        q = np.linspace(0.0, 1.0, n_quantiles)
        self._quantiles = q.tolist()
        self._axis_maps = []
        for axis in range(3):
            vals = ref_coords[:, axis]
            vals_sorted = np.sort(vals[~np.isnan(vals)])
            if vals_sorted.size == 0:
                self._axis_maps.append([0.0]*n_quantiles)
            else:
                # compute empirical quantiles via interpolation
                qs = np.quantile(vals_sorted, q)
                self._axis_maps.append(qs.tolist())
        self._fitted = True
        return self

    def transform(self, src_coords: np.ndarray):
        if not self._fitted:
            raise RuntimeError("QuantileAligner not fitted")
        src = np.asarray(src_coords, dtype=float)
        if src.ndim != 2 or src.shape[1] != 3:
            raise ValueError("src_coords must be (m,3)")
        out = np.empty_like(src)
        q = np.array(self._quantiles)
        for axis in range(3):
            axis_map = np.array(self._axis_maps[axis])
            # map each src value to its empirical quantile in axis_map, then map to axis_map value
            # we compute the quantile of src value relative to axis_map via linear interpolation
            # first compute CDF-like mapping by inverting axis_map
            # handle constant axis_map
            if np.allclose(axis_map, axis_map[0]):
                out[:, axis] = axis_map[0]
                continue
            # for each value, find its fractional position in axis_map
            # use np.interp: given x=src_val, xp=axis_map, fp=q
            src_vals = src[:, axis]
            # clamp src_vals to axis_map range
            minv, maxv = axis_map[0], axis_map[-1]
            src_clamped = np.clip(src_vals, minv, maxv)
            frac = np.interp(src_clamped, axis_map, q)
            # now map frac back to axis_map (identity here) — effectively we are projecting onto ref quantiles
            out[:, axis] = np.interp(frac, q, axis_map)
        return out

    def save(self, path):
        d = {"quantiles": self._quantiles, "axis_maps": self._axis_maps}
        Path(path).write_text(json.dumps(d))

    def load(self, path):
        d = json.loads(Path(path).read_text())
        self._quantiles = d["quantiles"]
        self._axis_maps = d["axis_maps"]
        self._fitted = True
        return self'''

Path("acsc/alt_mappings.py").write_text(alt_code)
Path("acsc/quantile.py").write_text(quant_code)
print("Wrote acsc/alt_mappings.py and acsc/quantile.py")
