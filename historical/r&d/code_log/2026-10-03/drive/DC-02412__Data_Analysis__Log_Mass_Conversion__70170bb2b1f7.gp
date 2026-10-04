n = #data[1]/3;  // Assuming 3 values per galaxy, total length divisible by 3
log_mass = vector(n, i, data[1][3*i-2]);
sfr = vector(n, i, data[1][3*i-1]);
         * z = vector(n, i, data[1][3*i]);
         * This assumes the data is interleaved as [log_mass1, sfr1, z1, log_mass2, sfr2, z2, ...], which fits the output starting with -9999.0, -0.677846, -0.7394319, etc., suggesting the first is log_mass, second sfr, third z, and so on. Verify with print(log_mass[1], sfr[1], z[1]); to check, expecting something like log_mass ≈ 10.09385, sfr ≈ -9999.0, z ≈ 0.1037164 for the first line.
         2. Define Necessary Functions for Computations:
         * Define the function to compute K_{\text{theory}}, which calculates the normalization constant expected to be near 1 for log-normal distributions:
compute_K_theory(log_mass) = {
  M = vector(#log_mass, i, 10^log_mass[i]);
  M_sorted = vecsort(M);
  n = #M;
  if (n % 2 == 0,
    M0 = (M_sorted[n/2] + M_sorted[n/2 + 1]) / 2,
    M0 = M_sorted[(n+1)/2]
