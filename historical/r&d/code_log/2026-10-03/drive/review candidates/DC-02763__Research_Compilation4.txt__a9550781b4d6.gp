for(k=1, #z_bins - 1, {
  z_min = z_bins[k];
  z_max = z_bins[k + 1];
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
                                                5. });
