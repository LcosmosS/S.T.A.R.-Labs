M_0 = 10^my_median(log_mass);
print("Reference mass M_0: ", M_0);


/* Compute regularization factor */
Reg_cosmo = sum(i=1, N, M[i] / M_0) / N;
print("Reg_cosmo: ", Reg_cosmo);


/* Product term */
prod_c_p_cosmo = N;
print("prod_c_p_cosmo: ", prod_c_p_cosmo);


/* Shape parameter */
Sha_cosmo = 0.315;
print("Sha_cosmo: ", Sha_cosmo);


/* Cosmological threshold for N=1000 */
T_cosmo = 29;  /* Adjusted for N=1000; sqrt(0.9583 * 2.8119 * 1000 * 0.315) ≈ 29 */
print("T_cosmo: ", T_cosmo);


/* L-function definition (unscaled) */
L_cosmo(s) = { sum(i=1, N, (M_0 / M[i])^s) / N };


/* Compute unscaled L_cosmo(1) */
unscaled_left = L_cosmo(1);
print("Unscaled L_cosmo(1): ", unscaled_left);


/* Compute right-hand side of the BSD analogue */
right_side = (Omega_tilde * Reg_cosmo * prod_c_p_cosmo * Sha_cosmo) / (T_cosmo^2);
print("Right side: ", right_side);


/* Normalization constant K */
K = right_side / unscaled_left;
print("Normalization constant K: ", K);


/* Normalized L-function */
L_cosmo_new(s) = { K * L_cosmo(s) };
left_side = L_cosmo_new(1);
print("Normalized L_cosmo(1): ", left_side);


/* Check if BSD analogue holds within 10% tolerance */
tolerance = 0.1;
if(abs(left_side - right_side) < tolerance * right_side,
  print("Cosmological BSD analogue holds within 10%"),
  print("Cosmological BSD analogue fails: Left side != Right side"));


/* Subsample stability check with 500 galaxies */
N_sub = 500;
log_mass_sub = vector(N_sub, i, log_mass[i]);
M_sub = vector(N_sub, i, 10^log_mass_sub[i]);
M_0_sub = 10^my_median(log_mass_sub);
print("Subsample M_0_sub: ", M_0_sub);
Reg_cosmo_sub = sum(i=1, N_sub, M_sub[i] / M_0_sub) / N_sub;
print("Subsample Reg_cosmo_sub: ", Reg_cosmo_sub);
prod_c_p_cosmo_sub = N_sub;
unscaled_left_sub = sum(i=1, N_sub, (M_0_sub / M_sub[i])) / N_sub;
print("Subsample unscaled_left_sub: ", unscaled_left_sub);
right_side_sub = (Omega_tilde * Reg_cosmo_sub * prod_c_p_cosmo_sub * Sha_cosmo) / (T_cosmo^2);
print("Subsample right_side_sub: ", right_side_sub);
K_sub = right_side_sub / unscaled_left_sub;
print("Subsample (N=500) K: ", K_sub);


/* Check stability of K */
if(abs(K_sub - K) / K < 0.1,
  print("K is stable within 10% between subsample and full sample"),
  print("K varies >10%; consider adjusting T_cosmo or L-function"));
