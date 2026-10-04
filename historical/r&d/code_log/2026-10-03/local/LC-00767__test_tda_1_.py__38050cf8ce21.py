"""
acsc.tda_pipeline
Thin wrapper to compute Vietoris-Rips persistence diagrams using Ripser or GUDHI.
Provides utilities to compute persistence diagrams and persistence summaries.
"""

from typing import Optional, Tuple
import numpy as np

# Prefer ripser for speed; fallback to gudhi if available.
try:
    from ripser import ripser
    from persim import PersistenceImager, wasserstein
    _HAS_RIPSER = True
except Exception:
    _HAS_RIPSER = False

try:
    import gudhi as gd
    _HAS_GUDHI = True
except Exception:
    _HAS_GUDHI = False

def compute_persistence(coords: np.ndarray,
                        maxdim: int = 2,
                        thresh: Optional[float] = None) -> dict:
    """
    Compute persistence diagrams for coords (n_points, d).
    Returns ripser-style dict with 'dgms' key (list of diagrams per dimension).
    """
    coords = np.asarray(coords)
    if _HAS_RIPSER:
        params = {"maxdim": maxdim}
        if thresh is not None:
            params["thresh"] = float(thresh)
        result = ripser(coords, **params)
        return result
    elif _HAS_GUDHI:
        # rudimentary GUDHI pipeline: compute RipsComplex -> simplex tree -> persistence
        rips = gd.RipsComplex(points=coords, max_edge_length=thresh if thresh is not None else np.inf)
        st = rips.create_simplex_tree(max_dimension=maxdim + 1)
        st.compute_persistence()
        dgms = []
        for k in range(maxdim + 1):
            dgm = np.array([pt for pt in st.persistence_intervals_in_dimension(k)])
            dgms.append(dgm)
        return {"dgms": dgms}
    else:
        raise RuntimeError("Neither ripser nor gudhi is available. Install one of them.")

def persistence_wasserstein(dgm1, dgm2, order: int = 2, internal_p: int = 2) -> float:
    """
    Compute p-Wasserstein distance between two diagrams using persim.wasserstein if available.
    dgm1/dgm2: numpy arrays of shape (m,2)
    """
    try:
        from persim import wasserstein
        return wasserstein(dgm1, dgm2, matching=False, order=order, internal_p=internal_p)
    except Exception:
        # fallback simple bottleneck via numpy (approximate): use max absolute difference of sorted births/deaths
        b1 = np.sort(dgm1[:, 0] - dgm1[:, 1]) if len(dgm1) else np.array([0.0])
        b2 = np.sort(dgm2[:, 0] - dgm2[:, 1]) if len(dgm2) else np.array([0.0])
        m = min(len(b1), len(b2))
        if m == 0:
            return float(np.max(np.abs(np.concatenate([b1, b2]))))
        return float(np.mean(np.abs(b1[:m] - b2[:m])))

