import numpy as np

def null_random_spatial(n_points, bbox):
    bbox = np.asarray(bbox, dtype=float)
    mins = bbox[0]
    maxs = bbox[1]
    return np.random.uniform(mins, maxs, size=(n_points, mins.size))

def null_permuted_invariant(records, invariant_key, project_fn):
    recs = list(records)
    vals = [r.get(invariant_key) for r in recs]
    perm = np.random.permutation(vals)
    recs_perm = []
    for r, v in zip(recs, perm):
        r2 = dict(r)
        r2[invariant_key] = v
        recs_perm.append(r2)
    return project_fn(recs_perm)
