t_H = 1.44e10;              /* Hubble time in years */
Omega_cosmo = 1.38e10;      /* Cosmological time scale */
Omega_tilde = Omega_cosmo / t_H;
print("Omega_tilde: ", Omega_tilde);


/* Load the filtered logmass and z vectors (insert your data here) */
log_mass = /* INSERT_LOG_MASS_HERE */;  /* e.g., [10.09385, 11.2518, ...] */
z = /* INSERT_Z_HERE */;                /* e.g., [0.1037164, 0.0766939, ...] */


/* Compute number of galaxies and convert logmass to mass */
N = length(log_mass);
print("Number of galaxies N: ", N);
M = vector(N, i, 10^log_mass[i]);  /* Convert logmass to stellar mass */


/* Custom median function since PARI/GP lacks a built-in median */
my_median(v) = {
  my(sorted = vecsort(v));
  my(len = length(sorted));
  if(len % 2 == 0, (sorted[len/2] + sorted[len/2 + 1]) / 2, sorted[(len + 1) / 2])
