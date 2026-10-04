# Convert DataFrame rows to dicts for projection functions
records_for_proj = rec_df.to_dict(orient="records")

# Primary projection (rank-normalized)
coords_primary = project_records(records_for_proj, method="primary", Amax=Amax, Nmax=Nmax, V0=V0)
print("Primary coords shape:", coords_primary.shape)

# Alternative projections
coords_ptd = project_records(records_for_proj, method="ptd")
coords_mcj = project_records(records_for_proj, method="mcj")

# Attach projected coords back to DataFrame (store as columns)
rec_df[["x_prim", "y_prim", "z_prim"]] = coords_primary
rec_df[["x_ptd", "y_ptd", "z_ptd"]] = coords_ptd
rec_df[["x_mcj", "y_mcj", "z_mcj"]] = coords_mcj

# Save a small sample for quick inspection
rec_df.sample(5)
