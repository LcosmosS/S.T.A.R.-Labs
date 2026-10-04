for (j=1, num_sim, {
  log_mass_sim = simulate_log_mass(N, mu, std_dev);
  K = compute_K_theory(log_mass_sim);
  kurtosis = compute_kurtosis(log_mass_sim);
  print("Simulation ", j, ": K_theory = ", K, ", Kurtosis = ", kurtosis);
  K_sum = K_sum + K;
  kurtosis_sum = kurtosis_sum + kurtosis;
})
