print("Precision set to 38");


/* Cosmological constants */
t_H = 1.44e10;
Omega_cosmo = 1.38e10;
Omega_tilde = Omega_cosmo / t_H;
print("Omega_tilde: ", Omega_tilde);


/* Load exactly 1,000 galaxies (replace placeholders) */
log_mass = [/* INSERT_FIRST_1000_VALID_LOG_MASS_HERE */];
z = [/* INSERT_FIRST_1000_VALID_Z_HERE */];
N = 1000;  /* Fixed to 1,000 galaxies */
print("Number of galaxies N: ", N);


/* Convert log_mass to mass */
M = vector(N, i, 10^log_mass[i]);


/* Function to compute median */
my_median(v) = {
  my(sorted = vecsort(v));
  my(len = length(sorted));
  if(len % 2 == 0, (sorted[len/2] + sorted[len/2 + 1]) / 2, sorted[(len + 1)/2])
