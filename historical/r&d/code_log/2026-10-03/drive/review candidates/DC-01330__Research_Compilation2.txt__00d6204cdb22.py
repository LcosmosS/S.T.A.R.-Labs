import pandas as pd


# Load the dataset
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Filter out invalid logmass values
df = df[df['logmass'] != -9999]


# Calculate the median logmass
median_logmass = df['logmass'].median()


# Compute M0
M0 = 10 ** median_logmass
print(f"Reference Mass M0: {M0:.2e} solar masses")
