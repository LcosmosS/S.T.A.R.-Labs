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
         * Use vector(#z_filtered, i, i) instead of Vecsmall for select, as PARI/GP might not accept t_VECSMALL in some contexts, ensuring type compatibility, which resolves errors like "incorrect type in select (t_POL)".
         3. Select Function and Comparison Errors:
         * The error ">=: forbidden comparison t_REAL , t_POL" suggests z_min or z_max was treated as a polynomial, likely due to variable conflicts. Ensure z_bins is a vector of real numbers, not a polynomial, by defining it as:
         * z_bins = vector(9, i, [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4][i]);
         * This ensures z_bins is a vector, and indexing with bin_index returns real numbers, fixing comparison errors.
