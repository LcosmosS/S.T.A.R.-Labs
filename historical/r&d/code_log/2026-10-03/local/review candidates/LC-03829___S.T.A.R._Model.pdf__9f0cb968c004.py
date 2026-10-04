    else:
        print(f"No valid RA/Dec data after cleaning in {ra_col}/{dec_col}")
    return df_cleaned

# Cross-match function
def deg_to_rad(df, ra_col, dec_col):
    try:
        df['ra_rad'] = np.radians(df[ra_col])
        df['dec_rad'] = np.radians(df[dec_col])
        return df
    except KeyError as e:
        print(f"KeyError in deg_to_rad: {e}")
        print(f"Available columns in DataFrame: {df.columns.tolist()}")
        raise

def cross_match(df1, df2, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec=10.0):
    try:
        # Clean DataFrames to remove rows with NaN or inf in RA/Dec
        df1_cleaned = clean_coordinates(df1, ra_col1, dec_col1)
        df2_cleaned = clean_coordinates(df2, ra_col2, dec_col2)

        # Check if either DataFrame is empty after cleaning
        if len(df1_cleaned) == 0 or len(df2_cleaned) == 0:
            print("One of the DataFrames is empty after cleaning. Cannot perform cross-match.")
            return df1_cleaned, pd.DataFrame()

        # Convert degrees to radians
        df1_cleaned = deg_to_rad(df1_cleaned, ra_col1, dec_col1)
        df2_cleaned = deg_to_rad(df2_cleaned, ra_col2, dec_col2)

        # Create coordinate arrays
