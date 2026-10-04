n = 1000;  \\ Number of galaxies
mass = vector(n, i, 10^random(10.0));  \\ Example: log10(mass) between 0 and 10
sfr = vector(n, i, random(100.0));     \\ Example: SFR between 0 and 100 M_sun/yr
metallicity = vector(n, i, 8.0 + random(2.0));  \\ Example: metallicity between 8 and 10
