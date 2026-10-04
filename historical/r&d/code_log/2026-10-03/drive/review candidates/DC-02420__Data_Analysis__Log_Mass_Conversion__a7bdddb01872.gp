for(k=1, #z_bins - 1,
  z_min = z_bins[k];
  z_max = z_bins[k+1];
  indices = select(i -> z[i] >= z_min && z[i] < z_max, Vecsmall(1,#z));
  if (#indices == 0, next);
  sfr_subset = vector(#indices, j, sfr[indices[j]]);
  median_sfr = compute_median(sfr_subset);
  high_sfr_indices = select(i -> sfr[i] > median_sfr, indices);
  low_sfr_indices = select(i -> sfr[i] <= median_sfr, indices);
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
