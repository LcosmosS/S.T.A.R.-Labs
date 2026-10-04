"""Fail-closed persistence computation for current S.T.A.R. code."""

from __future__ import annotations

import numpy as np

_persistence_cache = {}


def _validate_point_cloud(point_cloud, max_dim):
    points = np.asarray(point_cloud, dtype=float)
    if points.ndim != 2:
        raise ValueError("point_cloud must be a 2D array")
    if points.shape[0] == 0 or points.shape[1] == 0:
        raise ValueError("point_cloud must contain at least one point and feature")
    if not np.all(np.isfinite(points)):
        raise ValueError("point_cloud must contain only finite values")
    max_dim = int(max_dim)
    if max_dim < 0:
        raise ValueError("max_dim must be non-negative")
    return points, max_dim


def compute_persistence(point_cloud, max_dim=2):
    """Compute persistence diagrams using Ripser or GUDHI.

    Missing TDA dependencies are an execution error. This function never
    manufactures placeholder persistence diagrams.
    """
    points, max_dim = _validate_point_cloud(point_cloud, max_dim)
    key = (points.shape, points.dtype.str, points.tobytes(), max_dim)
    if key in _persistence_cache:
        return _persistence_cache[key]

    try:
        from ripser import ripser
    except ImportError as ripser_error:
        try:
            import gudhi
        except ImportError as gudhi_error:
            raise RuntimeError(
                "Ripser or GUDHI is required for persistence computation; "
                "placeholder diagrams are forbidden"
            ) from gudhi_error

        rips = gudhi.RipsComplex(points=points)
        st = rips.create_simplex_tree(max_dimension=max_dim + 1)
        st.compute_persistence()
        diagrams = [
            np.asarray(st.persistence_intervals_in_dimension(dim), dtype=float)
            for dim in range(max_dim + 1)
        ]
        result = {
            "dgms": diagrams,
            "betti": [len(d) for d in diagrams],
            "persistence_intervals": diagrams,
            "backend": "gudhi",
        }
    else:
        result = ripser(points, maxdim=max_dim)
        diagrams = result["dgms"]
        result = dict(result)
        result.update(
            {
                "betti": [len(d) for d in diagrams],
                "persistence_intervals": diagrams,
                "backend": "ripser",
            }
        )

    _persistence_cache[key] = result
    return result


compute_persistence_diagrams = compute_persistence
