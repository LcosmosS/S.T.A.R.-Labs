for (j=1, num_sim, {
  log_mass_sim = simulate_log_mass(N, mu, sigma);
  K = compute_K_theory(log_mass_sim);
  kurt = compute_kurtosis(log_mass_sim);
  print("Simulation ", j, ": K_theory = ", K, ", Kurtosis = ", kurt);
