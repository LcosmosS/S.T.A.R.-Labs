# acsc/null_models.py
"""Null model generation for statistical testing."""
import numpy as np

def generate_null_point_cloud(n_points: int, dimension: int = 3) -> np.ndarray:
    """Generate random null point cloud."""
    return np.random.randn(n_points, dimension)

def compute_null_metric(null_cloud, metric_func):
    """Compute metric on null cloud."""
    return metric_func(null_cloud)
