import pandas as pd


# Load the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Define key columns to process
key_columns = ['ra', 'dec', 'z', 'logmass', 'sfr', 'petrorad_r', 'ellipticity']


# Filter out rows with missing values or -9999.0 (invalid entries)
valid_df = df[df[key_columns].notna().all(axis=1) & (df[key_columns] != -9999.0).all(axis=1)]


# Write to PARI/GP file
with open('C:\\temp\\STM_Extract_Valid.gp', 'w') as f:
    for col in key_columns:
        # Convert to float and then to string for PARI/GP compatibility
        values = ','.join(valid_df[col].astype(float).astype(str))
        f.write(f"{col}=[{values}];\n")
    # Handle objid separately as a string (not used in computations)
    objid_values = ','.join(valid_df['objid'].astype(str))
    f.write(f"objid=[{objid_values}];\n")
