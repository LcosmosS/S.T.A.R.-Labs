df = df[(df['logmass'] != -9999) & (df['sfr'] != -9999) & (df['z'] != -9999)]
# Extract the columns to lists
log_mass = df['logmass'].tolist() sfr = df['sfr'].tolist() z = df['z'].tolist()
# Convert lists to string format
log_mass_str = '[' + ','.join(map(str, log_mass)) + ']' sfr_str = '[' + ','.join(map(str, sfr)) + ']' z_str = '[' + ','.join(map(str, z)) + ']'
# Print in a single line
print(f'log_mass={log_mass_str} sfr={sfr_str} z={z_str}')
# Optional: If you want to filter out missing values (-9999), uncomment the following lines # df = df[df['logmass'] != -9999] # df = df[df['sfr'] != -9999] # df = df[df['z'] != -9999] # Then re-extract the lists and print
