masses = readvec("masses.txt");


\\ Compute the number of masses
N = length(masses);


\\ Sort the masses to find the median
sorted_masses = vecsort(masses);


\\ Compute the median mass M0
if (N % 2 == 1,
    M0 = sorted_masses[(N+1)/2],
    M0 = (sorted_masses[N/2] + sorted_masses[N/2 + 1]) / 2
