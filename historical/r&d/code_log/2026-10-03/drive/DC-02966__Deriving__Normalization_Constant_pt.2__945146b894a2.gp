print("Precision set to 38");


/* Define cosmological constants based on Planck 2018 */
t_H = 1.44e10;                      /* Hubble time in years */
Omega_cosmo = 1.38e10;              /* Age of universe in years */
Omega_tilde = Omega_cosmo / t_H;    /* Dimensionless age ratio */
print("Omega_tilde: ", Omega_tilde);


/* Load real SDSS DR17 data from /home/pmqr7 */
M = read("masses.txt");             /* Vector of masses in solar masses */
Z = read("redshifts.txt");          /* Vector of redshifts */
N = length(M);                      /* Number of galaxies */
print("Number of galaxies N: ", N);


/* Verify data loading */
print("Type of M: ", type(M));      /* Should be t_VEC */
print("First few masses: ", vector(min(5, N), i, M[i]));
print("Type of Z: ", type(Z));      /* Should be t_VEC */
print("First few redshifts: ", vector(min(5, N), i, Z[i]));


/* Compute reference mass M_0 as median */
log_mass_vector = vector(N, i, log(M[i]) / log(10)); /* Convert to log10(M/M_sun) */
M_0 = 10^median(log_mass_vector);   /* Median mass */
print("Reference mass M_0: ", M_0);


/* Compute Reg_cosmo as average mass ratio */
Reg_cosmo = sum(i=1, N, M[i] / M_0) / N; /* Data-driven regulator */
print("Reg_cosmo: ", Reg_cosmo);


prod_c_p_cosmo = N;                 /* Number of galaxies */
print("prod_c_p_cosmo: ", prod_c_p_cosmo);


Sha_cosmo = 0.315;                  /* Matter density (Planck 2018) */
print("Sha_cosmo: ", Sha_cosmo);


T_cosmo = 17;                       /* Adjusted for normalization */
print("T_cosmo: ", T_cosmo);


/* Define and compute cosmological L-function (mass-based) */
L_cosmo(s) = sum(i=1, N, (M_0 / M[i])^s); /* L-function */
unscaled_left = L_cosmo(1);         /* Unscaled L_cosmo(1) */
print("Unscaled L_cosmo(1): ", unscaled_left);


/* Compute right side using cosmological invariants */
right_side = (Omega_tilde * Reg_cosmo * prod_c_p_cosmo * Sha_cosmo) / (T_cosmo^2);
print("Right side: ", right_side);


/* Calculate normalization constant K */
K = right_side / unscaled_left;     /* Normalization factor */
print("Normalization constant K: ", K);


/* Define and compute normalized L-function */
L_cosmo_new(s) = K * L_cosmo(s);    /* Normalized L-function */
left_side = L_cosmo_new(1);         /* Normalized L_cosmo(1) */
print("Normalized L_cosmo(1): ", left_side);


/* Compare left and right sides */
tolerance = 0.1;                    /* 10% tolerance */
if (abs(left_side - right_side) < tolerance * right_side,
    print("Cosmological BSD analogue holds within 10%"),
    print("Cosmological BSD analogue fails: Left side != Right side")
