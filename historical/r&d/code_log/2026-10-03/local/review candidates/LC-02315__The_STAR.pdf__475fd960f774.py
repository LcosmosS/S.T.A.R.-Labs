for col in key_features:
    if col in df.columns:
        nan_count = df[col].isna().sum()
        inf_count = np.isinf(df[col]).sum()
        mean_val = df[col].mean()
        median_val = df[col].median()
        std_val = df[col].std()
        min_val = df[col].min()
        max_val = df[col].max()
        sample_vals = df[col].iloc[:5].tolist()
        print(f"{col}: NaN = {nan_count}, Inf = {inf_count}, Mean = {mean_val:.4f}, Median =
