"""
cosmic_web_alignment.py
-----------------------
Implements symbolic–cosmic alignment metrics for the S.T.A.R. Model.

This module compares:
- ACSC-projected arithmetic structure
- ECC entropy curvature fields
- observed cosmic web filaments and voids

It provides:
- alignment scores
- filament–entropy ridge correlation
- void–entropy basin matching
"""

import numpy as np
from scipy.spatial.distance import cdist
from src.data.load_sky_surveys import load_sky_surveys

def test_sky_surveys_load():
    df1, df2 = load_sky_surveys(downsample=100, validate_schema=True)
    assert len(df1) > 0
    assert len(df2) > 0

class CosmicWebAlignment:
    """
    Computes alignment between symbolic entropy fields and cosmic web structure.
    """

    def __init__(self, smoothing=1.0):
        self.smoothing = smoothing

    def normalize(self, v):
        """
        Normalize a vector.
        """
        n = np.linalg.norm(v) + 1e-12
        return v / n

    def ridge_alignment(self, entropy_gradients, filament_vectors):
        """
        Compute alignment between entropy gradient directions and filament directions.

        alignment = <∇M, filament_dir>
        """
        alignments = []
        for g, f in zip(entropy_gradients, filament_vectors):
            g_norm = self.normalize(g)
            f_norm = self.normalize(f)
            alignments.append(np.dot(g_norm, f_norm))
        return np.mean(alignments)

    def basin_alignment(self, entropy_values, void_centers, points):
        """
        Match entropy minima to void centers using nearest-neighbor distances.
        """
        entropy_minima = np.argsort(entropy_values)[: len(void_centers)]
        selected_points = points[entropy_minima]
        D = cdist(selected_points, void_centers)
        return np.mean(np.min(D, axis=1))

    def combined_alignment(self, entropy_gradients, filament_vectors,
                           entropy_values, void_centers, points):
        """
        Combined symbolic–cosmic alignment score.
        """
        ridge = self.ridge_alignment(entropy_gradients, filament_vectors)
        basin = self.basin_alignment(entropy_values, void_centers, points)
        return {
            "ridge_alignment": ridge,
            "basin_alignment": basin,
            "combined_score": ridge - self.smoothing * basin
        }
