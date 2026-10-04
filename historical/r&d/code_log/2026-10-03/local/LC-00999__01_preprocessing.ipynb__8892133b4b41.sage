# Load cosmic point cloud (assumed to be Nx3 comoving coordinates)
cosmic = pd.read_csv(COSMIC_FILE)
# Ensure shape (n,3)
cosmic_coords = cosmic.iloc[:, :3].to_numpy()

# Fit quantile aligner on cosmic coords and transform primary arithmetic cloud
aligner = QuantileAligner()
aligner.fit(cosmic_coords, n_quantiles=N_QUANTILES)

# Transform the primary projection
arith_primary_coords = rec_df[["x_prim", "y_prim", "z_prim"]].to_numpy()
arith_aligned = aligner.transform(arith_primary_coords)

# Save aligned coords into DataFrame
rec_df[["x_aligned", "y_aligned", "z_aligned"]] = arith_aligned
print("Aligned coords shape:", arith_aligned.shape)
