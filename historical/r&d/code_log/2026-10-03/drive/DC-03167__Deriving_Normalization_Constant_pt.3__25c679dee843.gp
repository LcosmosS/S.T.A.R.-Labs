N_sub = 500;
log_mass_sub = vector(N_sub, i, log_mass[i]);
   * M_sub = vector(N_sub, i, 10^log_mass_sub[i]);
   * Recompute K_{\text{sub}} for the first 500 galaxies.
   * Compare:
   * \left| \frac{K_{\text{sub}} - K}{K} \right| < 0.1
   * If ( K ) varies >10%, adjust T_{\text{cosmo}} (e.g., try 28 or 30) or revisit L_{\text{cosmo}}(s) (e.g., weight by redshift).
