"""Pantheon+ likelihood validation utilities."""

from __future__ import annotations

import numpy as np


class PantheonPlusLikelihood:
    def __init__(self, data):
        try:
            self.z = np.asarray(data["z"], dtype=float)
            self.mu = np.asarray(data["mu"], dtype=float)
            self.sigma = np.asarray(data["sigma_mu"], dtype=float)
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                "Pantheon+ payload must contain numeric z, mu, sigma_mu arrays"
            ) from exc

        if self.z.size == 0:
            raise ValueError("Pantheon+ dataset is empty")
        if not (self.z.shape == self.mu.shape == self.sigma.shape):
            raise ValueError("Pantheon+ arrays must have equal shapes")
        if not (
            np.all(np.isfinite(self.z))
            and np.all(np.isfinite(self.mu))
            and np.all(np.isfinite(self.sigma))
        ):
            raise ValueError("Pantheon+ dataset contains non-finite values")
        if np.any(self.z < 0) or np.any(self.sigma <= 0):
            raise ValueError(
                "Pantheon+ requires non-negative z and positive uncertainties"
            )

    def chi2(self, model):
        mu_model = np.asarray(model.mu(self.z), dtype=float)
        if mu_model.shape != self.mu.shape or not np.all(np.isfinite(mu_model)):
            raise ValueError("model returned invalid Pantheon+ distance moduli")
        return float(np.sum(((self.mu - mu_model) / self.sigma) ** 2))

    def log_likelihood(self, model):
        return -0.5 * self.chi2(model)

    def __call__(self, model):
        return self.log_likelihood(model)
