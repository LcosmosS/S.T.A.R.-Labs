t_H = 1.44e10; /* Hubble time in years */
Omega_cosmo = 1.38e10; /* Age of universe in years */
Omega_tilde = Omega_cosmo / t_H; /* Dimensionless age ratio */


/* The 'log_mass' vector must be populated with the 978 values from the 'logmass' column of the Stellar_Mass_Table.csv dataset. */
N = 978; /* Number of galaxies */


/* Convert log_mass to actual masses in solar masses */
M = vector(N, i, 10^log_mass[i]); /* M_i = 10^(log_mass_i) */


/* Define a custom median function since PARI/GP lacks a built-in */
my_median(v) = {
    my(sorted = vecsort(v)); /* Sort the vector */
    my(len = length(sorted)); /* Length of the vector */
    if(len % 2 == 0, /* If even number of elements */
