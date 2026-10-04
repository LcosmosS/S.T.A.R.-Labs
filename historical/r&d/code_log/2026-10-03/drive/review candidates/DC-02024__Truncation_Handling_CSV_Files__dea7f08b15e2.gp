print("Type of num_sim: ", type(num_sim));  \\ Verify it's t_INT
for (j=1, num_sim, {
  log_mass_sim = simulate_log_mass(N, mu, std_dev);
  K = compute_K_theory(log_mass_sim);
  kurt = compute_kurtosis(log_mass_sim);
  print("Simulation ", j, ": K_theory = ", K, ", Kurtosis = ", kurt);
