print("Number of -9999 in log_mass:", sum(i=1, #log_mass, log_mass[i] == -9999));
print("Number of -9999 in sfr:", sum(i=1, #sfr, sfr[i] == -9999));
         * print("Number of -9999 in z:", sum(i=1, #z, z[i] == -9999));
         * If present, filter them out:
valid_indices = select(i -> log_mass[i] != -9999 && sfr[i] != -9999 && z[i] != -9999, vector(#log_mass, i, i));
log_mass_filtered = vector(#valid_indices, j, log_mass[valid_indices[j]]);
sfr_filtered = vector(#valid_indices, j, sfr[valid_indices[j]]);
         * z_filtered = vector(#valid_indices, j, z[valid_indices[j]]);
