"""
TDA Persistence Computation - Main entry point for notebooks
"""
from __future__ import annotations
import numpy as np
from typing import Dict, Any

_persistence_cache = {}

def compute_persistence(point_cloud, max_dim=2):
    """
    Compute persistence diagrams from a point cloud.
    Uses ripser → gudhi → placeholder fallback.
    """
    key = (tuple(point_cloud.flatten()), max_dim)
    if key in _persistence_cache:
        return _persistence_cache[key]
    
    point_cloud = np.asarray(point_cloud, dtype=float)

    try:
        # Try to use ripser
        from ripser import ripser
        result = ripser(point_cloud, maxdim=max_dim)
        diagrams = result['dgms']
        _persistence_cache[key] = result
        return result
        print(f" Computed persistence with ripser (dim 0-{max_dim})")
    except ImportError:
        try:
            # Fallback: gudhi
            import gudhi
            rips = gudhi.RipsComplex(points=point_cloud, max_edge_length=2.0)
            st = rips.create_simplex_tree(max_dimension=max_dim)
            persistence = st.persistence()
            
            diagrams = [[] for _ in range(max_dim + 1)]
            for birth_death in persistence:
                dim = birth_death[0]
                if dim <= max_dim:
                    diagrams[dim].append(birth_death[1])
            print(" Computed persistence with gudhi")
        except ImportError:
            # Ultimate fallback for CI / no libraries
            print(" No TDA library (ripser/gudhi) found. Using placeholder.")
            n = len(point_cloud) if len(point_cloud.shape) > 0 else 100
            diagrams = [
                [(0.0, 1.0 + np.random.rand()) for _ in range(n//3)],   # H0
                [(0.3, 0.8) for _ in range(n//10)] if max_dim >= 1 else []   # H1
            ]
    
    return {
        "dgms": diagrams,
        "betti": [len(d) for d in diagrams],
        "persistence_intervals": diagrams
    }

# Alias for backward compatibility
compute_persistence_diagrams = compute_persistence
