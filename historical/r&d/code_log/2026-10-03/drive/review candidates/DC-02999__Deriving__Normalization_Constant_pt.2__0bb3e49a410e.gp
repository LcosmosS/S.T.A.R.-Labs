M = read("masses.txt");
Z = read("redshifts.txt");
N = length(M);
print("Number of galaxies: ", N);


/* Compute median mass */
log_mass_vector = vector(N, i, log(M[i]) / log(10)); /* Convert back to log10 */
M_0 = 10^median(log_mass_vector);                    /* Median mass */
print("Median mass M_0: ", M_0);
