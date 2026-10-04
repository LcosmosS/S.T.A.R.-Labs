import pandas as pd


# Load the CSV
df = pd.read_csv("Stellar_Mass2_Table.csv")


# Filter out invalid logmass values
df_valid = df[df['logmass'] != -9999]


# Extract logmass and z
logmass = df_valid['logmass'].tolist()
z = df_valid['z'].tolist()


# Format as PARI/GP vectors (print to copy-paste)
print("log_mass = [", ", ".join(map(str, logmass)), "];")
print("z = [", ", ".join(map(str, z)), "];")
