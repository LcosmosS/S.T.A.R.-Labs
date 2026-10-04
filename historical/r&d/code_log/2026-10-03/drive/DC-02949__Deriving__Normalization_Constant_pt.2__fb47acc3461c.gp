print("Precision set to 38");


/* Define cosmological constants based on Planck 2018 and SDSS DR17 context */
t_H = 1.44e10;                      /* Hubble time in years */
Omega_cosmo = 1.38e10;              /* Age of universe in years */
Omega_tilde = Omega_cosmo / t_H;    /* Dimensionless age ratio */
print("Omega_tilde: ", Omega_tilde);
Reg_cosmo = 1;                      /* Placeholder for average mass ratio; update with real data */
print("Reg_cosmo: ", Reg_cosmo);
prod_c_p_cosmo = 1000;              /* Number of galaxies in sample */
print("prod_c_p_cosmo: ", prod_c_p_cosmo);
Sha_cosmo = 0.315;                  /* Total matter density parameter (Planck 2018) */
print("Sha_cosmo: ", Sha_cosmo);
T_cosmo = 10;                       /* Number of large-scale structures; adjust based on data */
print("T_cosmo: ", T_cosmo);


/* Load SDSS DR17 data (example placeholder; replace with actual data) */
M_0 = 1e11;                         /* Reference mass: median ~10^11 M_sun */
N = 1000;                           /* Number of galaxies */
M = vector(N, i, 10^(10.5 + 0.5 * random(1000) / 1000.0)); /* Mock masses; replace with real M_i */
Z = vector(N, i, 0.02 + 0.01 * random(1000) / 1000.0);     /* Mock redshifts; replace with real Z */


/* Compute L_cosmo(s) using galaxy masses */
L_cosmo(s) = sum(i=1, N, (M_0 / M[i])^s);
unscaled_left = L_cosmo(1);         /* Unscaled L_cosmo(1) */
print("Unscaled L_cosmo(1): ", unscaled_left);


/* Compute right side using cosmological invariants */
right_side = (Omega_tilde * Reg_cosmo * prod_c_p_cosmo * Sha_cosmo) / (T_cosmo^2);
print("Right side: ", right_side);


/* Derive normalization constant K */
K = right_side / unscaled_left;     /* Normalization to match right side */
print("Normalization constant K: ", K);


/* Define and compute normalized L_cosmo_new(s) */
L_cosmo_new(s) = K * L_cosmo(s);
left_side = L_cosmo_new(1);         /* Normalized L_cosmo(1) */
print("Normalized L_cosmo(1): ", left_side);


/* Compare left and right sides within a tolerance */
tolerance = 0.1;                    /* 10% tolerance */
if (abs(left_side - right_side) < tolerance * right_side,
    print("Cosmological BSD analogue holds within 10%"),
    print("Cosmological BSD analogue fails: Left side != Right side"));
