M = read("masses.txt");    /* Vector of masses */
* Z = read("redshifts.txt"); /* Vector of redshifts */
* Verify the data:
* pari
print("Number of masses: ", length(M));
print("First 5 masses: ", vector(min(5, length(M)), i, M[i]));
print("Number of redshifts: ", length(Z));
* print("First 5 redshifts: ", vector(min(5, length(Z)), i, Z[i]));
