N = length(log_mass);               /* Number of galaxies */
print("Number of galaxies N: ", N);

/* Convert log_mass to actual masses in solar masses */
M = vector(N, i, 10^log_mass[i]);   /* M_i = 10^(log_mass_i) */

/* Define a custom median function since PARI/GP lacks a built-in */
my_median(v) = {
    my(sorted = vecsort(v));        /* Sort the vector */
    my(len = length(sorted));       /* Length of the vector */
    if(len % 2 == 0,               /* If even number of elements */