from acsc.quantile import QuantileAligner
import numpy as np, pandas as pd

# load reference cloud (choose a representative sample or external cosmic cloud)
ref = pd.read_csv("data/cosmic_sample.csv")  # replace with your reference
ref_coords = ref[["x","y","z"]].to_numpy()

df = pd.read_csv("derived/acsc_projected_cremona_final.csv")
src_coords = df[["x_prim","y_prim","z_prim"]].to_numpy()

aligner = QuantileAligner()
aligner.fit(ref_coords, n_quantiles=200)
aligned = aligner.transform(src_coords)

df[["x_aligned","y_aligned","z_aligned"]] = aligned
df.to_csv("derived/acsc_projected_cremona_aligned.csv", index=False)
print("Wrote derived/acsc_projected_cremona_aligned.csv")
