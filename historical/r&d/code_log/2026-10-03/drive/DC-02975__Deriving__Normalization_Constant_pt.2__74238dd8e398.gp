M = read("masses.txt");    /* Vector of masses */
* Z = read("redshifts.txt"); /* Vector of redshifts */
   * Note: You used gpM in your original code but referenced M later. Stick with M for consistency unless gpM is intentional.
* Verify: Check the data loaded correctly:
* pari
print("Number of masses: ", length(M));
print("First 5 masses: ", vector(min(5, length(M)), i, M[i]));
print("Number of redshifts: ", length(Z));
* print("First 5 redshifts: ", vector(min(5, length(Z)), i, Z[i]));
   * If everything works, length(M) and length(Z) should match the number of entries in your files, and the first 5 elements should display correctly.
