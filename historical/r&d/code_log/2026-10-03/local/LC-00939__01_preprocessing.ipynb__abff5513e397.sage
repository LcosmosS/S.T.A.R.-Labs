import numpy as np, pandas as pd
df = pd.read_csv("derived/acsc_projected_cremona_ptd_aligned.csv")  # or your aligned file
coords = df[["x_ptd_al","y_ptd_al","z_ptd_al"]].to_numpy()
np.savez_compressed("derived/coords_ptd_al.npz", coords=coords)
print("Saved coords shape:", coords.shape)
