ra_bin4 = ra[group1_indices][bin4_mask]
dec_bin4 = dec[group1_indices][bin4_mask]
print(f"Group 1, Bin 4: ra range = {np.min(ra_bin4):.4f} to {np.max(ra_bin4):.4f}")
      * print(f"Group 1, Bin 4: dec range = {np.min(dec_bin4):.4f} to {np.max(dec_bin4):.4f}")
      * Optionally, plot ra vs. dec to visualize clustering.
