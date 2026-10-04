nan_count = df['logmass'].isna().sum()
print(f"Number of NaN values in logmass: {nan_count}")
