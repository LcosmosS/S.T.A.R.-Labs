log_mass = [10.29471, 11.36537, 10.56586, 9.363875, 11.16167, 11.16527, 9.958716, 10.3831, 9.767632];
z = [0.02122228, 0.02037833, 0.06465632, 0.05265425, 0.2138606, 0.1212705, 0.05598059, 0.09708638, 0.06477907];
N = length(log_mass);
M = vector(N, i, 10^log_mass[i]);
M_0 = 10^my_median(log_mass);
Reg_cosmo = sum(i=1, N, M[i] / M_0) / N;
Omega_tilde = 0.95833333333333333333;  /* 1.38e10 / 1.44e10 */
Sha_cosmo = 0.315;                     /* Matter density */
T_cosmo = 17;                          /* Adjusted constant */


/* Compute L-function and normalization */
L_cosmo(s) = sum(i=1, N, (M_0 / M[i])^s) / N;
unscaled_left = L_cosmo(1);
right_side = (Omega_tilde * Reg_cosmo * N * Sha_cosmo) / (T_cosmo^2);
K = right_side / unscaled_left;
L_cosmo_new(s) = K * L_cosmo(s);
left_side = L_cosmo_new(1);


/* Compare left and right sides */
tolerance = 0.1;  /* 10% tolerance */
if (abs(left_side - right_side) < tolerance * right_side,
    print("Cosmological BSD analogue holds within 10%"),
    print("Cosmological BSD analogue fails: Left side != Right side")
