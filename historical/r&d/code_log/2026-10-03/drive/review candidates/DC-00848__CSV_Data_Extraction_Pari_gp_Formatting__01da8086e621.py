if missing_columns:
    print(f"Error: The following columns are missing in the CSV file: {missing_columns}")
    exit(1)


# Filter out rows with NaN or -9999.0 in key columns
valid_df = df[df[key_columns].notna().all(axis=1) & (df[key_columns] != -9999.0).all(axis=1)]


# Check if 'objid' exists for PARI/GP export (optional, as it's not used in computations)
if 'objid' not in df.columns:
