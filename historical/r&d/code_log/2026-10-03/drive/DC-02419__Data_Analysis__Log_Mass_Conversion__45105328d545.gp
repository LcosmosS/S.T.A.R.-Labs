log_mass = vector(n, i, all_values[3*i - 2]);
sfr = vector(n, i, all_values[3*i - 1]);
         * z = vector(n, i, all_values[3*i]);
         * This assumes the order is log_mass, sfr, z, repeating, which fits the output starting with -9999.0, then -0.677846, then -0.7394319, etc. Verify the first few values with print(log_mass[1], sfr[1], z[1]); to ensure, expecting something like log_mass ≈ -9999.0, sfr ≈ -0.677846, z ≈ -0.7394319, but z should be positive; wait, let's check:
         * Given previous data, z is typically positive, so perhaps the order is different. Wait, in the output, it's a long list, and the first value -9999.0 might be log_mass, then -0.677846 might be sfr, then -0.7394319 might be z, but z negative is unusual. Let's assume the order is correct based on previous, and proceed, verifying later.
         3. Filter Out Missing Values (-9999.0):
         * Since -9999.0 indicates missing data, filter to keep only valid entries:
         * valid_indices = select(i -> log_mass[i] != -9999.0 && sfr[i] != -9999.0 && z[i] != -9999.0, Vecsmall(1,n));
         * Create filtered vectors for analysis:
log_mass_filtered = vector(#valid_indices, j, log_mass[valid_indices[j]]);
sfr_filtered = vector(#valid_indices, j, sfr[valid_indices[j]]);
         * z_filtered = vector(#valid_indices, j, z[valid_indices[j]]);
         * This ensures only complete data points are used, aligning with previous practices of filtering missing values for statistical computations, as seen in IQR and KDE results.
         4. Define Functions for Statistical Computations:
         * Define the function to compute K_{\text{theory}}, expected near 1 for log-normal distributions:
compute_K_theory(log_mass) = {
  M = vector(#log_mass, i, 10^log_mass[i]);
  M_sorted = vecsort(M);
  n = #M;
  if (n % 2 == 0,
    M0 = (M_sorted[n/2] + M_sorted[n/2 + 1]) / 2,
    M0 = M_sorted[(n+1)/2]
