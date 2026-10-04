total_sims = 1000;
\\ Run simulations
for (j=1, total_sims, {
  log_mass_sim = simulate_log_mass(N, mu, std_dev);
  K = compute_K_theory(log_mass_sim);
  kurt = compute_kurtosis(log_mass_sim);
  print("Simulation ", j, ": K_theory = ", K, ", Kurtosis = ", kurt);
