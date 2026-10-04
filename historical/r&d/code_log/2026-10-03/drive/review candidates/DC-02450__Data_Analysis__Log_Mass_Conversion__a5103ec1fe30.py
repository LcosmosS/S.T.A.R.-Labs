# Print columns for verification
print("Columns in CSV:", df.columns.tolist())


# Define required columns
required_columns = ['objid', 'ra', 'dec', 'z', 'logmass', 'petrorad_r', 'ellipticity', 'sfr', 'metallicity']


# Check for required columns
