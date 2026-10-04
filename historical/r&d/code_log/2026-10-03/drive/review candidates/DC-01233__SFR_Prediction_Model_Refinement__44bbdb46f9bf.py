# Check for duplicate columns
print(merged_df.columns)


# You can rename columns if necessary, for example:
merged_df.rename(columns={'recno_x': 'recno_from_file1', 'recno_y': 'recno_from_file2'}, inplace=True)
