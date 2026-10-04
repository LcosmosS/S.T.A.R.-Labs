import pandas as pd


# Read the CSV file
df = pd.read_csv('Stellar_Mass2_Table.csv')


# Extract the 'logmass' column (assumed to be in log10 solar masses)
logmasses = df['logmass']


# Convert to linear masses, filtering out invalid entries (e.g., -9999)
masses = [10**lm for lm in logmasses if lm != -9999]


# Write masses to masses.txt, one per line
with open('masses.txt', 'w') as f:
    for m in masses:
        f.write(str(m) + '\n')
