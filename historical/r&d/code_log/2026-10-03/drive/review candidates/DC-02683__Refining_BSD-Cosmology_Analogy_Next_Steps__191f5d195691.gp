c = 3e5; /* Speed of light in km/s */
H_0 = 67.4; /* Hubble constant in km/s/Mpc */
d_0 = 1; /* Reference distance: 1 Mpc */
/* Assume z vector from SDSS DR17 data */
z = vector(N, i, /* redshift values */);
d = vector(N, i, (c * z[i]) / H_0); /* Distances in Mpc */
