n = #log_mass;
indices = vector(n, i, i);
valid_indices = select(i -> log_mass[i] != -9999 && sfr[i] != -9999 && z[i] != -9999, indices);
log_mass_filtered = vector(#valid_indices, j, log_mass[valid_indices[j]]);
sfr_filtered = vector(#valid_indices, j, sfr[valid_indices[j]]);
         * z_filtered = vector(#valid_indices, j, z[valid_indices[j]]);
         * This filters out rows with -9999 in any vector, ensuring only complete data points are used, aligning with previous practices.
         2. Define Functions for Statistical Computations:
         * Define the function to compute K_{\text{theory}}, expected near 1 for log-normal distributions:
compute_K_theory(log_mass) = {
  M = vector(#log_mass, i, 10^log_mass[i]);
  M_sorted = vecsort(M);
  n = #M;
  if (n % 2 == 0,
    M0 = (M_sorted[n/2] + M_sorted[n/2 + 1]) / 2,
    M0 = M_sorted[(n+1)/2]
