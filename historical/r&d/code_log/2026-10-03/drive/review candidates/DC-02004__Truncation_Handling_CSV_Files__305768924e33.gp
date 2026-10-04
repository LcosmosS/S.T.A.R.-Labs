logmasses = vector(n_rows, i, data[i][5]);  // Extract logmass
mean_logmass = sum(i=1, n_rows, logmasses[i]) / n_rows;
variance = sum(i=1, n_rows, (logmasses[i] - mean_logmass)^2) / (n_rows - 1);
std_dev = sqrt(variance);
