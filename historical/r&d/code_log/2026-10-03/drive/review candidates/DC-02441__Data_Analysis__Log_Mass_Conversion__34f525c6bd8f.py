if missing_columns:
    print(f"Error: Missing columns in CSV: {', '.join(missing_columns)}")
    exit(1)


# Replace -9999 with NaN and drop rows with NaN in required columns
df[required_columns] = df[required_columns].replace(-9999, float('nan'))
df = df.dropna(subset=required_columns)


# Extract the columns to lists
log_mass = df['logmass'].tolist()
sfr = df['sfr'].tolist()
z = df['z'].tolist()


# Convert lists to string format
log_mass_str = '[' + ','.join(map(str, log_mass)) + ']'
sfr_str = '[' + ','.join(map(str, sfr)) + ']'
z_str = '[' + ','.join(map(str, z)) + ']'


# Print in a single line
print(f'log_mass={log_mass_str} sfr={sfr_str} z={z_str}')


# Optional: Add checks for verification
print("Filtered number of rows:", len(df))
print("Number of -9999 in log_mass:", sum([1 for x in log_mass if x == -9999]))
print("Number of -9999 in sfr:", sum([1 for x in sfr if x == -9999]))
print("Number of -9999 in z:", sum([1 for x in z if x == -9999]))
