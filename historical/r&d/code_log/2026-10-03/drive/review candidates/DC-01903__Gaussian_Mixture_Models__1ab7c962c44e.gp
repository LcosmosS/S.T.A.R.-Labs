log_mass = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
M_sorted = vecsort(log_mass);
end_indices = [2, 4, 6, 8, 10];


\\ Call the function
result = compute_L_cosmo(1);
print("Result: ", result);
