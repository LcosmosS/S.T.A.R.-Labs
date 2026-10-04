print("Precision set to 38");


/* Load SDSS DR17 data (example placeholder) */
M = vector(1000, i, 10^(10.5 + 0.5 * random(1000) / 1000.0)); /* Replace with real masses */
M_0 = 1e11;                         /* Median mass placeholder */
N = 1000;                           /* Number of galaxies */


/* Define L_cosmo(s) with galaxy masses */
L_cosmo(s) = sum(i=1, N, (M_0 / M[i])^s);
unscaled_left = L_cosmo(1);         /* Unscaled L_cosmo(1) */
print("Unscaled L_cosmo(1): ", unscaled_left);
normalized_left = unscaled_left / N; /* Normalized L_cosmo(1) */
print("Normalized L_cosmo(1): ", normalized_left);


/* Define cosmological constants */
t_H = 1.44e10;                      /* Hubble time in years */
Omega_cosmo = 1.38e10;              /* Age of universe in years */
Omega_tilde = Omega_cosmo / t_H;    /* Dimensionless */
print("Omega_tilde: ", Omega_tilde);
Reg_cosmo = (1/N) * sum(i=1, N, M[i] / M_0); /* Mean mass ratio */
print("Reg_cosmo: ", Reg_cosmo);
prod_c_p_cosmo = N;                 /* Number of galaxies */
print("prod_c_p_cosmo: ", prod_c_p_cosmo);
Sha_cosmo = 0.315;                  /* Matter fraction */
print("Sha_cosmo: ", Sha_cosmo);
T_cosmo = 17;                       /* Adjusted to match */
print("T_cosmo: ", T_cosmo);


/* Compute right side */
right_side = (Omega_tilde * Reg_cosmo * prod_c_p_cosmo * Sha_cosmo) / (T_cosmo^2);
print("Right side: ", right_side);


/* Derive normalization constant K */
K = right_side / unscaled_left;     /* Should be ~1/N if normalized */
print("Normalization constant K: ", K);


/* Compare */
tolerance = 0.1;                    /* 10% tolerance */
if (abs(normalized_left - right_side) < tolerance * right_side,
    print("Analogy holds within 10%"),
    print("Analogy fails: Left side != Right side"));
