import numpy as np, pandas as pd
df = pd.read_csv("derived/acsc_projected_cremona_realproj.csv")
coords = df[["x_prim","y_prim","z_prim"]].to_numpy()
# not all equal to index
print("Any coordinate equal to index sequence?", np.all(coords == np.arange(len(coords))[:,None]))
# check distributions
print("x_prim range:", coords[:,0].min(), coords[:,0].max())
print("y_prim range:", coords[:,1].min(), coords[:,1].max())
print("z_prim range:", coords[:,2].min(), coords[:,2].max())
