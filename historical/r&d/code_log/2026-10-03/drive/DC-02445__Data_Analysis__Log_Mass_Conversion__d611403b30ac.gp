print("Number of -9999 in log_mass:", sum(i=1, #log_mass, log_mass[i] == -9999));
print("Number of -9999 in sfr:", sum(i=1, #sfr, sfr[i] == -9999));
         * print("Number of -9999 in z:", sum(i=1, #z, z[i] == -9999));
         * The user already filtered with:
valid_indices = select(i -> log_mass[i] != -9999 && sfr[i] != -9999 && z[i] != -9999, vector(#log_mass, i, i));
log_mass_filtered = vector(#valid_indices, j, log_mass[valid_indices[j]]);
sfr_filtered = vector(#valid_indices, j, sfr[valid_indices[j]]);
         * z_filtered = vector(#valid_indices, j, z[valid_indices[j]]);
         * This is correct, ensuring data quality, aligning with previous practices of filtering missing values for statistical computations, as seen in IQR and KDE results.
         2. Compute Baseline Statistics for Entire Dataset:
         * Compute K_{\text{theory}} and skewness for the filtered dataset to have a baseline:
K_all = compute_K_theory(log_mass_filtered);
skew_all = compute_skewness(log_mass_filtered);
         * print("All data: K_theory = ", K_all, ", skewness = ", skew_all);
         * This provides a reference, likely showing K_{\text{theory}} far from 1, e.g., 0.0095, and skewness negative, e.g., -1.68, indicating the entire dataset doesn't fit, aligning with previous results, guiding subset analysis. The user's previous print showed "returnK_theory, returnskewness", which was due to incorrect function definitions, now fixed.
         3. Perform Subset Analysis by Redshift and SFR:
         * Set redshift bins for grouping, based on previous analyses:
         * z_bins = vector(9, i, [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4][i]);
         * For each z bin, select the subset, compute the median sfr, and split into high and low sfr groups, then compute statistics:
for(bin_index=1, #z_bins - 1,
  z_min = z_bins[bin_index];
  z_max = z_bins[bin_index + 1];
  bin_indices = select(i -> z_filtered[i] >= z_min && z_filtered[i] < z_max, vector(#z_filtered, i, i));
  if (#bin_indices == 0, next);
  sfr_bin = vector(#bin_indices, j, sfr_filtered[bin_indices[j]]);
  median_sfr = compute_median(sfr_bin);
  high_sfr_indices = select(i -> sfr_filtered[i] > median_sfr, bin_indices);
  low_sfr_indices = select(i -> sfr_filtered[i] <= median_sfr, bin_indices);
  log_mass_high_sfr = vector(#high_sfr_indices, j, log_mass_filtered[high_sfr_indices[j]]);
  log_mass_low_sfr = vector(#low_sfr_indices, j, log_mass_filtered[low_sfr_indices[j]]);
  K_high = compute_K_theory(log_mass_high_sfr);
  skew_high = compute_skewness(log_mass_high_sfr);
  K_low = compute_K_theory(log_mass_low_sfr);
  skew_low = compute_skewness(log_mass_low_sfr);
  print("z: ", z_min, " to ", z_max);
  print("high_sfr: K_theory = ", K_high, ", skewness = ", skew_high);
  print("low_sfr: K_theory = ", K_low, ", skewness = ", skew_low);
         * );
         * Enter this loop, pressing Enter after each line, and PARI/GP will execute, printing results for each subgroup, allowing the user to identify conditions where the theory fits better, using 'bin_index' to avoid variable conflicts.
         4. Analyze Results to Verify Theory:
         * Review the printed outputs for each z bin and sfr group, looking for combinations where K_{\text{theory}} is close to 1 (e.g., within 10% of 1, so 0.9 to 1.1) and skewness is near 0 (e.g., -0.1 to 0.1), indicating a good fit to log-normal assumptions. For example, if high_sfr at z: 0.05 to 0.1 shows K_theory ≈ 0.9 and skewness ≈ -0.1, it suggests star-forming galaxies at that redshift fit better.
         * Compare with simulated data, where K_{\text{theory}} \approx 1.077 and skewness ≈ 0.0088, to assess how well real data aligns under different conditions, identifying trends like high_sfr galaxies at lower z ranges showing better fits, potentially linking to star-forming galaxy properties, or low_sfr galaxies (quiescent) deviating more, suggesting different mass distribution behaviors, which could guide theoretical adjustments.
         * If no subgroups show K_{\text{theory}} close to 1, consider refining binning (e.g., smaller z bins) or exploring other groupings (e.g., by metallicity), or adjusting the theory to account for non-log-normal distributions.
