a = vector(100, n, 1/n^2); /* Placeholder: replace with P(k) or C_l */
/* Define L-function */
L_cosmo(s) = sum(n=1, 100, a[n]/n^s);
/* Constants */
Omega_cosmo = 5.4e7; /* Virgo distance */
Reg_cosmo = 1722; /* Size ratio */
prod_c_p_cosmo = 2; /* Clusters */
Sha_cosmo = 0.87; /* Dark matter fraction */
T_cosmo = 4; /* Structural units */
/* Compute */
left = L_cosmo(1);
right = (Omega_cosmo * Reg_cosmo * prod_c_p_cosmo * Sha_cosmo) / (T_cosmo^2);
print("Left: ", left, " Right: ", right);
