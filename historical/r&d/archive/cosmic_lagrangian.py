"""
cosmic_lagrangian.py
--------------------
Defines the symbolic–cosmic Lagrangian for the S.T.A.R. Model.

L = |∇M|² + λ * Ric(ω) + α * ρ_arith + β * K_entropy

This module:
- computes symbolic Ricci curvature
- constructs the S.T.A.R. Lagrangian density
- evaluates action integrals over symbolic manifolds
"""

import numpy as np
from ..entropy.entropy_field import EntropyField
from ..entropy.differential_forms import DifferentialForms
from ..physics.scalar_coupling import ScalarCoupling


class CosmicLagrangian:
    """
    Computes the symbolic–cosmic Lagrangian and action.
    """

    def __init__(self, lambda_coeff=0.1, alpha=0.01, beta=0.01):
        self.lambda_coeff = lambda_coeff
        self.alpha = alpha
        self.beta = beta
        self.M = EntropyField()
        self.forms = DifferentialForms()
        self.scalar = ScalarCoupling(alpha=alpha, beta=beta)

    def ricci_symbolic(self, x):
        """
        Compute symbolic Ricci curvature as trace of entropy Hessian.
        """
        H = self.M.hessian(x)
        return np.trace(H)

    def lagrangian_density(self, x, invariants):
        """
        L(x) = |∇M|² + λ * Ric(ω) + α * ρ_arith + β * K_entropy
        """
        grad = self.M.gradient(x)
        grad_term = np.dot(grad, grad)

        ricci_term = self.lambda_coeff * self.ricci_symbolic(x)

        rho = self.scalar.arithmetic_density(invariants)
        entropy_curv = self.ricci_symbolic(x)

        coupling_term = self.alpha * rho + self.beta * entropy_curv

        return grad_term + ricci_term + coupling_term

    def action(self, X, invariants_list):
        """
        Compute action integral over a point cloud X.
        """
        L_vals = [
            self.lagrangian_density(x, inv)
            for x, inv in zip(X, invariants_list)
        ]
        return np.sum(L_vals)
