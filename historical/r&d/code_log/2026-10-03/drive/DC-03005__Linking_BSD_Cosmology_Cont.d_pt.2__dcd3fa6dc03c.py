import pandas as pd import numpy as np
# Define the relevant columns (including optional ones)
columns_to_keep = [ 'log_SFR_Ha', # Target variable 'log_Mass', 'nsa_redshift', 'log_Mass_gas', 'OH_Mar13_N2_Re_fit', 'Re_kpc', 'ellip', 'vel_disp_ssp_1Re', 'u-g', 'g-r', 'r-i', 'i-z', 'nsa_mstar', 'vel_sigma_Re', 'V-band_SB_at_Re', 'Lambda_Re' ]
# Load the dataset
df = pd.read_csv('Pipe3D.csv') print(f"Initial number of rows: {len(df)}")
# Check if all required columns are present
missing_cols = [col for col in columns_to_keep if col not in df.columns] if missing_cols: raise ValueError(f"Missing columns: {missing_cols}")
# Select only the relevant columns
df = df[columns_to_keep]
# Handle missing values # Remove rows with missing target variable
initial_rows = len(df) df = df.dropna(subset=['log_SFR_Ha']) print(f"Removed {initial_rows - len(df)} rows with missing target variable")
# Impute missing values in feature columns with median
for col in columns_to_keep[1:]: # Exclude target if df[col].isnull().any(): median_val = df[col].median() df[col] = df[col].fillna(median_val) print(f"Imputed missing values in '{col}' with median: {median_val}")
# Remove invalid entries (e.g., negative values where not plausible) # Assuming masses, sizes, and similar should be positive
