import pandas as pd


# Load your dataset into a DataFrame
df = pd.read_csv('galaxy_data.csv')  # Replace with your actual file name


# Filter the DataFrame to get logmass values where groups == 1 (Group 2)
logmass_group2 = df[df['groups'] == 1]['logmass']


# Convert to a NumPy array if needed and check what we got
logmass_group2 = logmass_group2.values
print(f"Number of galaxies in Group 2: {len(logmass_group2)}")
print(f"Sample logmass values: {logmass_group2[:5]}")
