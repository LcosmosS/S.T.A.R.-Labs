# Print columns for verification
print("Columns in CSV:", df.columns.tolist())
# Define required columns with correct names, assuming petrorad is actually petrorad_r
required_columns = ['objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r', 'ellipticity', 'sfr', 'metallicity']
# Check for required columns
