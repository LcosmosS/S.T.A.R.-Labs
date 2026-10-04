  z_min = z_bins[idx];
  z_max = z_bins[idx + 1];
  bin_indices = select(i -> z_filtered[i] >= z_min && z_filtered[i] < z_max, vector(#z_filtered, i, i));
for(idx=1, #z_bins - 1, {
  ***   sorry, embedded braces (in parser) is not yet implemented.
