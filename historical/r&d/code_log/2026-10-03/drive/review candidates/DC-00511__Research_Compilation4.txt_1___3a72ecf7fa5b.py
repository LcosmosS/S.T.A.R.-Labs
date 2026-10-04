import pandas as pd


# Load the first 1,250 rows
df = pd.read_csv("Stellar_Mass2_Table.csv", nrows=1250)


# Filter out invalid logmass
df_valid = df[df['logmass'] != -9999]


# Select the first 1,000 valid entries
df_valid_1000 = df_valid.head(1000)


# Extract logmass and z
logmass = df_valid_1000['logmass'].tolist()
z = df_valid_1000['z'].tolist()


# Format for PARI/GP
print("log_mass = [", ", ".join(map(str, logmass)), "];")
print("z = [", ", ".join(map(str, z)), "];")
