log_mass = [1, 2, 3, 4, 5];  /* Example data */
log_mass_sorted = vecsort(log_mass);
n = #log_mass;
M_sorted = vector(n, i, 10^log_mass_sorted[i]);
end_indices = vector(5, k, floor((k / 5) * n));
result = compute_L_cosmo(1);
   * print(result);
