"""
persistence_landscape.py
------------------------
Implements persistence landscapes for TDA stability analysis in the
S.T.A.R. Model and ECC.

A persistence landscape is a functional summary of a barcode:
λ_k(t) = k-th largest value of max(0, min(t - b_i, d_i - t))
"""

import numpy as np


class PersistenceLandscape:
    """
    Computes persistence landscapes from barcodes.
    """

    def __init__(self, resolution=200):
        self.resolution = resolution

    def landscape(self, barcodes):
        """
        Compute the persistence landscape λ_k(t) for a set of intervals.
        barcodes = [(birth, death), ...]
        """
        if len(barcodes) == 0:
            return np.zeros((1, self.resolution))

        t_min = min(b for b, d in barcodes)
        t_max = max(d for b, d in barcodes)
        t = np.linspace(t_min, t_max, self.resolution)

        layers = []

        for birth, death in barcodes:
            layer = np.maximum(0, np.minimum(t - birth, death - t))
            layers.append(layer)

        layers = np.array(layers)
        layers.sort(axis=0)
        layers = layers[::-1]  # descending order

        return layers

    def wasserstein_distance(self, L1, L2):
        """
        Compute Wasserstein distance between two landscapes.
        """
        return np.linalg.norm(L1 - L2)
