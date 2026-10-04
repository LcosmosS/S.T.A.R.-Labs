M = read("masses.txt");  /* Vector of real masses */
Z = read("redshifts.txt"); /* Vector of real redshifts */
N = length(M);  /* Update number of galaxies */


/* Compute median mass for M_0 */
log_mass_vector = vector(N, i, log(M[i]) / log(10));  /* Convert to log10(M/M_sun) */
M_0 = 10^median(log_mass_vector);  /* Set M_0 to median mass */
