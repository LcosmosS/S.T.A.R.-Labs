import pandas as pd

# Load the first 1,250 rows from the CSV file
df = pd.read_csv("Stellar_Mass2_Table.csv", nrows=1250)

# Filter out rows where logmass is invalid (-9999)
df_valid = df[df['logmass'] != -9999]

# Check if we have at least 1,000 valid entries
if len(df_valid) < 1000:
    raise ValueError("Not enough valid galaxies after filtering. Increase the initial sample size.")
