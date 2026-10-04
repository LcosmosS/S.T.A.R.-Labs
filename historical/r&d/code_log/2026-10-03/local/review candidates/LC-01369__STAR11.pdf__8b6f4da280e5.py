def standardize_columns(df, cols):
    df = df[cols].copy()
    if 'RA_ICRS' in df.columns and 'DE_ICRS' in df.columns:
        df = df.rename(columns={"RA_ICRS": "objra_y", "DE_ICRS": "objdec"})
    elif 'ra' in df.columns and 'dec' in df.columns:
        df = df.rename(columns={"ra": "objra_y", "dec": "objdec"})
    return df

# Incremental merge
=========================================================================================
=============================================================================
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
