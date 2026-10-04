# Save projected coordinates and a compact manifest for downstream TDA
proj_out = os.path.join(OUT_DIR, "acsc_projected_primary_aligned.csv")
rec_df.to_csv(proj_out, index=False)
print("Saved projected coordinates to:", proj_out)

# Save a small manifest with counts and seed
manifest = {
    "rows": int(len(rec_df)),
    "seed": int(SEED),
    "Amax": Amax,
    "Nmax": Nmax,
    "V0": V0,
    "top_scale": TOP_SCALE
}
with open(os.path.join(OUT_DIR, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)
print("Saved manifest.")
