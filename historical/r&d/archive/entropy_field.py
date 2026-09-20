"""
entropy_field.py
----------------
Defines the entropy field M(x) on the symbolic manifold M_symbolic,
along with its differential 1-form θ = dM and curvature tensor K_ij.

This module implements the entropy machinery used in the
Entropy Cohomology Conjecture (ECC) and the S.T.A.R. Model.
"""

import numpy as np


class EntropyField:
    """
    Represents the symbolic entropy field M(x) defined over the
    arithmetic-projected manifold M_symbolic.

    M(x) = - Σ p_i(x) log p_i(x)
    where p_i(x) = x_i / Σ_j x_j
    """

    def __init__(self, epsilon=1e-12):
        self.eps = epsilon

    def normalize(self, x):
        """
        Normalize coordinates into probability-like weights p_i(x).
        """
        x = np.array(x, dtype=float)
        total = np.sum(x) + self.eps
        return x / total

    def entropy(self, x):
        """
        Compute the symbolic entropy M(x).
        """
        p = self.normalize(x)
        return -np.sum(p * np.log(p + self.eps))

    def gradient(self, x):
        """
        Compute the entropy gradient θ = dM.
        """
        p = self.normalize(x)
        logp = np.log(p + self.eps)
        return -(logp + 1 - np.sum(p * (logp + 1)))

    def hessian(self, x):
        """
        Compute the entropy Hessian K_ij = ∂²M / ∂x_i ∂x_j.
        """
        p = self.normalize(x)
        n = len(p)
        H = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                if i == j:
                    H[i, j] = -(1 / (p[i] + self.eps)) * (p[i] * (1 - p[i]))
                else:
                    H[i, j] = (p[i] * p[j]) / (p[i] + self.eps)

        return H

    def differential_form(self, x):
        """
        Return the 1-form θ = dM as a numpy vector.
        """
        return self.gradient(x)
