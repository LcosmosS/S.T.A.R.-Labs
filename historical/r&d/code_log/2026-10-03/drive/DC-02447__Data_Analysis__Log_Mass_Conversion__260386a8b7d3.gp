for(bin_index=1, #z_bins - 1, {
  z_min = z_bins[bin_index];
  z_max = z_bins[bin_index + 1];
  bin_indices = select(i -> z_filtered[i] >= z_min && z_filtered[i] < z_max, vector(#z_filtered, i, i));
  if (#bin_indices == 0, next);
  sfr_bin = vector(#bin_indices, j, sfr_filtered[bin_indices[j]]);
  median_sfr = compute_median(sfr_bin);
  high_sfr_indices = select(i -> sfr_filtered[i] > median_sfr, bin_indices);
  low_sfr_indices = select(i -> sfr_filtered[i] <= median_sfr, bin_indices);
  log_mass_high_sfr = vector(#high_sfr_indices, j, log_mass_filtered[high_sfr_indices[j]]);
  log_mass_low_sfr = vector(#low_sfr_indices, j, log_mass_filtered[low_sfr_indices[j]]);
  K_high = compute_K_theory(log_mass_high_sfr);
  skew_high = compute_skewness(log_mass_high_sfr);
  K_low = compute_K_theory(log_mass_low_sfr);
  skew_low = compute_skewness(log_mass_low_sfr);
  print("z: ", z_min, " to ", z_max);
  print("high_sfr: K_theory = ", K_high, ", skewness = ", skew_high);
  print("low_sfr: K_theory = ", K_low, ", skewness = ", skew_low);
         * });
         * This ensures the loop is treated as a single block, avoiding syntax errors.
         2. Type Errors with Variables:
         * The errors like "incorrect type in gtos [integer expected] (t_POL)" when accessing z_bins[bin_index] suggest that bin_index is not an integer but a polynomial or another type. This might be because bin_index was previously defined as a polynomial in the session.
         * Similarly, errors in select and vector indexing suggest type mismatches, likely due to z_min, z_max, or bin_indices being polynomials instead of real numbers or vectors.
         * Solution: Use a different variable name that is not previously defined, such as idx, and ensure z_bins is a vector of real numbers:
         * Check type(z_bins); it should be "t_VEC". If it's "t_POL", redefine:
         * z_bins = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4];
         * Use idx in the loop:
         * for(idx=1, #z_bins - 1, { ... });
         * Clear any previous definitions if needed: kill(bin_index) before redefining.
         3. Forbidden Comparison in Select:
         * The error ">=: forbidden comparison t_REAL , t_POL" in the select statement indicates that z_min or z_max is a polynomial, not a real number, causing a type mismatch when comparing with z_filtered[i], which is presumably a real number.
         * This ties back to the previous error where bin_index was a polynomial, leading to z_min and z_max being polynomials.
         * Solution: Ensure z_bins is a vector of real numbers, and use idx as an integer in the loop, as above. The comparison should then work, as z_filtered[i] is a real number, and z_min, z_max will be real numbers from the vector.
         4. Incorrect Type in Vector Indexing:
         * Errors like "incorrect type in [] OCcompo1 [not a vector] (t_POL)" when trying to access sfr_filtered[bin_indices[j]] suggest that bin_indices[j] is not an integer but a polynomial, again likely due to variable type conflicts.
         * Solution: Ensure bin_indices is a vector of integers, which it should be if select is used with vector(#z_filtered, i, i). Verify with print(type(bin_indices));, expecting "t_VEC". If it's "t_POL", redefine the loop and select with correct types.
         5. Function Return Issues:
         * When printing K_all and skew_all, it showed "returnK_theory" and "returnskewness", indicating the functions didn't return numerical values but strings or other types. This is because the functions were defined with "return" statements, which are not standard in PARI/GP.
         * Solution: Redefine the functions without "return", making sure the last expression is the value to be returned:
         * Change:
         * compute_K_theory(log_mass) = { ... return K_theory; }
         * to:
         * compute_K_theory(log_mass) = { ... K_theory }
         * Similarly for compute_skewness and compute_median, ensuring the last line is the value, like:
compute_skewness(log_mass) = { ... skewness }
         * compute_median(v) = { ... if (n % 2 == 0, (v_sorted[n/2] + v_sorted[n/2 + 1]) / 2, v_sorted[(n+1)/2]) }
         * This fixes the function return issue, ensuring K_all and skew_all hold numerical values.
         6. Skewness Calculation for Small n:
         * The message "n too small" in skewness calculation indicates that for some subgroups, the number of elements is less than 3, making skewness undefined. This is handled in the function, but it's good to note that some bins might have too few points.
         * Solution: Ensure that subgroups have sufficient data points. If not, consider adjusting bin sizes or merging bins, or note these cases in analysis.
