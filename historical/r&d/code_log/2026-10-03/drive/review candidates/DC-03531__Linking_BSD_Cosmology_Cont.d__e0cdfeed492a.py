rows_before_outlier_removal = len(df)
df = df[mask]
removed_due_to_outliers = rows_before_outlier_removal - len(df)
print(f"Removed {removed_due_to_outliers} rows due to outliers in SFR_PETRORAD_R")
