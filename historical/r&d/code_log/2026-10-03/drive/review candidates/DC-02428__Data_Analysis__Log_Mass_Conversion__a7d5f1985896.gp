valid_indices_all = select(i -> log_mass[i] != -9999 && sfr[i] != -9999 && z[i] != -9999, Vecsmall(1,#log_mass));
log_mass_all = vector(#valid_indices_all, j, log_mass[valid_indices_all[j]]);
K_all = compute_K_theory(log_mass_all);
skew_all = compute_skewness(log_mass_all);
         * print("All data: K_theory = ", K_all, ", skewness = ", skew_all);
