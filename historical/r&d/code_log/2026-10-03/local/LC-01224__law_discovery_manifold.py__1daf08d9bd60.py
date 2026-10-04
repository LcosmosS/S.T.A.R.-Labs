"""
law_discovery_manifold.py
-------------------------
Defines the constrained search space for symbolic regression
in the S.T.A.R. Model.

Implements:
- restricted primitive set
- max tree depth
- Lipschitz penalty
- isogeny-invariance constraint
- null-scramble tests
"""

import numpy as np
from src.data.load_sky_surveys import load_sky_surveys

def test_sky_surveys_load():
    df1, df2 = load_sky_surveys(downsample=100, validate_schema=True)
    assert len(df1) > 0
    assert len(df2) > 0


class LawDiscoveryManifold:
    """
    Constrained symbolic regression search space.
    """

    def __init__(self, max_depth=6):
        self.max_depth = max_depth
        self.primitives = [
            "add", "sub", "mul", "div",
            "log", "exp", "arctan"
        ]

    def lipschitz_penalty(self, f_values, x_values):
        """
        Compute Lipschitz penalty ||f(x_i) - f(x_j)|| / ||x_i - x_j||.
        """
        penalties = []
        for i in range(len(x_values)):
            for j in range(i + 1, len(x_values)):
                dx = np.linalg.norm(x_values[i] - x_values[j])
                df = abs(f_values[i] - f_values[j])
                if dx > 0:
                    penalties.append(df / dx)
        return np.mean(penalties)

    def isogeny_invariant(self, f, curves):
        """
        Test f(E1) == f(E2) for isogenous curves.
        curves = list of (E1, E2) pairs
        """
        for E1, E2 in curves:
            if abs(f(E1) - f(E2)) > 1e-6:
                return False
        return True

    def null_scramble(self, f, scrambled_data):
        """
        Ensure f does NOT perform well on scrambled data.
        """
        outputs = [f(x) for x in scrambled_data]
        variance = np.var(outputs)
        return variance > 0.1  # placeholder threshold

    def admissible(self, f, data, isogeny_pairs, scrambled):
        """
        Check if f satisfies all constraints.
        """
        f_values = np.array([f(x) for x in data])

        return (
            self.lipschitz_penalty(f_values, data) < 10.0 and
            self.isogeny_invariant(f, isogeny_pairs) and
            self.null_scramble(f, scrambled)
        )
