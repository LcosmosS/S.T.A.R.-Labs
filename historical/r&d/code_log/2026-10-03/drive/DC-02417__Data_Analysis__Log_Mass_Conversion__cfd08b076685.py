# Check for required columns
required_columns = ['logmass', 'sfr', 'z']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Error: Missing columns in CSV: {', '.join(missing_columns)}")
    exit(1)


# Filter out rows where any of logmass, sfr, or z are -9999
df = df[(df['logmass'] != -9999) & (df['sfr'] != -9999) & (df['z'] != -9999)]


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
