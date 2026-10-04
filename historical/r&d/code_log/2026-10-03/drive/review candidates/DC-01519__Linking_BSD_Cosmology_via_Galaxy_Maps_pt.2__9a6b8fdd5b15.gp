t_H = 1.44e10;  \\ Hubble time, likely in seconds
Omega_cosmo = 1.38e10;  \\ Cosmological density parameter
Omega_tilde = Omega_cosmo / t_H;
print("Omega_tilde: ", Omega_tilde);


\\ Use the log_mass vector already defined in data.gp
N = length(log_mass);
M = vector(N, i, 10^log_mass[i]);  \\ Convert log masses to linear masses
M_0 = median(M);  \\ Find the median mass
print("Reference mass M_0: ", M_0);


\\ Set additional parameters for the theory
Reg_cosmo = 2.8;  \\ Estimated from prior subsets
prod_c_p_cosmo = N;  \\ Number of galaxies, 1000 here
Sha_cosmo = 0.315;  \\ Another cosmological parameter
T_cosmo = sqrt(0.9583 * Reg_cosmo * prod_c_p_cosmo * Sha_cosmo);  \\ Compute T_cosmo
print("T_cosmo: ", T_cosmo);


\\ Calculate the unscaled likelihood, average of M_0 divided by each mass
UnscaledL_cosmo = sum(i=1, N, M_0 / M[i]) / N;
print("Unscaled L_cosmo(1): ", UnscaledL_cosmo);


\\ Compute Rightside using the formula
Rightside = (Omega_tilde * Reg_cosmo * prod_c_p_cosmo * Sha_cosmo) / (T_cosmo^2);
print("Rightside: ", Rightside);


\\ Compute the normalization constant K
K = Rightside / UnscaledL_cosmo;
print("Normalization constant K: ", K);


\\ Check if K is within 10% of 1 to see if the theory holds
if(abs(K - 1) < 0.1, print("Cosmological BSD analogue holds within 10%"), print("Cosmological BSD analogue does not hold within 10%"));


\\ Subsample analysis for stability, first 500
N_sub1 = 500;
M_sub1 = vector(N_sub1, i, M[i]);
M_0_sub1 = median(M_sub1);
print("Subsample M_0_sub1: ", M_0_sub1);
subsample_unscaled_left_sub1 = sum(i=1, N_sub1, M_0_sub1 / M_sub1[i]) / N_sub1;
print("Subsample unscaled left sub1: ", subsample_unscaled_left_sub1);
subsample_right_side_sub1 = (Omega_tilde * Reg_cosmo * N_sub1 * Sha_cosmo) / (T_cosmo^2);
print("Subsample right side sub1: ", subsample_right_side_sub1);
subsample_K_sub1 = subsample_right_side_sub1 / subsample_unscaled_left_sub1;
print("Subsample (N=500) K_sub1: ", subsample_K_sub1);


\\ Subsample analysis for stability, next 500
N_sub2 = 500;
M_sub2 = vector(N_sub2, i, M[500+i]);
M_0_sub2 = median(M_sub2);
print("Subsample M_0_sub2: ", M_0_sub2);
subsample_unscaled_left_sub2 = sum(i=1, N_sub2, M_0_sub2 / M_sub2[i]) / N_sub2;
print("Subsample unscaled left sub2: ", subsample_unscaled_left_sub2);
subsample_right_side_sub2 = (Omega_tilde * Reg_cosmo * N_sub2 * Sha_cosmo) / (T_cosmo^2);
print("Subsample right side sub2: ", subsample_right_side_sub2);
subsample_K_sub2 = subsample_right_side_sub2 / subsample_unscaled_left_sub2;
print("Subsample (N=500) K_sub2: ", subsample_K_sub2);


\\ Check stability within 10% for both subgroups
print("K is stable within 10% for Subgroup1: ", abs(K - subsample_K_sub1)/abs(K) < 0.1);
print("K is stable within 10% for Subgroup2: ", abs(K - subsample_K_sub2)/abs(K) < 0.1);
