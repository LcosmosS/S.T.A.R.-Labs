# Compute persistence for a small sample to verify pipeline integration
sample_coords = arith_aligned[:2000]  # keep small to avoid heavy compute in notebook
res = compute_persistence(sample_coords, maxdim=2, thresh=None)
# res['dgms'] contains diagrams per dimension
for k, dgm in enumerate(res.get("dgms", [])):
    print(f"Dimension {k}: {len(dgm)} features")
