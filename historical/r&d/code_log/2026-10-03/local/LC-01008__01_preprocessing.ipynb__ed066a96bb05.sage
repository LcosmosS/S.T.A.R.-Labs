import numpy as np
rec_df[["x_prim","y_prim","z_prim"]] = coords_primary
rec_df[["x_ptd","y_ptd","z_ptd"]] = coords_ptd
rec_df[["x_mcj","y_mcj","z_mcj"]] = coords_mcj

# quick sanity stats
for name in ["x_prim","y_prim","z_prim"]:
    a = rec_df[name].to_numpy()
    print(f"{name}: min {a.min():.6g}, max {a.max():.6g}, mean {a.mean():.6g}, std {a.std():.6g}")

rec_df.to_csv("derived/acsc_projected_cremona_realproj.csv", index=False)
print("Wrote derived/acsc_projected_cremona_realproj.csv")
