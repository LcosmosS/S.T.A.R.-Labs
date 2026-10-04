initial_rows = len(df)
df = df.dropna()
removed_due_to_nan = initial_rows - len(df)
print(f"Removed {removed_due_to_nan} rows due to NaN or -9999.0")
