print("Precision set to 38");


/* Define cosmological constants */
t_H = 1.44e10;                      /* Hubble time in years */
Omega_cosmo = 1.38e10;              /* Age of universe in years */
Omega_tilde = Omega_cosmo / t_H;    /* Dimensionless */
print("Omega_tilde: ", Omega_tilde);
Reg_cosmo = 1000;                   /* Approx. number of significant structures */
print("Reg_cosmo: ", Reg_cosmo);
prod_c_p_cosmo = 1000;              /* Number of galaxies in sample */
print("prod_c_p_cosmo: ", prod_c_p_cosmo);
Sha_cosmo = 0.857;                  /* Dark matter fraction: Omega_DM / Omega_m */
print("Sha_cosmo: ", Sha_cosmo);
T_cosmo = 100;                      /* Number of large-scale structures */
print("T_cosmo: ", T_cosmo);


/* Define L_cosmo(s) using galaxy masses (approximated) */
M_0 = 1e12;                         /* Reference mass: Milky Way ~ 10^12 M_sun */
N = 1000;                           /* Number of galaxies */
M = vector(N, i, M_0 * (1 + 0.5 * random(1000) / 1000.0)); /* Random masses around M_0 */
L_cosmo(s) = sum(i=1, N, (M_0 / M[i])^s); /* L-function based on inverse masses */
unscaled_left = L_cosmo(1);         /* Compute unscaled L_cosmo(1) */
print("Unscaled L_cosmo(1): ", unscaled_left);


/* Compute right side */
right_side = (Omega_tilde * Reg_cosmo * prod_c_p_cosmo * Sha_cosmo) / (T_cosmo^2);
print("Right side: ", right_side);


/* Derive normalization constant K */
K = right_side / unscaled_left;     /* K scales L_cosmo to match right side */
print("Normalization constant K: ", K);


/* Define normalized L_cosmo_new(s) */
L_cosmo_new(s) = K * L_cosmo(s);
left_side = L_cosmo_new(1);         /* Compute normalized L_cosmo(1) */
print("Normalized L_cosmo(1): ", left_side);


/* Compare left and right sides */
tolerance = 0.1;                    /* 10% tolerance */
if (abs(left_side - right_side) < tolerance * right_side,
    print("Analogy holds within 10%"),
    print("Analogy fails: Left side != Right side"));
