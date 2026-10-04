data = readvec("C:\temp\GMM.txt"); n = length(data); logmasses = vector(n, i, data[i][5]); mu = sum(i=1, n, logmasses[i]) / n; variance = sum(i=1, n, (logmasses[i] - mu)^2) / (n - 1); std_dev = sqrt(variance); N = n; total_sims = 8807;
box_muller() = { my(u1, u2, r, theta); u1 = random(1.0); u2 = random(1.0); r = sqrt(-2 * log(u1)); theta = 2 * Pi * u2; [r * cos(theta), r * sin(theta)] }
simulate_log_mass(N, mu, sigma) = { my(v, i, pair); v = vector(N); for (i=1, floor(N/2), pair = box_muller(); v[2*i-1] = mu + sigma * pair[1]; if (2*i <= N, v[2*i] = mu + sigma * pair[2]); ); if (N % 2 == 1, pair = box_muller(); v[N] = mu + sigma * pair[1]; ); v }
log_mass_sim = simulate_log_mass(); K_sim = compute_K_theory(log_mass_sim); print("Simulated K_theory: ", K_sim); num_sim=8000; K_sum = 0;
compute_K_theory(v) = { my(n = length(v), masses, sorted_masses, m0, sum_m_over_m0, sum_m0_over_m, k); masses = vector(n, i, 10^v[i]); sorted_masses = vecsort(masses); m0 = sorted_masses[floor((n+1)/2)]; sum_m_over_m0 = sum(i=1, n, masses[i] / m0); sum_m0_over_m = sum(i=1, n, m0 / masses[i]); k = sum_m_over_m0 / sum_m0_over_m; k }
compute_kurtosis(v) = { my(n = length(v), mean, m4, variance); mean = sum(i=1, n, v[i]) / n; m4 = sum(i=1, n, (v[i] - mean)^4) / n; variance = sum(i=1, n, (v[i] - mean)^2) / n; m4 / variance^2 }
mean_K = K_sum / num_sim;
num_sim=8807; K_sum = 0; for (j=1, num_sim, log_mass_sim = simulate_log_mass(N, mu, sigma); K = compute_K_theory(log_mass_sim); kurtosis = compute_kurtosis(log_mass_sim); print("Simulation ", j, ": K_theory = ", K, ", Kurtosis = ", kurtosis); K_sum = K_sum + K; kurtosis_sum = kurtosis_sum + kurtosis; );
print("Mean simulated K_theory: ", mean_K);if (z_min == 0.05 &&<5 && z_max == 0.1, write("subgroup_z_0.05_0.1_low_sfr.txt", log_mass_low_sfr));
