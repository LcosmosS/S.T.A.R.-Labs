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
