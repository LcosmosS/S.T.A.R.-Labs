prod_c_p_cosmo = 50;                /* Number of major galaxy clusters */
Sha_cosmo = 0.27;                   /* Dark matter density parameter */
T_cosmo = 5;                        /* Number of superclusters */

/* Define mock CMB data based on a simplified approximation of Planck TT spectrum */
T_cmb = 2.7255e6;                   /* CMB temperature in μK */
/* Use a piecewise function for C_l from l=2 to l=2508 */
C_l = vector(2509, n, if(n<2, 0, if(n<=29, (1000 * 2 * Pi) / (n * (n+1)), \
