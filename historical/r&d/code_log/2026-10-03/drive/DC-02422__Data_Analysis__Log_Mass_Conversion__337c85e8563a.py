print("Number of -9999 in log_mass:", sum([1 for x in log_mass if x == -9999]))
print("Number of -9999 in sfr:", sum([1 for x in sfr if x == -9999]))
         * print("Number of -9999 in z:", sum([1 for x in z if x == -9999]))
         * These checks will help determine if filtering worked, with expected output showing reduced rows and no -9999 in the lists.
         4. Adaptation for Robust Filtering:
         * To ensure all invalid entries (both -9999 and NaN) are filtered out, modify the script to replace -9999 with NaN and drop rows with NaN in the required columns, which is a more robust approach:
df[required_columns] = df[required_columns].replace(-9999, float('nan'))
         * df = df.dropna(subset=required_columns)
         * This handles both cases, ensuring no missing values in the output, which aligns with the user's intent to filter out "invalid entries" and improves data quality for testing the BDS cosmology theory.
