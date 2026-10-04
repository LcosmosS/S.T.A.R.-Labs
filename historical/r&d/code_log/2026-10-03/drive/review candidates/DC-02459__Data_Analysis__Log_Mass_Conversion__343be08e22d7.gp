n = #log_mass;
indices = vector(n, i, i);
valid_indices = select(i -> log_mass[i] != -9999 && sfr[i] != -9999 && z[i] != -9999, indices);
log_mass_filtered = vector(#valid_indices, j, log_mass[valid_indices[j]]);
sfr_filtered = vector(#valid_indices, j, sfr[valid_indices[j]]);
         * z_filtered = vector(#valid_indices, j, z[valid_indices[j]]);
