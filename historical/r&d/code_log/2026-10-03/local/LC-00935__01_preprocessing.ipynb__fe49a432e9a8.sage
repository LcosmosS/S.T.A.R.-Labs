from acsc.quantile import QuantileAligner
import numpy as np, pandas as pd

# build reference cloud from your dataset if you don't have external reference
df = pd.read_csv("derived/acsc_projected_cremona_with_alt.csv")
ref_coords = df[["x_ptd","y_ptd","z_ptd"]].sample(min(10000, len(df)), random_state=int(42)).to_numpy()

aligner = QuantileAligner()
aligner.fit(ref_coords, n_quantiles=200)
aligned = aligner.transform(df[["x_ptd","y_ptd","z_ptd"]].to_numpy())
df[["x_ptd_al","y_ptd_al","z_ptd_al"]] = aligned
df.to_csv("derived/acsc_projected_cremona_ptd_aligned.csv", index=False)
print("Wrote derived/acsc_projected_cremona_ptd_aligned.csv")
