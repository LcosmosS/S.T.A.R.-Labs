t_H = 1.44e10;                      /* Hubble time in years */
Omega_cosmo = 5.38e7;               /* Light travel time to Virgo in years */
Omega_tilde = Omega_cosmo / t_H;    /* Dimensionless Omega */
Reg_cosmo = 9.3e10 / 5.38e7;        /* Size ratio: observable universe / Virgo distance */
prod_c_p_cosmo = 50;                /* Number of major galaxy clusters */
Sha_cosmo = 0.27;                   /* Dark matter density parameter */
T_cosmo = 5;                        /* Number of superclusters */


/* Define mock CMB data based on a simplified approximation of Planck TT spectrum */
T_cmb = 2.7255e6;                   /* CMB temperature in μK */
/* Use a piecewise function for C_l from l=2 to l=2508 */
C_l = vector(2509, n, if(n<2, 0, if(n<=29, (1000 * 2 * Pi) / (n * (n+1)), \
