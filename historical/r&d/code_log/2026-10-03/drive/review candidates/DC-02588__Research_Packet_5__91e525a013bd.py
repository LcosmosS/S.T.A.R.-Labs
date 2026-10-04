def replace_nan_with_median(df, ra_col, dec_col):
    # Replace NaN with median
    df[ra_col] = df[ra_col].fillna(df[ra_col].median())
    df[dec_col] = df[dec_col].fillna(df[dec_col].median())
    # Replace inf with median
    df[ra_col] = df[ra_col].replace([np.inf, -np.inf], df[ra_col].median())
    df[dec_col] = df[dec_col].replace([np.inf, -np.inf], df[dec_col].median())
    return df
