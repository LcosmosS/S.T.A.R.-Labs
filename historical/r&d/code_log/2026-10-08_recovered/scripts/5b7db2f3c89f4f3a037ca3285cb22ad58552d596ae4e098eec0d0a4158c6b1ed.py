"""
Hubble Tension Quantification
=============================

Computes:
- ΔH0
- σ-level tension
- χ² difference
- AIC/BIC comparison
"""

from __future__ import annotations
import numpy as np


def compute_H0_tension(H0_lcdm, H0_star, sigma_lcdm, sigma_star):
    delta = abs(H0_lcdm - H0_star)
    sigma = np.sqrt(sigma_lcdm**2 + sigma_star**2)
    tension_sigma = delta / sigma
    return tension_sigma


def chi2(model, z, mu_obs, sigma_mu):
    mu_model = np.array([model.distance_modulus(zi) for zi in z])
    return np.sum(((mu_obs - mu_model) / sigma_mu)**2)


def aic(chi2, k):
    return chi2 + 2*k


def bic(chi2, k, n):
    return chi2 + k*np.log(n)
