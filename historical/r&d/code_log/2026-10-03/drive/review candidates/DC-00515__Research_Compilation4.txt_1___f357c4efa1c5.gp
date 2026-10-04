print("Precision set to 38 decimal places");


/* Cosmological constants */
t_H = 1.44e10;           /* Hubble time in years */
Omega_cosmo = 1.38e10;   /* Cosmological time scale in years */
Omega_tilde = Omega_cosmo / t_H;
print("Omega_tilde: ", Omega_tilde);


/* Load exactly 1,000 galaxies */
log_mass = [/* INSERT_FIRST_1000_VALID_LOG_MASS_HERE */];
z = [/* INSERT_FIRST_1000_VALID_Z_HERE */];
N = 1000;  /* Fixed number of galaxies */
print("Number of galaxies N: ", N);


/* Convert log_mass to mass (in solar masses) */
M = vector(N, i, 10^log_mass[i]);


/* Function to compute median */
my_median(v) = {
  my(sorted = vecsort(v));
  my(len = length(sorted));
  if(len % 2 == 0, (sorted[len/2] + sorted[len/2 + 1]) / 2, sorted[(len + 1)/2])
