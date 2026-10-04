import pandas as pd
# Load the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')
# Define key columns to process
key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr', 'petrorad_r', 'ellipticity']
# Filter out rows with missing values or -9999.0 (invalid entries)
valid_df = df[df[key_columns].notna().all(axis=1) & (df[key_columns] != -9999.0).all(axis=1)]
# Write to PARI/GP file
with open('C:\\temp\\STM_Extract_Valid.gp', 'w') as f: for col in key_columns: # Convert to float and then to string for PARI/GP compatibility values = ','.join(valid_df[col].astype(float).astype(str)) f.write(f"{col}=[{values}];\n") # Handle objid separately as a string (not used in computations) objid_values = ','.join(valid_df['objid'].astype(str)) f.write(f"objid=[{objid_values}];\n")
from sklearn.mixture import GaussianMixture import numpy as np
logmass = np.array(your_filtered_logmass_data) # Your logmass data gmm = GaussianMixture(n_components=3).fit(logmass.reshape(-1, 1)) groups = gmm.predict(logmass.reshape(-1, 1))
for i in range(3): # If you used 3 groups group_logmass = logmass[groups == i] group_z = np.array(z)[groups == i] group_sfr = np.array(sfr)[groups == i] group_ra = np.array(ra)[groups == i] print(f"Group {i}: Avg z = {np.mean(group_z)}, Avg sfr = {np.mean(group_sfr)}, Avg ra = {np.mean(group_ra)}")
