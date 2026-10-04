import pandas as pd
import numpy as np


# Define the relevant columns to keep
columns_to_keep = [
    'log_Mass',
    'nsa_z',
    'Re_kpc',
    'ellip',
    'log_Mass_gas',
    'OH_Mar13_N2_Re_fit',
    'vel_disp_ssp_1Re',
    'u-g',
    'g-r',
    'V-band_SB_at_Re',
    'zcomp_1Mpc',
    'SFR_PETRORAD_R'
]


# Load the CSV file
df = pd.read_csv('Pipe3D.csv')
print(f"Initial number of rows: {len(df)}")


# Verify all required columns are present
missing_cols = [col for col in columns_to_keep if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing columns: {missing_cols}")


# Select only the specified columns
df = df[columns_to_keep]


# Replace -9999.0 with NaN and drop rows with any NaN in these columns
df = df.replace(-9999.0, np.nan)
initial_rows = len(df)
df = df.dropna()
removed_due_to_nan = initial_rows - len(df)
print(f"Removed {removed_due_to_nan} rows due to NaN or -9999.0")
print(f"Rows after NaN removal: {len(df)}")


# Apply IQR-based outlier removal to SFR_PETRORAD_R
Q1 = df['SFR_PETRORAD_R'].quantile(0.25)
Q3 = df['SFR_PETRORAD_R'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 3 * IQR
upper_bound = Q3 + 3 * IQR
mask = (df['SFR_PETRORAD_R'] >= lower_bound) & (df['SFR_PETRORAD_R'] <= upper_bound)
rows_before_outlier_removal = len(df)
df = df[mask]
removed_due_to_outliers = rows_before_outlier_removal - len(df)
print(f"Removed {removed_due_to_outliers} rows due to outliers in SFR_PETRORAD_R")
print(f"Final number of rows: {len(df)}")


# Save the filtered data to a new CSV file
df.to_csv('filtered_Pipe3D.csv', index=False)
print("Filtered data saved to 'filtered_Pipe3D.csv'")
