if missing_cols:
    print(f"Warning: Missing key columns after merge: {missing_cols}")
else:
    print("All key columns present after merge.")
print(f"Sample data:\n{df[key_columns].head() if not missing_cols else df.head()}")

# Downcast numeric columns to save memory
========================================================================
=======================================================
def downcast_df(df):
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    return df
df = downcast_df(df)
print(f"Memory usage after downcast: {df.memory_usage().sum() / 1024**2:.2f} MB")

# Ensure RA/Dec are numeric and impute NaN/infinities with medians
========================================================================
========================================================================
==========================
df['objra_y'] = pd.to_numeric(df['objra_y'], errors='coerce')
df['objdec'] = pd.to_numeric(df['objdec'], errors='coerce')
print(f"Initial df: objra_y dtype: {df['objra_y'].dtype}, objdec dtype: {df['objdec'].dtype}")
print(f"NaN in objra_y: {df['objra_y'].isna().sum()}, NaN in objdec: {df['objdec'].isna().sum()}")
df['objra_y'] = df['objra_y'].replace([np.inf, -np.inf],
np.nan).fillna(df['objra_y'].median(skipna=True))
df['objdec'] = df['objdec'].replace([np.inf, -np.inf], np.nan).fillna(df['objdec'].median(skipna=True))
print(f"Rows after RA/Dec imputation: {len(df)}")

# Impute NaN/infinities for all numeric columns
========================================================================
====================================================
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    df[col] = df[col].replace([np.inf, -np.inf], np.nan).fillna(df[col].median(skipna=True))

# Recompute log_SFR_Ha and metallicity
========================================================================
==============================================================
flux_cols = ['flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']
for col in flux_cols:
    print(f"NaN count in {col} after imputation: {df[col].isna().sum()}")