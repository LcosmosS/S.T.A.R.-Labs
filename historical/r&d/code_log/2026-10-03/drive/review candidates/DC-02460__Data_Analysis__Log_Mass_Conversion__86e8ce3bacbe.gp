n = #log_mass;
indices = vector(n, i, i);
         * valid_indices = select(i -> log_mass[i] != -9999 && sfr[i] != -9999 && z[i] != -9999, indices);
