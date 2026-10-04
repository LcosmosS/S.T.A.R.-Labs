"""
acsc.quantile
Coordinate-wise non-linear quantile alignment (fit on cosmic data, apply to arithmetic cloud).
Implements a smooth rank-based transformer using monotone spline interpolation.
"""

from typing import Tuple
import numpy as np
from scipy.interpolate import PchipInterpolator

class QuantileAligner:
    """
    Fit on a reference point cloud (cosmic) and apply to a target cloud (arithmetic).
    Works coordinate-wise.
    """
    def __init__(self):
        self._maps = []  # list of (xs, ys) interpolators per coordinate

    def fit(self, ref_coords: np.ndarray, n_quantiles: int = 200):
        ref_coords = np.asarray(ref_coords)
        assert ref_coords.ndim == 2
        d = ref_coords.shape[1]
        self._maps = []
        for j in range(d):
            vals = ref_coords[:, j]
            ranks = np.linspace(0.0, 1.0, n_quantiles)
            qs = np.quantile(vals, ranks)
            # monotone interpolator from [0,1] -> value
            interp = PchipInterpolator(ranks, qs, extrapolate=True)
            self._maps.append(interp)

    def transform(self, src_coords: np.ndarray) -> np.ndarray:
        src_coords = np.asarray(src_coords)
        assert src_coords.ndim == 2
        d = src_coords.shape[1]
        out = np.zeros_like(src_coords, dtype=float)
        for j in range(d):
            interp = self._maps[j]
            # compute empirical CDF value for each src coordinate via rank
            vals = src_coords[:, j]
            # rank-based CDF (simple empirical)
            ranks = np.argsort(np.argsort(vals)).astype(float) / max(1, len(vals) - 1)
            out[:, j] = interp(ranks)
        return out

    def fit_transform(self, ref_coords: np.ndarray, src_coords: np.ndarray, n_quantiles: int = 200) -> np.ndarray:
        self.fit(ref_coords, n_quantiles=n_quantiles)
        return self.transform(src_coords)

