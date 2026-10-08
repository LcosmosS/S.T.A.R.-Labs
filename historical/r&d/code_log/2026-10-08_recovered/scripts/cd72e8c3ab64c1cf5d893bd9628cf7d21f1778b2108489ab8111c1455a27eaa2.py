"""
S.T.A.R. Model Parameter Inference
==================================

Fits symbolic H(z) models to distance modulus data using:
- Maximum likelihood estimation (MLE)
- Gradient-free optimization (Nelder-Mead)
"""

from __future__ import annotations
import numpy as np
from scipy.optimize import minimize
from src.physics.symbolic_cosmology import SymbolicCosmology


class STARParameterInference:
    def __init__(self, H_expr, param_names):
        """
        Parameters
        ----------
        H_expr : str
            Symbolic expression for H(z)
        param_names : list[str]
            Names of free parameters in the expression
        """
        self.H_expr = H_expr
        self.param_names = param_names

    def _make_model(self, theta):
        params = dict(zip(self.param_names, theta))
        return SymbolicCosmology(self.H_expr, params)

    def neg_log_likelihood(self, theta, z, mu_obs, sigma_mu):
        model = self._make_model(theta)
        mu_model = np.array([model.distance_modulus(zi) for zi in z])
        chi2 = np.sum(((mu_obs - mu_model) / sigma_mu)**2)
        return 0.5 * chi2

    def fit(self, z, mu_obs, sigma_mu, theta0):
        result = minimize(
            self.neg_log_likelihood,
            theta0,
            args=(z, mu_obs, sigma_mu),
            method="Nelder-Mead"
        )
        best_params = dict(zip(self.param_names, result.x))
        return best_params, result
