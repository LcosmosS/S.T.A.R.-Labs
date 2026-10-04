rec_df[["x_ptd","y_ptd","z_ptd"]] = coords_ptd
rec_df[["x_mcj","y_mcj","z_mcj"]] = coords_mcj
rec_df.to_csv("derived/acsc_projected_cremona_with_alt.csv", index=False)
print("Wrote derived/acsc_projected_cremona_with_alt.csv")
display(rec_df.head(int(3)))
