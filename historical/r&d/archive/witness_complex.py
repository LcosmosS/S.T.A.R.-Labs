"""
witness_complex.py
------------------
Implements a Witness Complex for TDA stability analysis in the
S.T.A.R. Model and ECC.

This module constructs:
- landmark selection
- witness assignment
- simplicial complex generation
"""

import numpy as np
from scipy.spatial.distance import cdist


class WitnessComplex:
    """
    Builds a witness complex from a point cloud.
    """

    def __init__(self, num_landmarks=20):
        self.num_landmarks = num_landmarks

    def select_landmarks(self, X):
        """
        Randomly select landmark points.
        """
        idx = np.random.choice(len(X), self.num_landmarks, replace=False)
        return X[idx]

    def assign_witnesses(self, X, L):
        """
        Assign each point in X to its nearest landmark.
        """
        D = cdist(X, L)
        return np.argmin(D, axis=1)

    def build_complex(self, X):
        """
        Construct the witness complex (0- and 1-simplices).
        """
        L = self.select_landmarks(X)
        W = self.assign_witnesses(X, L)

        edges = set()
        for i in range(len(X)):
            for j in range(i + 1, len(X)):
                if W[i] == W[j]:
                    edges.add((i, j))

        return {
            "landmarks": L,
            "edges": list(edges)
        }
