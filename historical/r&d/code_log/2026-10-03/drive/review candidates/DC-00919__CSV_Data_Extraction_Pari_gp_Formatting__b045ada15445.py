nan_count = df['logmass'].isna().sum()
total_rows = len(df)
print(f"Number of NaN values in logmass: {nan_count} out of {total_rows} rows ({nan_count/total_rows*100:.2f}%)")
