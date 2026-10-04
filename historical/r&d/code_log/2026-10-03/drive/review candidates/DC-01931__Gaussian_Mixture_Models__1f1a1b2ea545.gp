N = #mass_sorted;
elems_per_bin = floor(N / B);
end_indices = vector(B, k, min(N, k * elems_per_bin));
if (N % B != 0, end_indices[B] = N);  \\ Adjust the last bin to include remaining elements
