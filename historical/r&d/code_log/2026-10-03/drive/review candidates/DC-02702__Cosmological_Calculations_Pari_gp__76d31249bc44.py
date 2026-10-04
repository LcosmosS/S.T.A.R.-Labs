# Extract z and logmass values
z_values = first_1000['z'].tolist() logmass_values = first_1000['logmass'].tolist()
# Print the lists enclosed in brackets
print("z values: [" + ','.join(map(str, z_values)) + "]") print("logmass values: [" + ','.join(map(str, logmass_values)) + "]")
