N = 1000; is the number of galaxies.
M = vector(N, i, 10^(10.5 + 0.5 * random(1000) / 1000.0)); generates mock masses; replace with actual masses from log_mass.
Z = vector(N, i, 0.02 + 0.01 * random(1000) / 1000.0); generates mock redshifts; replace with actual z values.
