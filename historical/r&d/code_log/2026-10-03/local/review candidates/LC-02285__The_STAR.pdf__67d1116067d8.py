print("Preprocessing completed. Engineering features...")

# Clean metallicity and sfr columns by replacing -9999 with NaN
columns_to_clean = ['metallicity', 'sfr']
existing_columns = [col for col in columns_to_clean if col in df.columns]
if existing_columns:
    df[existing_columns] = df[existing_columns].replace(-9999, np.nan)
    print(f"Replaced -9999 with NaN in {existing_columns} columns.")

# Impute NaN with medians for all numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    if df[col].isna().any():
        median_val = df[col].median(skipna=True)
        if pd.isna(median_val):
