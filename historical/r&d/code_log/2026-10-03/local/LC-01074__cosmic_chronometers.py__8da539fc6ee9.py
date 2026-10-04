"""
Cosmic Chronometer Likelihood
=============================

Gaussian likelihood for H(z) measurements from cosmic chronometers.
"""

from __future__ import annotations
import numpy as np
import pandas as pd


# ----------------------------------------------------------------------
# Embedded Cosmic Chronometer dataset (Moresco et al. 2022)
# ----------------------------------------------------------------------
COSMIC_CHRONOMETERS = {
    "z": [
        0.07, 0.09, 0.12, 0.17, 0.179, 0.199, 0.2, 0.27, 0.28, 0.352,
        0.38, 0.4, 0.48, 0.593, 0.68, 0.781, 0.875, 0.88, 0.9, 1.037,
        1.3, 1.363, 1.43, 1.53, 1.75, 1.965
    ],
    "H": [
        69.0, 69.0, 68.6, 83.0, 75.0, 75.0, 72.9, 77.0, 88.8, 83.0,
        81.5, 82.8, 97.0, 104.0, 92.0, 105.0, 125.0, 90.0, 117.0, 154.0,
        168.0, 160.0, 177.0, 140.0, 202.0, 186.5
    ],
    "sigma": [
        19.6, 12.0, 26.2, 8.0, 4.0, 5.0, 29.6, 14.0, 36.6, 14.0,
        1.9, 10.0, 62.0, 13.0, 8.0, 12.0, 17.0, 40.0, 23.0, 20.0,
        17.0, 33.0, 18.0, 14.0, 40.0, 50.4
    ],
}


# ----------------------------------------------------------------------
# Cosmic Chronometer Likelihood Class
# ----------------------------------------------------------------------
class CosmicChronometers:
    """
    Cosmic Chronometer H(z) likelihood.

    Supports:
    - embedded Python dictionaries (CI‑safe)
    - pandas DataFrames

    Provides:
    - strict validation
    - vectorized Gaussian log-likelihood
    - numerical stability checks
    - API compatibility with DESIBAO and PlanckSH0ESJointLikelihood
    """

    def __init__(self, data):
        self.z, self.H, self.sigma = self._parse_and_validate(data)

    # ------------------------------------------------------------------
    # Parsing + Validation
    # ------------------------------------------------------------------
    def _parse_and_validate(self, data):
        if isinstance(data, dict):
            try:
                z = np.asarray(data["z"], dtype=float)
                H = np.asarray(data["H"], dtype=float)
                sigma_key = "sigma" if "sigma" in data else "sigma_H"
                sigma = np.asarray(data[sigma_key], dtype=float)
            except KeyError as e:
                raise KeyError(f"Missing required key in CC data: {e}")

        elif isinstance(data, pd.DataFrame):
            for key in ["z", "H", "sigma"]:
                if key not in data.columns:
                    raise KeyError(f"Missing required column '{key}' in CC DataFrame")
            z = data["z"].to_numpy(dtype=float)
            H = data["H"].to_numpy(dtype=float)
            sigma = data["sigma"].to_numpy(dtype=float)

        else:
            raise TypeError("CosmicChronometers data must be a dict or pandas.DataFrame")

        # Shape validation
        if not (z.shape == H.shape == sigma.shape):
            raise ValueError(
                f"Shape mismatch: z {z.shape}, H {H.shape}, sigma {sigma.shape}"
            )

        # Finite values
        if not np.all(np.isfinite(z)):
            raise ValueError("Non-finite values detected in CC redshifts z")
        if not np.all(np.isfinite(H)):
            raise ValueError("Non-finite values detected in CC H(z) measurements")
        if not np.all(np.isfinite(sigma)):
            raise ValueError("Non-finite values detected in CC uncertainties sigma")

        # Positive uncertainties
        if np.any(sigma <= 0):
            raise ValueError("All CC sigma values must be strictly positive")

        return z, H, sigma

    # ------------------------------------------------------------------
    # Log-likelihood
    # ------------------------------------------------------------------
    def log_likelihood(self, model):
        H_model = np.asarray(model.H(self.z), dtype=float)

        if H_model.shape != self.H.shape:
            raise ValueError(
                f"Model.H(z) returned shape {H_model.shape}, expected {self.H.shape}"
            )

        if not np.all(np.isfinite(H_model)):
            raise ValueError("Model returned non-finite H(z) values")

        resid = (self.H - H_model) / self.sigma
        chi2 = np.sum(resid * resid)
        return -0.5 * chi2

    # ------------------------------------------------------------------
    @property
    def ndata(self):
        return self.z.size

    def __repr__(self):
        return f"CosmicChronometers(ndata={self.ndata})"
