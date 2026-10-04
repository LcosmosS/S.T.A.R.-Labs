print("Precision set to 38");


/* Define cosmological constants */
t_H = 1.44e10;                      /* Hubble time in years */
Omega_cosmo = 5.38e7;               /* Light travel time to Virgo in years */
Omega_tilde = Omega_cosmo / t_H;    /* Dimensionless Omega */
print("Omega_tilde: ", Omega_tilde);
Reg_cosmo = 9.3e10 / 5.38e7;        /* Size ratio: observable universe / Virgo distance */
print("Reg_cosmo: ", Reg_cosmo);
prod_c_p_cosmo = 50;                /* Number of major galaxy clusters */
print("prod_c_p_cosmo: ", prod_c_p_cosmo);
Sha_cosmo = 0.27;                   /* Dark matter density parameter */
print("Sha_cosmo: ", Sha_cosmo);
T_cosmo = 5;                        /* Number of superclusters */
print("T_cosmo: ", T_cosmo);


/* Define mock CMB data (simplified approximation of Planck TT spectrum) */
T_cmb = 2.7255e6;                   /* CMB temperature in μK */
C_l = vector(2509, n, if(n<2, 0, if(n<=29, (1000 * 2 * Pi) / (n * (n+1)), 
