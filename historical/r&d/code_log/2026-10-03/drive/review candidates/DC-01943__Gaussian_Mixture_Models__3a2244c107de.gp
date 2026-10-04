valid = vector(n, i, mass[i] > 0 && sfr[i] >= 0);
mass = select(i -> valid[i], mass);
sfr = select(i -> valid[i], sfr);
metallicity = select(i -> valid[i], metallicity);
n = #mass;  \\ Update length
