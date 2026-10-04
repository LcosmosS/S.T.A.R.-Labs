n = length(data);
logmasses = vector(n, i, data[i][5]);
mu = sum(i=1, n, logmasses[i]) / n;
variance = sum(i=1, n, (logmasses[i] - mu)^2) / (n - 1);
