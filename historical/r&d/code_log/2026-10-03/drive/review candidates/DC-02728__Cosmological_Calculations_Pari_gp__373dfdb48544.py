# Extract z and logmass values
z_values = selected_df['z'].tolist() logmass_values = selected_df['logmass'].tolist()
# Print the number of selected rows
print(f"Number of selected rows: {len(selected_df)}")
# Print the lists enclosed in brackets
print("z values: [" + ','.join(map(str, z_values)) + "]") print("logmass values: [" + ','.join(map(str, logmass_values)) + "]")
