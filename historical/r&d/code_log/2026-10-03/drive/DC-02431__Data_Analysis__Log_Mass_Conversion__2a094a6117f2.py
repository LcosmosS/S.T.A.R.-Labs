# Print columns for verification
print("Columns in CSV:", df.columns.tolist())


# Define required columns
required_columns = ['objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r', 'ellipticity', 'sfr', 'metallicity']


# Check for required columns
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Error: Missing columns in CSV: {', '.join(missing_columns)}")
    exit(1)


# Print original number of rows for verification
print("Original number of rows:", len(df))


# Replace -9999 with NaN in required columns and drop rows with any NaN
df[required_columns] = df[required_columns].replace(-9999, float('nan'))
df = df.dropna(subset=required_columns)


# Print filtered number of rows for verification
print("Filtered number of rows:", len(df))


# Extract the columns to lists
objid = df['objid'].tolist()
ra = df['ra'].tolist()
dec = df['dec'].tolist()
z = df['z'].tolist()
log_mass = df['logmass'].tolist()
petrorad_r = df['petrorad_r'].tolist()
ellipticity = df['ellipticity'].tolist()
sfr = df['sfr'].tolist()
metallicity = df['metallicity'].tolist()


# Convert lists to string format
objid_str = '[' + ','.join(map(str, objid)) + ']'
ra_str = '[' + ','.join(map(str, ra)) + ']'
dec_str = '[' + ','.join(map(str, dec)) + ']'
z_str = '[' + ','.join(map(str, z)) + ']'
log_mass_str = '[' + ','.join(map(str, log_mass)) + ']'
petrorad_r_str = '[' + ','.join(map(str, petrorad_r)) + ']'
ellipticity_str = '[' + ','.join(map(str, ellipticity)) + ']'
sfr_str = '[' + ','.join(map(str, sfr)) + ']'
metallicity_str = '[' + ','.join(map(str, metallicity)) + ']'


# Note: For very long outputs, redirect to a file with: python analyze_galaxy_data.py > output.txt to avoid console wrapping
# Print in a single line
print(f'objid={objid_str} ra={ra_str} dec={dec_str} z={z_str} log_mass={log_mass_str} petrorad_r={petrorad_r_str} ellipticity={ellipticity_str} sfr={sfr_str} metallicity={metallicity_str}')


# Optional: Add checks for verification
print("Number of -9999 in objid:", sum([1 for x in objid if x == -9999]))
print("Number of -9999 in ra:", sum([1 for x in ra if x == -9999]))
print("Number of -9999 in dec:", sum([1 for x in dec if x == -9999]))
print("Number of -9999 in z:", sum([1 for x in z if x == -9999]))
print("Number of -9999 in log_mass:", sum([1 for x in log_mass if x == -9999]))
print("Number of -9999 in petrorad_r:", sum([1 for x in petrorad_r if x == -9999]))
print("Number of -9999 in ellipticity:", sum([1 for x in ellipticity if x == -9999]))
print("Number of -9999 in sfr:", sum([1 for x in sfr if x == -9999]))
print("Number of -9999 in metallicity:", sum([1 for x in metallicity if x == -9999]))
