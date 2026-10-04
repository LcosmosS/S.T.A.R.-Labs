log_mass = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];  /* Example data */
M_sorted = vecsort(log_mass);                /* Sorted masses */
n = #M_sorted;                               /* Length of M_sorted (10) */
end_indices = vector(5, k, floor((k / 5) * n));  /* Bin endpoints: [2, 4, 6, 8, 10] */
