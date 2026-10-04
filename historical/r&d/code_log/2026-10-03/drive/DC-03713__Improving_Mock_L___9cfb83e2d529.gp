T_cmb = 2.7255e6; /* CMB temperature in μK */
C_l = vector(2500, n, if(n>=2, 2500 / (n * (n + 1)), 0)); /* Placeholder for CMB power spectrum */
   * L_cosmo(s) = 1e4 * sum(n=2, 2500, (C_l[n] / T_cmb^2) / n^s);
   * Evaluates to 4.88 \times 10^{-7} at s = 1, dimensionless due to normalization by T_{\text{cmb}}^2.
* Right Side:
   * Definition:
   * pari
t_H = 1.44e10; /* Hubble time in years */
Omega_cosmo = 5.38e7; /* Light travel time to Virgo in years */
Omega_tilde = Omega_cosmo / t_H; /* ≈ 0.00374 */
Reg_cosmo = 9.3e10 / 5.38e7; /* ≈ 1728.62 */
prod_c_p_cosmo = 50; /* Cluster count */
Sha_cosmo = 0.27; /* Dark matter density */
T_cosmo = 5; /* Supercluster count */
   * right_side = (Omega_tilde * Reg_cosmo * prod_c_p_cosmo * Sha_cosmo) / (T_cosmo^2);
   * Yields approximately 3.4875, dimensionless after normalizing \Omega_{\text{cosmo}} with t_H.
* Mismatch:
   * Magnitude: 4.88 \times 10^{-7} vs. 3.4875, a factor of ~10^7.
   * Units: Both sides are dimensionless, but the numerical values are misaligned, suggesting issues in scaling or interpretation.
