print("Precision set to 38");


/* Cosmological constants */
t_H = 1.44e10;              /* Hubble time in years */
Omega_cosmo = 1.38e10;      /* Cosmological time scale */
Omega_tilde = Omega_cosmo / t_H;
print("Omega_tilde: ", Omega_tilde);


/* Load data for first 1,000 galaxies (replace placeholders) */
log_mass = [/* INSERT_FIRST_1000_LOG_MASS_HERE */];  /* Filter out -9999 */
z = [/* INSERT_FIRST_1000_Z_HERE */];
N = length(log_mass);       /* Number of valid galaxies */
print("Number of galaxies N: ", N);


/* Convert log_mass to mass */
M = vector(N, i, 10^log_mass[i]);


/* Function to compute median */
my_median(v) = {
  my(sorted = vecsort(v));
  my(len = length(sorted));
  if(len % 2 == 0, (sorted[len/2] + sorted[len/2 + 1]) / 2, sorted[(len + 1)/2])
