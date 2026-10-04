import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


# Load the data
df = pd.read_csv("Stellar_Mass2_Table_cleaned.csv")
print("Loaded data successfully.")


# Define column names for readability
logmass_col = 'logmass'  # Logarithmic stellar mass
z_col = 'z'              # Redshift
sfr_col = 'sfr'          # Star formation rate


# Handle missing values by imputing with the mean
for col in [logmass_col, z_col, sfr_col]:
    if df[col].isnull().any():
        print(f"Warning: Missing values in {col}. Imputing with mean.")
        df[col].fillna(df[col].mean(), inplace=True)


# Step 1: Explore Trends
# Plot logmass vs. SFR and z vs. SFR to identify patterns
plt.figure(figsize=(10, 5))


plt.subplot(1, 2, 1)
plt.scatter(df[logmass_col], df[sfr_col], alpha=0.5)
plt.xlabel('Log Stellar Mass')
plt.ylabel('Star Formation Rate')
plt.title('Logmass vs. SFR')


plt.subplot(1, 2, 2)
plt.scatter(df[z_col], df[sfr_col], alpha=0.5)
plt.xlabel('Redshift (z)')
plt.ylabel('Star Formation Rate')
plt.title('z vs. SFR')


plt.tight_layout()
plt.show()


# Step 2: Group Analysis
# Analyze properties of galaxy groups if 'group' column exists
if 'group' in df.columns:
    group_stats = df.groupby('group').agg({
        logmass_col: ['mean', 'median', 'std'],
        z_col: ['mean', 'median', 'std'],
