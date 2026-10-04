log_mass = [10.29471, 11.36537, 10.56586, 9.36387, 10.3831, 10.8335, 10.2848, 10.5113, 10.1293];

/* Function to compute the median */
my_median(v) = {
   my(s = vecsort(v), n = #s);
   if (n % 2 == 1, s[(n+1)/2], (s[n/2] + s[n/2+1])/2);
}

/* Convert log mass to linear mass */
M = vector(#log_mass, i, 10^log_mass[i]);
M0 = 10^my_median(log_mass); /* Reference mass is the median */

/* Compute the sums for K */
sum_M_over_M0 = sum(i=1, #M, M[i]/M0);
sum_M0_over_M = sum(i=1, #M, M0/M[i]);

/* Compute the Normalization Constant K */
K = sum_M_over_M0 / sum_M0_over_M;

print("Normalization Constant K for N=9: ", K);
