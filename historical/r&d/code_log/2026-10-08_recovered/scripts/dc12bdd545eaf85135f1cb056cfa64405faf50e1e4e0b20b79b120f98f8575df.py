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

def compute_persistence(coords, maxdim=2, thresh=None):
    coords = np.asarray(coords)
    if _HAS_RIPSER:
        params = {'maxdim': maxdim}
        if thresh is not None:
            params['thresh'] = float(thresh)
        return ripser(coords, **params)
    elif _HAS_GUDHI:
        rips = gd.RipsComplex(points=coords, max_edge_length=thresh if thresh is not None else np.inf)
        st = rips.create_simplex_tree(max_dimension=maxdim+1)
        st.compute_persistence()
        dgms = [np.array(st.persistence_intervals_in_dimension(k)) for k in range(maxdim+1)]
        return {'dgms': dgms}
    else:
        # fallback: return empty diagrams
        return {'dgms': [np.empty((0,2)) for _ in range(maxdim+1)]}
