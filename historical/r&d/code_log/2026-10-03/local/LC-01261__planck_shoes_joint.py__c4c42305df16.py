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
        self.cov_inv = np.linalg.inv(np.array(self.planck["cov"]))
        self.H0_shoes = H0_shoes
        self.sigma_shoes = sigma_shoes
        print(f"PlanckSH0ESJointLikelihood initialized (H0_SH0ES = {H0_shoes})")

    # -----------------------------
    # Planck compressed likelihood
    # -----------------------------
    def log_likelihood_planck(self, model):
        try:
            R_model = getattr(model, "R", lambda: np.nan)()
            lA_model = getattr(model, "lA", lambda: np.nan)()
            ombh2_model = getattr(model, "ombh2", lambda: np.nan)()

            R_obs = self.planck["R"]
            lA_obs = self.planck["lA"]
            ombh2_obs = self.planck["ombh2"]
            cov = np.array(self.planck["cov"])

            delta = np.array(
                [R_model - R_obs, lA_model - lA_obs, ombh2_model - ombh2_obs]
            )
            chi2 = delta.T @ self.cov_inv @ delta

            logp = -0.5 * chi2
            print(
                f"  Planck → R={R_model:.4f}, lA={lA_model:.4f}, ombh2={ombh2_model:.6f} | logp={logp:.4f}"
            )
            return logp

        except Exception as e:
            print(f"  Planck likelihood ERROR: {e}")
            return -np.inf

    # -----------------------------
    # SH0ES likelihood
    # -----------------------------
    def log_likelihood_shoes(self, model):
        try:
            H0_model = getattr(model, "H", lambda z: np.nan)(0)
            if not np.isfinite(H0_model):
                H0_model = getattr(model, "H0", np.nan)

            logp = -0.5 * ((H0_model - self.H0_shoes) / self.sigma_shoes) ** 2
            print(f"  SH0ES  → H0_model={H0_model:.3f} | logp={logp:.4f}")
            return logp
        except Exception as e:
            print(f"  SH0ES likelihood ERROR: {e}")
            return -np.inf

    def __call__(self, theta):
        """Main entry point with full diagnostics"""
        print(f"\n[Likelihood] theta = {theta}")
        try:
            logp_planck = self.log_likelihood_planck(
                None
            )  # placeholder - will be fixed later
            logp_shoes = self.log_likelihood_shoes(None)
            total = logp_planck + logp_shoes

            print(f"[Likelihood] TOTAL logp = {total:.4f}")
            return total
        except Exception as e:
            print(f"[Likelihood] CRITICAL ERROR: {e}")
            return -np.inf

    # -----------------------------
    # Total likelihood
    # -----------------------------
    def log_likelihood(self, model):
        return self.log_likelihood_planck(model) + self.log_likelihood_shoes(model)
