data = readvec("C:\\temp\\load_vectors.txt");
n = length(data);
logmasses = vector(n, i, data[i][5]);  // Extract logmass (5th column, 1-based indexing)
masses = vector(n, i, 10^logmasses[i]);
sorted_masses = vecsort(masses);
m0 = sorted_masses[floor((n+1)/2)];  // Median mass
sum_m_over_m0 = sum(i=1, n, masses[i] / m0);
sum_m0_over_m = sum(i=1, n, m0 / masses[i]);
k = sum_m_over_m0 / sum_m0_over_m;
print("K = ", k);
mean_logmass = sum(i=1, n, logmasses[i]) / n;
variance = sum(i=1, n, (logmasses[i] - mean_logmass)^2) / (n - 1);
std_dev = sqrt(variance);
print("Mean logmass = ", mean_logmass);
print("Standard deviation = ", std_dev);
