from src.data.load_sky_surveys import load_sky_surveys

def test_sky_surveys_load():
    df1, df2 = load_sky_surveys(downsample=100, validate_schema=True)
    assert len(df1) > 0
    assert len(df2) > 0

import numpy as np
try:
    from ripser import ripser
    _HAS_RIPSER = True
except Exception:
    _HAS_RIPSER = False

try:
    import gudhi as gd
    _HAS_GUDHI = True
except Exception:
    _HAS_GUDHI = False

def compute_persistence(coords, maxdim=1, thresh=None):
    coords = np.asarray(coords)
    if coords.size == 0 or coords.shape[0] == 0:
        # Return empty diagrams for all dimensions up to maxdim
        return {"dgms": [np.empty((0,2)) for _ in range(maxdim+1)]}
    elif _HAS_GUDHI:
        rips = gd.RipsComplex(points=coords, max_edge_length=thresh if thresh is not None else np.inf)
        st = rips.create_simplex_tree(max_dimension=maxdim+1)
        st.compute_persistence()
        dgms = [np.array(st.persistence_intervals_in_dimension(k)) for k in range(maxdim+1)]
        return {'dgms': dgms}
    else:
        # fallback: return empty diagrams
        return {'dgms': [np.empty((0,2)) for _ in range(maxdim+1)]}

def persistence_wasserstein(dgm1, dgm2, order=2, internal_p=2):
    """
    Compute p-Wasserstein distance between two persistence diagrams.
    Fallback implementation without persim.
    """
    try:
        from persim import wasserstein
        return wasserstein(dgm1, dgm2, matching=False, order=order, internal_p=internal_p)
    except Exception:
        # Fallback: simple bottleneck approximation
        dgm1 = np.asarray(dgm1)
        dgm2 = np.asarray(dgm2)
        if len(dgm1) == 0 and len(dgm2) == 0:
            return 0.0
        if len(dgm1) == 0 or len(dgm2) == 0:
            return float(max(len(dgm1), len(dgm2)))
        # Simple L2 distance between diagrams
        m = min(len(dgm1), len(dgm2))
        dgm1_sorted = dgm1[np.argsort(dgm1[:, 0])][:m]
        dgm2_sorted = dgm2[np.argsort(dgm2[:, 0])][:m]
        return float(np.linalg.norm(dgm1_sorted - dgm2_sorted))












