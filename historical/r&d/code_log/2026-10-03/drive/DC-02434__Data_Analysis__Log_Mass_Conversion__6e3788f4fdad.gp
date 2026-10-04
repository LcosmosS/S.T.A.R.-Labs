print("Number of -9999 in log_mass:", sum(i=1, #log_mass, log_mass[i] == -9999));
print("Number of -9999 in sfr:", sum(i=1, #sfr, sfr[i] == -9999));
         * print("Number of -9999 in z:", sum(i=1, #z, z[i] == -9999));
         * If there are -9999 values, filter them out for analysis:
valid_indices = select(i -> log_mass[i] != -9999 && sfr[i] != -9999 && z[i] != -9999, Vecsmall(1,#log_mass));
log_mass_filtered = vector(#valid_indices, j, log_mass[valid_indices[j]]);
sfr_filtered = vector(#valid_indices, j, sfr[valid_indices[j]]);
         * z_filtered = vector(#valid_indices, j, z[valid_indices[j]]);
         * Use log_mass_filtered, sfr_filtered, z_filtered for further analysis, aligning with previous practices of filtering missing values for statistical computations.
         4. Define Functions for Statistical Computations:
         * Define the function to compute K_{\text{theory}}, expected near 1 for log-normal distributions:
compute_K_theory(log_mass) = {
  M = vector(#log_mass, i, 10^log_mass[i]);
  M_sorted = vecsort(M);
  n = #M;
  if (n % 2 == 0,
    M0 = (M_sorted[n/2] + M_sorted[n/2 + 1]) / 2,
    M0 = M_sorted[(n+1)/2]
