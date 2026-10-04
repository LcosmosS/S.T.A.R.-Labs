import pandas as pd
import numpy as np


# Define target and key feature columns based on importance
target_column = 'log_SFR_Ha'
feature_columns = [
    'log_Mass_gas',
    'nsa_mstar',
    'log_Mass',
    'V-band_SB_at_Re',
    'vel_sigma_Re',
    # Add other important features as needed, e.g., 'OH_Mar13_N2_Re_fit' for metallicity
]


# Columns to check for invalid values
columns_to_check = [target_column] + feature_columns


# Load the dataset
df = pd.read_csv('filtered_Pipe3D.csv')  # Replace with your file name
print(f"Original dataset shape: {df.shape}")


# Replace sentinel values (-9999) with NaN in key columns
df[columns_to_check] = df[columns_to_check].replace(-9999, np.nan)


# Remove rows with NaN in key columns
df_filtered = df.dropna(subset=columns_to_check)
print(f"Filtered dataset shape after removing NaN: {df_filtered.shape}")


# Optional: Check for negative fluxes if used (example for flux columns)
