  M0 = median(log_mass);
K_all = compute_K_theory(log_mass_filtered);
skew_all = compute_skewness(log_mass_filtered);
print("All data: K_theory = ", K_all, ", skewness = ", skew_all);
for(k=1, #z_bins - 1, {
  ***   sorry, embedded braces (in parser) is not yet implemented.
