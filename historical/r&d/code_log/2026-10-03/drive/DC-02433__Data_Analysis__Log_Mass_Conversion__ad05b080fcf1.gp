for(k=1, #z_bins - 1,
  z_min = z_bins[k];
  z_max = z_bins[k+1];
  bin_indices = select(i -> z_filtered[i] >= z_min && z_filtered[i] < z_max, Vecsmall(1,#z_filtered));
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
         * Enter this loop, pressing Enter after each line, and PARI/GP will execute, printing results for each subgroup, allowing the user to identify conditions where the theory fits better, with missing values already handled.
         5. Analyze the Results and Refine Theory:
         * After running, review the printed outputs for each z bin and sfr group, looking for combinations where K_{\text{theory}} is closer to 1 and skewness is closer to 0, indicating better fit to log-normal assumptions. For example, if high_sfr at z: 0.05 to 0.1 shows K_theory ≈ 0.9 and skewness ≈ -0.1, it suggests star-forming galaxies at that redshift fit better.
         * Compare with simulated data, where K_{\text{theory}} \approx 1.077 and skewness ≈ 0.0088, to assess how well real data aligns under different conditions, identifying trends like high_sfr galaxies at lower z ranges showing better fits, potentially linking to star-forming galaxy properties, or low_sfr galaxies (quiescent) deviating more, suggesting different mass distribution behaviors, which could guide theoretical adjustments.
