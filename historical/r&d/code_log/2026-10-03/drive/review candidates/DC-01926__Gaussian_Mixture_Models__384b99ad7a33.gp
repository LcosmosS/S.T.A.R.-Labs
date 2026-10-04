n = #mass_sorted;          /* Total number of galaxies */
bins = 5;                  /* Number of bins */
bin_size = floor(n / bins); /* Size of each bin */
end_indices = vector(bins, k, min(n, k * bin_size));
                                             * #mass_sorted: Length of the mass vector.
                                             * floor(n / bins): Ensures integer bin sizes.
