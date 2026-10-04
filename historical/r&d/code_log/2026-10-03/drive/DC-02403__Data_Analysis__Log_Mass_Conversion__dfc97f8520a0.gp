log_mass = [9.5, 10.0, 10.2, ...];
sfr = [0.1, 0.2, 0.3, ...];
         * z = [0.01, 0.02, 0.03, ...];
         * Start PARI/GP by typing gp in the terminal, then load the data with:
         * read("sfr_log_mass_z_data.txt")
         * This will define log_mass, sfr, and z as vectors in PARI/GP, ready for computations. If the file format differs, ensure it's valid PARI/GP syntax for vector assignments.
         2. Define Necessary Functions for Computations:
         * Define functions to compute the required statistics, leveraging PARI/GP's vector operations for precision:
         * Compute K_{\text{theory}}:
compute_K_theory(log_mass) = {
  M = vector(#log_mass, i, 10^log_mass[i]);
  M_sorted = vecsort(M);
  n = #M;
  if (n % 2 == 0,
    M0 = (M_sorted[n/2] + M_sorted[n/2 + 1]) / 2,
    M0 = M_sorted[(n+1)/2]
