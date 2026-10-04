print("Precision set to 38");


/* Define cosmological constants based on Planck 2018 */
t_H = 1.44e10;                      /* Hubble time in years */
Omega_cosmo = 1.38e10;              /* Age of universe in years */
Omega_tilde = Omega_cosmo / t_H;    /* Dimensionless age ratio */
print("Omega_tilde: ", Omega_tilde);


/* Embed real SDSS DR17 data directly from your sample */
log_mass = [10.29471, 11.36537, 10.56586, 9.363875, 11.16167, 11.16527, 9.958716, 10.3831, 9.767632]; /* log10(M/M_sun) */
z = [0.02122228, 0.02037833, 0.06465632, 0.05265425, 0.2138606, 0.1212705, 0.05598059, 0.09708638, 0.06477907]; /* Redshifts */
N = length(log_mass);               /* Number of galaxies */
print("Number of galaxies N: ", N);


/* Convert log_mass to actual masses in solar masses */
M = vector(N, i, 10^log_mass[i]);   /* M_i = 10^(log_mass_i) */


/* Define a custom median function since PARI/GP lacks a built-in */
my_median(v) = {
    my(sorted = vecsort(v));        /* Sort the vector */
    my(len = length(sorted));       /* Length of the vector */
    if(len % 2 == 0,               /* If even number of elements */
