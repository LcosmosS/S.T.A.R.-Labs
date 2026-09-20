"""
symbolic_manifold.py
--------------------
Defines the symbolic entropy manifold M_symbolic used in the
Entropy Cohomology Conjecture (ECC) and the S.T.A.R. Model.

This module constructs:
- symbolic coordinates
- entropy shells M_n
- projection vector fields
- symbolic curvature tensors
"""

import numpy as np
from .entropy_field import EntropyField


class SymbolicManifold:
    """
    Represents the symbolic entropy manifold M_symbolic.
    """

    def __init__(self, entropy_field=None):
        self.M = entropy_field if entropy_field else EntropyField()

    def point(self, invariants):
        """
        Construct a symbolic point x in M_symbolic from arithmetic invariants.
        invariants = [logR, r, L_cosmo(1)]
        """
        return np.array(invariants, dtype=float)

    def entropy_shell(self, x, thresholds):
        """
        Assign x to an entropy shell M_n based on thresholds.
        """
        value = self.M.entropy(x)
        for i in range(len(thresholds) - 1):
            if thresholds[i] <= value < thresholds[i + 1]:
                return i
        return len(thresholds) - 1

    def projection_vector_field(self, x):
        """
        Compute the symbolic projection vector field V_phi(x).
        """
        grad = self.M.gradient(x)
        norm = np.linalg.norm(grad) + 1e-12
        return grad / norm

    def curvature_tensor(self, x):
        """
        Return the entropy curvature tensor K_ij.
        """
        return self.M.hessian(x)
