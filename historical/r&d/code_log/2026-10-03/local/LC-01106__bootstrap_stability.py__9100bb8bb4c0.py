"""
bootstrap_stability.py
----------------------
Implements bootstrap averaging for persistence landscapes and
topological stability analysis in the S.T.A.R. Model.

This module:
- resamples point clouds
- computes persistence landscapes
- averages landscapes
- estimates variance and stability metrics
"""

import numpy as np
from .persistence_landscape import PersistenceLandscape
from src.data.load_sky_surveys import load_sky_surveys

def test_sky_surveys_load():
    df1, df2 = load_sky_surveys(downsample=100, validate_schema=True)
    assert len(df1) > 0
    assert len(df2) > 0

class BootstrapStability:
    """
    Bootstrap ensemble for TDA stability.
    """

    def __init__(self, num_bootstrap=50, resolution=200):
        self.num_bootstrap = num_bootstrap
        self.landscape = PersistenceLandscape(resolution=resolution)

    def resample(self, X):
        """
        Bootstrap resample the point cloud.
        """
        idx = np.random.choice(len(X), len(X), replace=True)
        return X[idx]

    def compute_landscape(self, barcodes):
        """
        Compute a single persistence landscape.
        """
        return self.landscape.landscape(barcodes)

    def bootstrap_landscapes(self, barcode_fn, X):
        """
        Compute bootstrap ensemble of landscapes.
        barcode_fn: function that computes barcodes from X
        """
        landscapes = []
        for _ in range(self.num_bootstrap):
            X_resampled = self.resample(X)
            barcodes = barcode_fn(X_resampled)
            L = self.compute_landscape(barcodes)
            landscapes.append(L)
        return landscapes

    def average_landscape(self, landscapes):
        """
        Compute the mean persistence landscape.
        """
        return np.mean(np.array(landscapes), axis=0)

    def landscape_variance(self, landscapes):
        """
        Compute variance across bootstrap landscapes.
        """
        return np.var(np.array(landscapes), axis=0)
