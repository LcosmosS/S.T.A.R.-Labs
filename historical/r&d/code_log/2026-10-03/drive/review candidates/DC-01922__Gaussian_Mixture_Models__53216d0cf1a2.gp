n = #mass_sorted;
bins = 5;
bin_size = floor(n / bins);
end_indices = vector(bins, k, min(n, k * bin_size));
