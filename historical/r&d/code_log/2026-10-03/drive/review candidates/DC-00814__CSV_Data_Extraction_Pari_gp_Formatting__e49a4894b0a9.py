import pandas as pd
# Read the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')
# List of columns to process (excluding objid)
columns = ['ra', 'dec', 'z', 'logmass', 'petrorad_r', 'ellipticity', 'sfr', 'metallicity']
# Initialize a list to hold formatted strings
formatted_list = []
for column in columns: # Filter out invalid values valid_values = df[df[column] != -9999.0][column] # Convert to string str_values = valid_values.astype(str).tolist() # Join with commas values_str = ','.join(str_values) # Create formatted string formatted = f"{column}=[{values_str}];" # Append to list formatted_list.append(formatted)
# Concatenate all formatted strings without spaces
output = ''.join(formatted_list)
# Print the output
print(output)
