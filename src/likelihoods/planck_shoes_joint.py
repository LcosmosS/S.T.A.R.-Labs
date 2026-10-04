"""Planck compressed-prior plus SH0ES likelihood."""

from __future__ import annotations

import numpy as np
import pandas as pd


class PlanckSH0ESJointLikelihood:
    def __init__(self, planck_data, H0_shoes=73.04, sigma_shoes=1.04):
        if isinstance(planck_data, dict):
            self.planck = planck_data
        else:
            df = pd.read_csv(planck_data)
            self.planck = {
                "R": df["R"].iloc[0],
                "lA": df["lA"].iloc[0],
                "ombh2": df["ombh2"].iloc[0],
                "cov": df[
                    [f"cov{i}{j}" for i in range(3) for j in range(3)]
                ].values.reshape(3, 3),
            }

        covariance = np.asarray(self.planck["cov"], dtype=float)
        if covariance.shape != (3, 3) or not np.all(np.isfinite(covariance)):
            raise ValueError("Planck covariance must be a finite 3x3 matrix")
        self.cov_inv = np.linalg.inv(covariance)
        self.H0_shoes = float(H0_shoes)
        self.sigma_shoes = float(sigma_shoes)
        if self.sigma_shoes <= 0:
            raise ValueError("SH0ES uncertainty must be positive")

    def log_likelihood_planck(self, model):
        model_values = np.asarray(
            [model.R(), model.lA(), model.ombh2()],
            dtype=float,
        )
        observed = np.asarray(
            [self.planck["R"], self.planck["lA"], self.planck["ombh2"]],
            dtype=float,
        )
        if not np.all(np.isfinite(model_values)):
            return -np.inf
        delta = model_values - observed
        chi2 = float(delta.T @ self.cov_inv @ delta)
        return -0.5 * chi2 if np.isfinite(chi2) else -np.inf

    def log_likelihood_shoes(self, model):
        h0_model = float(model.H(0.0))
        if not np.isfinite(h0_model):
            return -np.inf
        return float(-0.5 * ((h0_model - self.H0_shoes) / self.sigma_shoes) ** 2)

    def log_likelihood(self, model):
        terms = (self.log_likelihood_planck(model), self.log_likelihood_shoes(model))
        if not np.all(np.isfinite(terms)):
            return -np.inf
        return float(sum(terms))

    def __call__(self, model):
        return self.log_likelihood(model)
