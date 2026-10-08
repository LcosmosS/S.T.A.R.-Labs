"""
acsc.statistics
Functions to compute W2 distances, empirical p-values, and basic effect sizes.
"""

import numpy as np
from typing import Sequence, List
from acsc.tda_pipeline import persistence_wasserstein

def w2_between_diagrams(dgmA, dgmB) -> float:
    """
    Compute 2-Wasserstein distance between two persistence diagrams.
    """
    return float(persistence_wasserstein(np.asarray(dgmA), np.asarray(dgmB), order=2))

def empirical_p_value(observed: float, null_samples: Sequence[float]) -> float:
    """
    One-sided empirical p-value: proportion of null samples <= observed (smaller is better).
    Uses +1 numerator/denominator correction.
    """
    null = np.asarray(null_samples, dtype=float)
    m = len(null)
    count = np.sum(null <= observed)
    return float((1 + count) / (1 + m))

def effect_size(observed: float, null_samples: Sequence[float]) -> float:
    """
    Cohen-like effect size: (mean_null - observed) / std_null
    Positive means observed is smaller (better match) than null mean.
    """
    null = np.asarray(null_samples, dtype=float)
    mu = float(np.mean(null))
    sigma = float(np.std(null, ddof=1) if len(null) > 1 else 1.0)
    return float((mu - observed) / (sigma if sigma > 0 else 1.0))

