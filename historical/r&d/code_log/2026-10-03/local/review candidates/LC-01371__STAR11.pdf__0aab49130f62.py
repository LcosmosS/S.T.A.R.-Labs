    temp_file = f"temp_merge_step_{i+1}.csv"
    merged_df.to_csv(temp_file, index=False)
    print(f"Saved to {temp_file}")

# Final assignment and save after all merges
=========================================================================================
=================================
df = merged_df
df.to_csv("*STAR_preprocess.csv", index=False)
print(f"Completed merging. Final rows: {len(df)}, columns: {len(df.columns)}. Saved to *STAR_preprocess.csv")
print("Preprocessing completed. Engineering features...")

# Clean metallicity and sfr columns by replacing -9999 with NaN
=========================================================================================
==============
df[['metallicity', 'sfr']] = df[['metallicity', 'sfr']].replace(-9999, np.nan)
print(f"Replaced -9999 with NaN in 'metallicity' and 'sfr' columns.")
print(f"NaN in metallicity: {df['metallicity'].isna().sum()}, NaN in sfr: {df['sfr'].isna().sum()}")

# Merge Diagnostics
=========================================================================================
==========================================================
key_columns = ['objra_y', 'objdec', 'zsp', 'flux_Ha', 'logmass', 'petrorad_r']
missing_cols = [col for col in key_columns if col not in df.columns]
if missing_cols:
    print(f"Warning: Missing key columns after merge: {missing_cols}")
else:
    print("All key columns present after merge.")
print(f"Sample data:\n{df[key_columns].head() if not missing_cols else df.head()}")

# Downcast numeric columns to save memory
=========================================================================================
====================================
def downcast_df(df):
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    return df
df = downcast_df(df)
print(f"Memory usage after downcast: {df.memory_usage().sum() / 1024**2:.2f} MB")

# Ensure RA/Dec are numeric and impute NaN/infinities with medians
=========================================================================================
===========