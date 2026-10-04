# Very small smoke test (safe)
import numpy as np, pandas as pd
from acsc import tda_pipeline as tdp

df = pd.read_csv("derived/acsc_projected_cremona_with_alt.csv")
coords = df[["x_ptd","y_ptd","z_ptd"]].to_numpy()
coords_small = coords[:100]   # << tiny
res = tdp.compute_persistence(coords_small, maxdim=1, thresh=None)
print("dgms lengths (small):", [len(d) for d in res.get("dgms", [])])

