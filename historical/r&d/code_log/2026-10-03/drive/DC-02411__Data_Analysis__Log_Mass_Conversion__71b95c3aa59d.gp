for(k=1, #z_bins - 1,
  z_min = z_bins[k];
  z_max = z_bins[k+1];
  indices = select(i -> z[i] >= z_min && z[i] < z_max && z[i] != -9999, Vecsmall(1,#z));
  if (#indices == 0, next);
  valid_indices = select(i -> log_mass[i] != -9999 && sfr[i] != -9999, indices);
  if (#valid_indices == 0, next);
  sfr_subset = vector(#valid_indices, j, sfr[valid_indices[j]]);
  median_sfr = compute_median(sfr_subset);
  high_sfr_indices = select(i -> sfr[i] > median_sfr, valid_indices);
  low_sfr_indices = select(i -> sfr[i] <= median_sfr, valid_indices);
  log_mass_high_sfr = vector(#high_sfr_indices, j, log_mass[high_sfr_indices[j]]);
  log_mass_low_sfr = vector(#low_sfr_indices, j, log_mass[low_sfr_indices[j]]);
  K_high = compute_K_theory(log_mass_high_sfr);
  skew_high = compute_skewness(log_mass_high_sfr);
  K_low = compute_K_theory(log_mass_low_sfr);
  skew_low = compute_skewness(log_mass_low_sfr);
  print("z: ", z_min, " to ", z_max);
  print("high_sfr: K_theory = ", K_high, ", skewness = ", skew_high);
  print("low_sfr: K_theory = ", K_low, ", skewness = ", skew_low);
         * );
         * Enter this loop, pressing Enter after each line, and PARI/GP will execute, printing results for each subgroup, allowing the user to identify conditions where the theory fits better, filtering out missing values for accuracy.
         4. Interpret the Results and Refine Theory:
         * After running, review the printed outputs for each z bin and sfr group, looking for combinations where K_{\text{theory}} is closer to 1 and skewness is closer to 0, indicating better fit to log-normal assumptions. For example, if high_sfr at z: 0.05 to 0.1 shows K_theory ≈ 0.9 and skewness ≈ -0.1, it suggests star-forming galaxies at that redshift fit better.
         * Compare with simulated data, where K_{\text{theory}} \approx 1.077 and skewness ≈ 0.0088, to assess how well real data aligns under different conditions, identifying trends like high_sfr galaxies at lower z ranges showing better fits, potentially linking to star-forming galaxy properties, or low_sfr galaxies (quiescent) deviating more, suggesting different mass distribution behaviors, which could guide theoretical adjustments.
         5. Optional: Compute for Entire Dataset or Other Groupings:
         * To compute for the entire dataset, first filter valid data:
valid_indices_all = select(i -> log_mass[i] != -9999 && sfr[i] != -9999 && z[i] != -9999, Vecsmall(1,#log_mass));
log_mass_all = vector(#valid_indices_all, j, log_mass[valid_indices_all[j]]);
K_all = compute_K_theory(log_mass_all);
skew_all = compute_skewness(log_mass_all);
         * print("All data: K_theory = ", K_all, ", skewness = ", skew_all);
         * This might give values similar to previous computations, like K_theory = 0.0095 and skewness ≈ -1.68, providing a baseline. The user can adjust binning or grouping strategies, such as using fixed sfr bins instead of median split, to explore alternative conditions, by modifying the loop to use predefined sfr thresholds.
