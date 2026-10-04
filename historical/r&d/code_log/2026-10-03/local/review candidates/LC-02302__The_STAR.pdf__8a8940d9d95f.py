            try:
                bins = pd.cut(df['kronRad'], bins=20, labels=False, duplicates='drop') + 1
                df['z_bin'] = bins
                n_bins = df['z_bin'].nunique()
                print(f"Number of unique bins (cut): {n_bins}")
                print("Bin distribution for kronRad (cut):")
                print(df['z_bin'].value_counts().sort_index())
            except Exception as e:
                print(f"Warning: pd.cut also failed due to {e}. Using median-based fallback.")
                df['z_bin'] = (df['kronRad'] > df['kronRad'].median()).astype(int) + 1  # Binary split
                n_bins = df['z_bin'].nunique()
                print(f"Number of unique bins (fallback): {n_bins}")
                print("Bin distribution for kronRad (fallback):")
                print(df['z_bin'].value_counts().sort_index())

# ======== Ensure a minimum number of bins
