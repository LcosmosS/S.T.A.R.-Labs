import numpy as np, pandas as pd
df = pd.read_csv("derived/acsc_projected_cremona_with_alt.csv")
coords = df[["x_ptd","y_ptd","z_ptd"]].to_numpy()
print("shape:", coords.shape)
print("per-axis min/max/std:", np.min(coords,0), np.max(coords,0), np.std(coords,0))
