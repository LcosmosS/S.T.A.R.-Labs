data = readvec("C:\\temp\\load_vectors.txt");
n = length(data);
print("Min logmass: ", vecmin(data));
print("Max logmass: ", vecmax(data));
masses = vector(length(data), i, 10^data[i]);  \\ Try, adjust with offset if overflow
sorted_masses = vecsort(masses);
m0 = sorted_masses[floor((n+1)/2)];
sum_m_over_m0 = sum(i=1, n, masses[i] / m0);
sum_m0_over_m = sum(i=1, n, m0 / masses[i]);
k = sum_m_over_m0 / sum_m0_over_m;
print("K = ", k);
mean_logmass = sum(i=1, n, data[i]) / n;
deviations = vector(n, i, data[i] - mean_logmass);
variance = sum(i=1, n, deviations[i]^2) / (n - 1);
std_dev = sqrt(variance);
print("Mean logmass = ", mean_logmass);
print("Standard deviation = ", std_dev);
