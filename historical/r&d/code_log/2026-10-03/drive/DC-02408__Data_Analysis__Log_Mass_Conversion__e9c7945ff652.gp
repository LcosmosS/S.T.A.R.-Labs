log_mass = vector(#data, i, data[i][1]);
sfr = vector(#data, i, data[i][2]);
         * z = vector(#data, i, data[i][3]);
         * This creates log_mass, sfr, and z as separate vectors, ready for analysis, handling any -9999 values as part of the data.
         2. Define Necessary Functions for Computations:
         * Define the function to compute K_{\text{theory}}, which calculates the normalization constant expected to be near 1 for log-normal distributions:
compute_K_theory(log_mass) = {
  M = vector(#log_mass, i, 10^log_mass[i]);
  M_sorted = vecsort(M);
  n = #M;
  if (n % 2 == 0,
    M0 = (M_sorted[n/2] + M_sorted[n/2 + 1]) / 2,
    M0 = M_sorted[(n+1)/2]
