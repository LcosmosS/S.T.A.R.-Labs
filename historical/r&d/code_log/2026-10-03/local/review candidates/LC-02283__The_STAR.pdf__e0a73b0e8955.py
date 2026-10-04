            merge_keys = ['SpecObj']
        # Fall back to objid if available in both datasets
        elif 'objid' in df.columns and 'objid' in merged_df.columns:
            merge_keys = ['objid']

        if merge_keys:
            print(f"Merging {file} on {merge_keys}")
            merged_df = merged_df.merge(df, on=merge_keys, how='left', suffixes=('', f'_dup_{i}'))
            dup_cols = [col for col in merged_df.columns if f'_dup_{i}' in col]
            merged_df = merged_df.drop(columns=dup_cols)
        else:
            print(f"Skipping merge for {file}: No common merge keys found")
            continue

    if 'objra_y' in merged_df.columns and 'objdec' in merged_df.columns:
        merged_df = merged_df.drop_duplicates(subset=['objra_y', 'objdec'], keep='first')