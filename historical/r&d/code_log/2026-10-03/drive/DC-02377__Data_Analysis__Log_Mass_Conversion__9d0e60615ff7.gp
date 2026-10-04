for(j=1, n\2, {
  U1 = random(1.0);
  U2 = random(1.0);
  R = sqrt(-2 * log(U1));
  Theta = 2 * Pi * U2;
  Z0 = R * cos(Theta);
  Z1 = R * sin(Theta);
  log_mass[2*j-1] = mu + sig * Z0;
  log_mass[2*j] = mu + sig * Z1;
* })
* This uses the Box-Muller transform to fill the vector with normally distributed numbers.
* Compute Mass Values: Type M = vector(n, i, 10^log_mass[i]); and press Enter to convert log masses to actual masses.
* Sort and Find Median: Type M_sorted = vecsort(M); M0 = (M_sorted[n\2] + M_sorted[n\2 + 1]) / 2; and press Enter to find the median.
* Compute K_{\text{theory}}: Type sum_M_over_M0 = sum(i=1, n, M[i]/M0); sum_M0_over_M = sum(i=1, n, M0 / M[i]); K_theory = sum_M_over_M0 / sum_M0_over_M; print("K_theory = ", K_theory); and press Enter. It should be close to 1.
* Compute Skewness: Type these lines, pressing Enter after each:
mean = sum(i=1, n, log_mass[i]) / n;
variance = sum(i=1, n, (log_mass[i] - mean)^2) / (n - 1);
sd = sqrt(variance);
mu3 = sum(i=1, n, (log_mass[i] - mean)^3) / n;
* skewness = mu3 / sd^3; print("skewness = ", skewness);
* It should be close to 0.
* Verify Results: Type print("sample mean of log_mass = ", mean); print("sample sd of log_mass = ", sd); print("computed M0 = ", M0); print("theoretical M0 = ", 10^mu); and press Enter to check values are near expected (mean ≈ 10, sd ≈ 1, M0 ≈ 10^{10}).
