num_sim = 100;
K_sum = 0;
for (j=1, num_sim, {
  log_mass_sim = simulate_log_mass(500, 9.7843, 0.3645);
  K_sum += compute_K_theory(log_mass_sim);
