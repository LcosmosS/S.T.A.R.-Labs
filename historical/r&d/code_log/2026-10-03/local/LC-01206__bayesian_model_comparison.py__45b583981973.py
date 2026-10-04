"""
Bayesian Model Comparison
=========================

Computes:
- log evidence via Laplace approximation
- Bayes factor
- Jeffreys scale classification
"""

from __future__ import annotations
import numpy as np


def log_evidence_laplace(chi2_min, k, n):
    """
    Laplace approximation:
    log Z ≈ -0.5 χ²_min - (k/2) log(n)
    """
    return -0.5 * chi2_min - (k/2) * np.log(n)


def bayes_factor(logZ1, logZ2):
    return np.exp(logZ1 - logZ2)


def jeffreys_scale(B):
    if B < 1:
        return "Negative evidence"
    if B < 3:
        return "Barely worth mentioning"
    if B < 10:
        return "Substantial"
    if B < 30:
        return "Strong"
    if B < 100:
        return "Very strong"
    return "Decisive"
