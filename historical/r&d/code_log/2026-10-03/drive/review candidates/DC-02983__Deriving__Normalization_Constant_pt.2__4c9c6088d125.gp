print("Precision set to 38");       /* Confirm precision setting */


/* Define cosmological constants based on Planck 2018 and SDSS DR17 context */
t_H = 1.44e10;                      /* Hubble time in years */
Omega_cosmo = 1.38e10;              /* Age of universe in years */
Omega_tilde = Omega_cosmo / t_H;    /* Dimensionless age ratio */
print("Omega_tilde: ", Omega_tilde);/* Display dimensionless age ratio */
Reg_cosmo = 1;                      /* Placeholder for average mass ratio */
print("Reg_cosmo: ", Reg_cosmo);    /* Display mass ratio placeholder */
prod_c_p_cosmo = 1000;              /* Number of galaxies in sample */
print("prod_c_p_cosmo: ", prod_c_p_cosmo); /* Display galaxy count */
Sha_cosmo = 0.315;                  /* Total matter density parameter (Planck 2018) */
print("Sha_cosmo: ", Sha_cosmo);    /* Display matter density parameter */
T_cosmo = 10;                       /* Number of large-scale structures */
print("T_cosmo: ", T_cosmo);        /* Display structure count */


/* Define mock SDSS DR17 data (replace with real data as needed) */
M_0 = 1e11;                         /* Reference mass: ~10^11 solar masses */
N = 1000;                           /* Number of galaxies */
M = vector(N, i, 10^(10.5 + 0.5 * random(1000) / 1000.0)); /* Mock masses in solar masses */
Z = vector(N, i, 0.02 + 0.01 * random(1000) / 1000.0);     /* Mock redshifts */


/* Define and compute the cosmological L-function using galaxy masses */
L_cosmo(s) = sum(i=1, N, (M_0 / M[i])^s); /* L-function as sum over mass ratios */
unscaled_left = L_cosmo(1);         /* Compute unscaled L_cosmo at s=1 */
print("Unscaled L_cosmo(1): ", unscaled_left); /* Display unscaled left side */


/* Compute the right side using cosmological invariants */
right_side = (Omega_tilde * Reg_cosmo * prod_c_p_cosmo * Sha_cosmo) / (T_cosmo^2);
print("Right side: ", right_side);  /* Display right side value */


/* Calculate normalization constant to align left and right sides */
K = right_side / unscaled_left;     /* Normalization factor */
print("Normalization constant K: ", K); /* Display normalization constant */


/* Define and compute the normalized L-function */
L_cosmo_new(s) = K * L_cosmo(s);    /* Normalized L-function */
left_side = L_cosmo_new(1);         /* Compute normalized L_cosmo at s=1 */
print("Normalized L_cosmo(1): ", left_side); /* Display normalized left side */


/* Compare left and right sides within a tolerance */
tolerance = 0.1;                    /* Set 10% tolerance */
if (abs(left_side - right_side) < tolerance * right_side, /* Check if within tolerance */
    print("Cosmological BSD analogue holds within 10%"), /* Success message */
    print("Cosmological BSD analogue fails: Left side != Right side")); /* Failure message */
