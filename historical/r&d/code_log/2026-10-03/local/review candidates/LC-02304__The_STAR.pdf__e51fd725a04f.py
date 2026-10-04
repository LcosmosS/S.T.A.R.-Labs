            n_bins = df['z_bin'].nunique()
            print(f"Adjusted number of unique bins: {n_bins}")
            print("Adjusted bin distribution for kronRad:")
            print(df['z_bin'].value_counts().sort_index())

# ======== Compute L_cosmo_s_* features
