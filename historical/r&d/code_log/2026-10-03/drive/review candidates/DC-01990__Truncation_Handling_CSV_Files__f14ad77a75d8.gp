n = length(masses);
sorted_masses = vecsort(masses);
m0 = sorted_masses[floor((n+1)/2)];  \\ Median for odd n, adjust for even if needed
