if missing_cols:
    raise ValueError(f"Missing columns: {missing_cols}")


# Select only the relevant columns
df = df[columns_to_keep]


# Handle missing values
# Remove rows with missing target variable
initial_rows = len(df)
df = df.dropna(subset=['log_SFR_Ha'])
print(f"Removed {initial_rows - len(df)} rows with missing target variable")


# Impute missing values in feature columns with median
for col in columns_to_keep[1:]:  # Exclude target
    if df[col].isnull().any():
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"Imputed missing values in '{col}' with median: {median_val}")


# Remove invalid entries (e.g., negative values where not plausible)
# Assuming masses, sizes, and similar should be positive
for col in ['log_Mass', 'log_Mass_gas', 'Re_kpc', 'vel_disp_ssp_1Re', 'vel_sigma_Re', 'V-band_SB_at_Re']:
    if (df[col] < 0).any():
        invalid_rows = df[df[col] < 0]
        df = df[df[col] >= 0]
        print(f"Removed {len(invalid_rows)} rows with negative values in '{col}'")


# Apply IQR-based outlier removal to the target variable 'log_SFR_Ha'
Q1 = df['log_SFR_Ha'].quantile(0.25)
Q3 = df['log_SFR_Ha'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 3 * IQR
upper_bound = Q3 + 3 * IQR
outlier_mask = (df['log_SFR_Ha'] >= lower_bound) & (df['log_SFR_Ha'] <= upper_bound)
rows_before_outlier_removal = len(df)
df = df[outlier_mask]
print(f"Removed {rows_before_outlier_removal - len(df)} rows due to outliers in 'log_SFR_Ha'")


# Final check for any remaining invalid entries
# For example, ensure no infinite values
for col in columns_to_keep:
    if np.isinf(df[col]).any():
        print(f"Warning: Infinite values found in '{col}'")


# Save the filtered dataset
df.to_csv('filtered_Pipe3D.csv', index=False)
print(f"Filtered dataset saved to 'filtered_Pipe3D.csv' with {len(df)} rows")
