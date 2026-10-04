import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


# Load data
df = pd.read_csv("Stellar_Mass2_Table_cleaned.csv")
print("Loaded data successfully.")


# Define column names
logmass_col = 'logmass'  # Logarithmic stellar mass
z_col = 'z'              # Redshift
sfr_col = 'sfr'          # Star formation rate


# Check for missing values and impute with mean
for col in [logmass_col, z_col, sfr_col]:
    if df[col].isnull().any():
        print(f"Warning: Missing values in {col}. Imputing with mean.")
        df[col].fillna(df[col].mean(), inplace=True)


# Explore Trends: Plot logmass vs. SFR and z vs. SFR
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.scatter(df[logmass_col], df[sfr_col], alpha=0.5)
plt.xlabel('logmass')
plt.ylabel('sfr')
plt.title('logmass vs. SFR')


plt.subplot(1, 2, 2)
plt.scatter(df[z_col], df[sfr_col], alpha=0.5)
plt.xlabel('z')
plt.ylabel('sfr')
plt.title('z vs. SFR')


plt.tight_layout()
plt.show()


# Group Analysis: If 'group' column exists, analyze group properties
if 'group' in df.columns:
    group_stats = df.groupby('group').agg({
        logmass_col: ['mean', 'median', 'std'],
        z_col: ['mean', 'median', 'std'],
