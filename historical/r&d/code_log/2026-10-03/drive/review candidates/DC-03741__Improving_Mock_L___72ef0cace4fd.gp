T_cmb = 2.7255e6; /* μK */
C_l = vector(2500, n, if(n>=2, 2500 / (n * (n + 1)), 0)); /* Replace with actual Planck data */
K = 1e10; /* Scaling factor */
L_cosmo(s) = K * sum(n=2, 2500, (C_l[n] / T_cmb^2) / n^s);
print("L_cosmo defined with normalized CMB data and scaling");


/* Cosmological constants */
t_H = 1.44e10;
Omega_cosmo = 1.38e10; /* Universe age in years */
Omega_tilde = Omega_cosmo / t_H;
Reg_cosmo = 9.3e10 / 5.38e7; /* Consider alternative definition */
prod_c_p_cosmo = 50;
Sha_cosmo = 0.27;
T_cosmo = 5;


/* Compute sides */
left_side = L_cosmo(1);
right_side = (Omega_tilde * Reg_cosmo * prod_c_p_cosmo * Sha_cosmo) / (T_cosmo^2);
print("Left side: ", left_side);
print("Right side: ", right_side);


/* Compare */
tolerance = 0.1;
if (abs(left_side - right_side) < tolerance * right_side,
    print("Analogy holds within 10%"),
    print("Analogy fails"));
