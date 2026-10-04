def cross_match_in_chunks(df1, filepath, ra_col1, dec_col1, ra_col2, dec_col2, columns_to_keep, max_dist_arcsec=10.0, chunksize=100000):
    try:
        # Filter df1 by RA/Dec range
        min_ra, max_ra = df1[ra_col1].min() - 0.1, df1[ra_col1].max() + 0.1
        min_dec, max_dec = df1[dec_col1].min() - 0.1, df1[dec_col1].max() + 0.1


        # Initialize lists to store matched DataFrames
        matched_df1_list = []
        matched_df2_list = []
        
        # Read the CSV file in chunks, skipping bad lines
        chunk_reader = pd.read_csv(
            filepath, 
            chunksize=chunksize, 
            error_bad_lines=False,  # Skip rows with too many/few fields
            warn_bad_lines=True     # Print warnings for skipped rows
        )
        for i, chunk in enumerate(chunk_reader):
            print(f"Processing chunk {i+1} with {len(chunk)} rows...")
            # Filter chunk by RA/Dec range
            chunk_filtered = chunk[
                (chunk[ra_col2] >= min_ra) & (chunk[ra_col2] <= max_ra) &
                (chunk[dec_col2] >= min_dec) & (chunk[dec_col2] <= max_dec)
