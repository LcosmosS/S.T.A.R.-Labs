# Function to standardize RA/Dec =======================================================================================================================================================================
def standardize_columns(df, cols):
    df = df[cols].copy()
    if 'RA_ICRS' in df.columns and 'DE_ICRS' in df.columns:
        df = df.rename(columns={"RA_ICRS": "objra_y", "DE_ICRS": "objdec"})
    elif 'ra' in df.columns and 'dec' in df.columns:
        df = df.rename(columns={"ra": "objra_y", "dec": "objdec"})
    return df


# Incremental merge ======================================================================================================================================================================
print("Merging Datasets...")
merged_df = None
for i, file in tqdm(enumerate(csv_files), total=len(csv_files), desc="Merging CSV Files"):
    print(f"Loading {file} ({i+1}/{len(csv_files)})...")
    try:
        chunksize = 50000
        df_chunks = pd.read_csv(file, usecols=column_mappings[file], chunksize=chunksize)
        df = pd.concat([standardize_columns(chunk, column_mappings[file]) for chunk in df_chunks], ignore_index=True)
        print(f"Rows in {file}: {len(df)}, Columns: {len(df.columns)}")
        if 'objid' in df.columns:
            print(f"objid present in {file}")
        else:
            print(f"No objid in {file}")
    except ValueError as e:
        print(f"Error loading {file}: {e}. Check column names.")
        continue
    
    if merged_df is None:
        merged_df = df
    else:
        merge_keys = ['objra_y', 'objdec']
        if 'objid' in merged_df.columns and 'objid' in df.columns:
            merge_keys.append('objid')
        merged_df = merged_df.merge(df, on=merge_keys, how='left', suffixes=('', f'_dup_{i}'))
        dup_cols = [col for col in merged_df.columns if f'_dup_{i}' in col]
        merged_df = merged_df.drop(columns=dup_cols)
    
    merged_df = merged_df.drop_duplicates(subset=['objra_y', 'objdec'], keep='first')
    print(f"Rows after merging {file}: {len(merged_df)}")
# - Save intermediate result per file --------------------------------------------------------------------------------------------------------------------------------
    temp_file = f"temp_merge_step_{i+1}.csv"
    merged_df.to_csv(temp_file, index=False)
    print(f"Saved to {temp_file}")


# Final assignment and save after all merges ==========================================================================================================================
df = merged_df
df.to_csv("*STAR_preprocess.csv", index=False)
print(f"Completed merging. Final rows: {len(df)}, columns: {len(df.columns)}. Saved to *STAR_preprocess.csv")
print("Preprocessing completed. Engineering features...")


# Clean metallicity and sfr columns by replacing -9999 with NaN =======================================================================================================
df[['metallicity', 'sfr']] = df[['metallicity', 'sfr']].replace(-9999, np.nan)
print(f"Replaced -9999 with NaN in 'metallicity' and 'sfr' columns.")
print(f"NaN in metallicity: {df['metallicity'].isna().sum()}, NaN in sfr: {df['sfr'].isna().sum()}")


# Merge Diagnostics ===================================================================================================================================================
key_columns = ['objra_y', 'objdec', 'zsp', 'flux_Ha', 'logmass', 'petrorad_r']
