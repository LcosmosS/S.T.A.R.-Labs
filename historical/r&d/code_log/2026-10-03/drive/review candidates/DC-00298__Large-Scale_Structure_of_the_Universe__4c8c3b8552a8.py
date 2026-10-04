print(f"Found flux columns: {flux_columns}")


# If we find any flux columns, we can use the first one found for SFR calculation
if flux_columns:
    flux_col = flux_columns[0]  # Take the first one found
    df1['SFR'] = df1[flux_col] / (1.26e-41)  # SFR in solar masses per year
    print(f"SFR column successfully created from {flux_col}.")
else:
    print("No 'fS' column found. Cannot calculate SFR.")
    # Skip calculation and handle this case if needed


# --- Check for necessary columns and handle suffixes ---
# Rename RAJ2000 to ra, DEJ2000 to dec, and z to redshift
if 'RAJ2000' in df1.columns:
    df1.rename(columns={'RAJ2000': 'ra'}, inplace=True)
if 'DEJ2000' in df1.columns:
    df1.rename(columns={'DEJ2000': 'dec'}, inplace=True)
if 'z' in df1.columns:
    df1.rename(columns={'z': 'redshift'}, inplace=True)


# Ensure 'SFR' is available as the target (we just calculated it above)
if 'SFR' in df1.columns:
    # Step 2: Impute missing values with the mean or median
    imputer = SimpleImputer(strategy='mean')  # You can change to 'median' if desired
    
    # Impute missing values in all numerical columns
