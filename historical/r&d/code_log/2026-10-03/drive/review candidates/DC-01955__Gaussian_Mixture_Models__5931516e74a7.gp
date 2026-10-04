n = #mass_sorted;
bins = 5;
bin_size = floor(n / bins);
end_indices = vector(bins, k, min(n, k * bin_size));
                                             * n is the total number of masses.
                                             * bin_size is the number of masses per bin.
