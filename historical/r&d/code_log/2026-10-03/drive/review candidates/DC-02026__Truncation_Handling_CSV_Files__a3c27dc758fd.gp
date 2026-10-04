data = readvec("C:\\temp\\load_vectors.txt");
n = length(data);
logmasses = vector(n, i, data[i][5]);
mu = sum(i=1, n, logmasses[i]) / n;
variance = sum(i=1, n, (logmasses[i] - mu)^2) / (n - 1);
std_dev = sqrt(variance);
N = n;
total_sims = 1000;  \\ Use a new variable name to avoid conflicts


\\ Define functions (assuming already defined)
box_muller() = {
  my(u1, u2, r, theta);
  u1 = randomreal();
  u2 = randomreal();
  r = sqrt(-2 * log(u1));
  theta = 2 * Pi * u2;
