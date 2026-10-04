N_sub = 5; /* Subsample size */
log_mass_sub = vector(N_sub, i, log_mass[i]);
M_sub = vector(N_sub, i, 10^log_mass_sub[i]);
M_0_sub = 10^my_median(log_mass_sub);
Reg_cosmo_sub = sum(i=1, N_sub, M_sub[i] / M_0_sub) / N_sub;
prod_c_p_cosmo_sub = N_sub;
unscaled_left_sub = sum(i=1, N_sub, (M_0_sub / M_sub[i])) / N_sub;
right_side_sub = (Omega_tilde * Reg_cosmo_sub * prod_c_p_cosmo_sub * Sha_cosmo) /
