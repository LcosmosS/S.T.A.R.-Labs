if missing_cols:
    raise ValueError(f"Missing columns: {missing_cols}")


# Select only the specified columns
df = df[columns_to_keep]


# Replace -9999.0 with NaN
df = df.replace(-9999.0, np.nan)


# Drop rows with any NaN in the selected columns
initial_rows = len(df)
df = df.dropna()
removed_due_to_nan = initial_rows - len(df)
print(f"Removed {removed_due_to_nan} rows due to NaN or -9999.0")


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


# Save the filtered data to a new CSV file
df.to_csv('filtered_Pipe3D.csv', index=False)
print("Filtered data saved to 'filtered_Pipe3D.csv'")
