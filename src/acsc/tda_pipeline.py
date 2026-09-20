import numpy as np

try:
    from gudhi import RipsComplex
except Exception as exc:
    RipsComplex = None
    _GUDHI_IMPORT_ERROR = exc

def compute_persistence(coords, maxdim=1, thresh=None):
    """Compute Vietoris-Rips persistence; fail explicitly if GUDHI is unavailable."""
    coords = np.asarray(coords, dtype=float)
    if coords.ndim != 2:
        raise ValueError("coords must be a 2D array")
    if coords.shape[0] == 0:
        return {"dgms": [np.empty((0, 2)) for _ in range(maxdim + 1)]}
    if RipsComplex is None:
        raise RuntimeError(
            "GUDHI is required for controlled persistence computation"
        ) from _GUDHI_IMPORT_ERROR
    kwargs = {"points": coords}
    if thresh is not None:
        kwargs["max_edge_length"] = float(thresh)
    rips = RipsComplex(**kwargs)
    st = rips.create_simplex_tree(max_dimension=maxdim + 1)
    st.compute_persistence()
    return {
        "dgms": [
            np.asarray(st.persistence_intervals_in_dimension(k), dtype=float)
            for k in range(maxdim + 1)
        ]
    }

def persistence_wasserstein(dgm1, dgm2, order=2, internal_p=2):
    """Compute the registered Wasserstein metric; fail if persim is unavailable."""
    try:
        from persim import wasserstein
    except Exception as exc:
        raise RuntimeError(
            "persim is required for controlled Wasserstein comparison"
        ) from exc
    return float(wasserstein(
        np.asarray(dgm1, dtype=float),
        np.asarray(dgm2, dtype=float),
        matching=False,
        order=order,
        internal_p=internal_p,
    ))
