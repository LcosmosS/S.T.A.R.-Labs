masses = readvec("masses.txt");
\\ Compute N
N = length(masses);
\\ Compute sorted masses
sorted_masses = vecsort(masses);
\\ Compute M0 as median
if (N % 2 == 1,
    M0 = sorted_masses[(N+1)/2],
    M0 = (sorted_masses[N/2] + sorted_masses[N/2 + 1]) / 2
