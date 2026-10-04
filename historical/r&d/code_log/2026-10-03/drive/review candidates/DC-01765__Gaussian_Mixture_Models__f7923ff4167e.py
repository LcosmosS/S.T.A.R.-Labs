df = df.dropna(subset=columns_to_filter)
df = df[(df[columns_to_filter] != -9999).all(axis=1)]
print(f"Number of valid rows after filtering for GMM: {len(df)}")
