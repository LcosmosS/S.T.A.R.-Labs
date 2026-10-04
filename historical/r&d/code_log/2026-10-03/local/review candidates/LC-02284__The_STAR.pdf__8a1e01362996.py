    elif 'SpecObj' in merged_df.columns:
        merged_df = merged_df.drop_duplicates(subset=['SpecObj'], keep='first')
    print(f"Rows after merging {file}: {len(merged_df)}")
    temp_file = f"temp_merge_step_{i+1}.csv"
    merged_df.to_csv(temp_file, index=False)
    print(f"Saved to {temp_file}")

# Final assignment and save after all merges
df = merged_df
df.to_csv("*STAR_preprocess.csv", index=False)
print(f"Completed merging. Final rows: {len(df)}, columns: {len(df.columns)}. Saved to
