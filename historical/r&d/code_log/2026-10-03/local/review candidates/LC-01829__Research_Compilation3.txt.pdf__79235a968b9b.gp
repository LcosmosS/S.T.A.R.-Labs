N = length(log_mass);
print("Number of galaxies N: ", N);
M = vector(N, i, 10^log_mass[i]);
my_median(v) = {
    my(sorted = vecsort(v));
    my(len = length(sorted));
    if(len % 2 == 0,
        (sorted[len/2] + sorted[len/2 + 1]) / 2,
        sorted[(len+1)/2]
