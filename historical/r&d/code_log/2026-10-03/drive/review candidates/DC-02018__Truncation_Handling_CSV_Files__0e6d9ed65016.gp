data = readvec("C:\\temp\\load_vectors.txt");
n = length(data);
logmasses = vector(n, i, data[i][5]);
mu = sum(i=1, n, logmasses[i]) / n;
variance = sum(i=1, n, (logmasses[i] - mu)^2) / (n - 1);
std_dev = sqrt(variance);
N = n;  // Set sample size to match data, or choose, e.g., 500
num_sim = 1000;


// Define box_muller function
box_muller() = {
  my(u1, u2, r, theta);
  u1 = random(1.0);
  u2 = random(1.0);
  r = sqrt(-2 * log(u1));
  theta = 2 * Pi * u2;
