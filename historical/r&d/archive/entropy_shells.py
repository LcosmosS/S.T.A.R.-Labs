"""
entropy_shells.py
-----------------
Implements entropy shell stratification for the S.T.A.R. Model.

Entropy shells M_n are defined by threshold intervals:
M_n = { x ∈ M_symbolic | τ_n ≤ M(x) < τ_{n+1} }

This module:
- computes entropy values
- assigns points to shells
- constructs nested shell structures
- computes shell curvature statistics
"""

import numpy as np
from .entropy_field import EntropyField


class EntropyShells:
    """
    Stratifies the symbolic manifold into entropy shells.
    """

    def __init__(self, entropy_field=None):
        self.M = entropy_field if entropy_field else EntropyField()

    def assign_shell(self, x, thresholds):
        """
        Assign a point x to an entropy shell M_n.
        """
        value = self.M.entropy(x)
        for i in range(len(thresholds) - 1):
            if thresholds[i] <= value < thresholds[i + 1]:
                return i
        return len(thresholds) - 1

    def shell_structure(self, X, thresholds):
        """
        Build full shell structure for a point cloud X.
        """
        shells = {i: [] for i in range(len(thresholds))}
        for x in X:
            n = self.assign_shell(x, thresholds)
            shells[n].append(x)
        return shells

    def shell_curvature(self, X):
        """
        Compute average entropy curvature (trace of Hessian) for each point.
        """
        curvatures = []
        for x in X:
            H = self.M.hessian(x)
            curvatures.append(np.trace(H))
        return np.array(curvatures)
