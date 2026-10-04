K_sum = 0; num_sim = 100; K_values = vector(num_sim);
for (j=1, num_sim, 
  log_mass_sim = simulate_log_mass(500, 9.7843, 0.3645);
  M0 = vecmedian(log_mass_sim); 
  K_sim = sum(i=1, #log_mass_sim, exp(log_mass_sim[i] - M0)) / sum(i=1, #log_mass_sim, exp(M0 - log_mass_sim[i]));
  K_values[j] = K_sim;
  K_sum += K_sim;
