"""
Planck + SH0ES Joint Likelihood
===============================

Supports:
- Planck compressed distance priors (2015 or 2018 reconstructed)
- SH0ES H0 measurement

Works with embedded Python dictionaries or legacy CSV files.
"""

from __future__ import annotations
import numpy as np
import pandas as pd


class PlanckSH0ESJointLikelihood:
    def __init__(self, planck_data, H0_shoes=73.04, sigma_shoes=1.04):
        """
        planck_data can be:
        - a dict (embedded data module)
        - a CSV file path (legacy mode)
        """
        if isinstance(planck_data, dict):
            # Embedded data mode
            self.planck = planck_data
        else:
            # Legacy CSV mode
            df = pd.read_csv(planck_data)
            self.planck = {
                "R": df["R"].iloc[0],
                "lA": df["lA"].iloc[0],
                "ombh2": df["ombh2"].iloc[0],
                "cov": df[["cov00", "cov01", "cov02",
                           "cov10", "cov11", "cov12",
                           "cov20", "cov21", "cov22"]].values.reshape(3, 3)
            }

        self.H0_shoes = H0_shoes
        self.sigma_shoes = sigma_shoes

    # -----------------------------
    # Planck compressed likelihood
    # -----------------------------
    def log_likelihood_planck(self, model):
        # Model predictions
        R_model = model.R()
        lA_model = model.lA()
        ombh2_model = model.ombh2()

        # Observed values
        R_obs = self.planck["R"]
        lA_obs = self.planck["lA"]
        ombh2_obs = self.planck["ombh2"]
        cov = np.array(self.planck["cov"])

        # Residual vector
        delta = np.array([
            R_model - R_obs,
            lA_model - lA_obs,
            ombh2_model - ombh2_obs
        ])

        chi2 = delta.T @ np.linalg.inv(cov) @ delta
        return -0.5 * chi2

    # -----------------------------
    # SH0ES likelihood
    # -----------------------------
    def log_likelihood_shoes(self, model):
        H0_model = model.H(0)
        return -0.5 * ((H0_model - self.H0_shoes) / self.sigma_shoes)**2

    # -----------------------------
    # Total likelihood
    # -----------------------------
    def log_likelihood(self, model):
        return (
            self.log_likelihood_planck(model)
            + self.log_likelihood_shoes(model)
        )
