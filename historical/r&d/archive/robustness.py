"""Ablation studies and robustness validation."""
import numpy as np

def subsample_stability(coords, fractions=[0.5, 0.75, 0.9]):
    """Test stability under subsampling."""
    results = {}
    for frac in fractions:
        n_keep = int(len(coords) * frac)
        idx = np.random.choice(len(coords), n_keep, replace=False)
        results[f"frac_{frac}"] = coords[idx]
    return results

def gaussian_jitter_test(coords, sigma=0.01, n_trials=10):
    """Test robustness to Gaussian noise."""
    return [coords + np.random.normal(0, sigma, coords.shape) 
            for _ in range(n_trials)]
