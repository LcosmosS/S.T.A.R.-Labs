t_H = 1.44e10; Omega_cosmo = 1.38e10; Omega_tilde = Omega_cosmo / t_H;
print("Omega_tilde = ", Omega_tilde);


/* Embedded 9-galaxy SDSS DR17 data */
log_mass = [10.29471, 11.36537, 10.56586, 9.363875, 11.16167, 11.16527, 9.958716, 10.3831, 9.767632];
z = [0.02122228, 0.02037833, 0.06465632, 0.05265425, 0.2138606, 0.1212705, 0.05598059, 0.09708638, 0.06477907];
N = length(log_mass); print("Number of galaxies N = ", N);
M = vector(N, i, 10^log_mass[i]);


/* Custom median function */
my_median(v) = { my(sorted = vecsort(v)); my(len = length(sorted)); if(len % 2 == 0, (sorted[len/2] + sorted[len/2 + 1]) / 2, sorted[(len+1)/2]); };
M_0 = my_median(M); print("Reference mass M_0 = ", M_0);


/* Cosmological invariants */
Reg_cosmo = sum(i=1, N, M[i] / M_0) / N; print("Reg_cosmo = ", Reg_cosmo);
prod_c_p_cosmo = N; Sha_cosmo = 0.315; T_cosmo = 17;
print("T_cosmo = ", T_cosmo);


/* L-function definition */
L_cosmo(s) = sum(i=1, N, (M_0 / M[i])^s) / N;
unscaled_left = L_cosmo(1); print("Unscaled L_cosmo(1) = ", unscaled_left);


/* Compute K */
right_side = (Omega_tilde * Reg_cosmo * N * Sha_cosmo) / T_cosmo^2;
print("Right side = ", right_side);
K = right_side / unscaled_left; print("Normalization constant K = ", K);


/* Check if analogy holds within 10% tolerance */
tolerance = 0.1;
left_side = unscaled_left * K;
if(abs(left_side - right_side) < tolerance * right_side, print("Cosmological BSD analogue holds within 10%"), print("Cosmological BSD analogue fails: Left side != Right side"));


/* Stability check with subsample (first 5 galaxies) */
N_sub = 5; M_sub = vector(N_sub, i, M[i]);
M_0_sub = my_median(M_sub); Reg_cosmo_sub = sum(i=1, N_sub, M_sub[i] / M_0_sub) / N_sub;
L_cosmo_sub(s) = sum(i=1, N_sub, (M_0_sub / M_sub[i])^s) / N_sub;
unscaled_left_sub = L_cosmo_sub(1);
right_side_sub = (Omega_tilde * Reg_cosmo_sub * N_sub * Sha_cosmo) / T_cosmo^2;
K_sub = right_side_sub / unscaled_left_sub; print("Subsample K_sub (N_sub = ", N_sub, ") = ", K_sub);
if(abs(K_sub - K) / K < tolerance, print("K is stable within 10% for subsample"), print("K is unstable: >10% variation in subsample"));
