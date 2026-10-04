import pandas as pd
import numpy as np


# Define key columns to check for invalid values, including target and specified features
key_columns = [
    'log_SFR_Ha',         # Target variable
    'log_Mass_gas',       # Important feature
    'nsa_mstar',          # Stellar mass
    'log_Mass',           # Another mass indicator
    'OH_Mar13_N2_Re_fit', # Metallicity indicator for model testing
    'Av_gas_Re'           # Dust attenuation for model testing
]


# Load the dataset
df = pd.read_csv('pipe3d_data.csv')
print(f"Original dataset shape: {df.shape}")


# Replace sentinel values (-9999) with NaN in key columns
df[key_columns] = df[key_columns].replace(-9999, np.nan)


# Drop rows with NaN in key columns
df_filtered = df.dropna(subset=key_columns)
print(f"Filtered dataset shape after removing NaN in key columns: {df_filtered.shape}")


# Optionally, filter based on QCFLAG if present, assuming 1 indicates valid data
if 'QCFLAG' in df.columns:
    df_filtered = df_filtered[df_filtered['QCFLAG'] == 1]
    print(f"Filtered dataset shape after QCFLAG filtering: {df_filtered.shape}")


# Save the filtered dataset
df_filtered.to_csv('filtered_pipe3d_data.csv', index=False)
print("Filtered dataset saved to 'filtered_pipe3d_data.csv'")
