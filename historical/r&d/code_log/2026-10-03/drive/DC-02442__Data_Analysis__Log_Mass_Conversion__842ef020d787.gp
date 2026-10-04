n = #log_mass;
indices = vector(n, i, i);
         * valid_indices = select(i -> log_mass[i] != -9999 && sfr[i] != -9999 && z[i] != -9999, indices);
         * This is correct, creating a vector of indices and selecting valid ones, which worked as seen in subsequent commands.
         2. Type Errors in Loop and Select:
         * When defining the loop for(k=1, #z_bins - 1, ..., they got errors like "incorrect type in gtos [integer expected] (t_POL)", suggesting k was defined as a polynomial elsewhere. This is likely because PARI/GP variables can be redefined, and k might have been a polynomial from a previous session.
         * To fix, use a different variable name, like bin, and ensure no conflicts:
for(bin=1, #z_bins - 1,
  z_min = z_bins[bin];
  z_max = z_bins[bin+1];
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
         * Use vector(#z_filtered, i, i) instead of Vecsmall for select, as PARI/GP might not accept t_VECSMALL in some contexts, ensuring type compatibility.
         3. Function Definition Issues:
         * The user defined compute_K_theory, compute_skewness, and compute_median, but when printing, got "All data: K_theory = returnK_theory, skewness = returnskewness", suggesting the functions didn't return values properly. In PARI/GP, functions should end with the expression to return, without "return" keyword:
         * Change:
         * compute_K_theory(log_mass) = { ... return K_theory; }
         * to:
         * compute_K_theory(log_mass) = { ... K_theory }
         * Similarly for compute_skewness and compute_median, ensuring the last line is the value, like:
compute_skewness(log_mass) = { ... skewness }
         * compute_median(v) = { ... if (n % 2 == 0, (v_sorted[n/2] + v_sorted[n/2 + 1]) / 2, v_sorted[(n+1)/2]) }
         * This fixes the function return issue, ensuring K_all and skew_all hold numerical values.
