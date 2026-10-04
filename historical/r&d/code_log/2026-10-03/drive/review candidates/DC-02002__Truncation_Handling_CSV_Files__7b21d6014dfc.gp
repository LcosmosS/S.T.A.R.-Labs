lines = readstr("C:\\temp\\load_vectors.txt");
data_str = lines[1];  // Assuming one line
data = Vecsmall(data_str);
data = vector(length(data), i, eval(data[i]));
num_columns = 9;
n_rows = floor(length(data) / num_columns);
logmasses = vector(n_rows, i, data[5 + (i-1)*num_columns]);
masses = vector(n_rows, i, 10^logmasses[i]);
sorted_masses = vecsort(masses);
m0 = sorted_masses[floor((n_rows+1)/2)];
sum_m_over_m0 = sum(i=1, n_rows, masses[i] / m0);
sum_m0_over_m = sum(i=1, n_rows, m0 / masses[i]);
k = sum_m_over_m0 / sum_m0_over_m;
print("K = ", k);
mean_logmass = sum(i=1, n_rows, logmasses[i]) / n_rows;
variance = sum(i=1, n_rows, (logmasses[i] - mean_logmass)^2) / (n_rows - 1);
std_dev = sqrt(variance);
print("Mean logmass = ", mean_logmass);
* print("Standard deviation = ", std_dev);
