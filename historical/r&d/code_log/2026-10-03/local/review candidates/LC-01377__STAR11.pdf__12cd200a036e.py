    df['cosmo_rank'] = 0.5 * gz_df['Num_w_norm'] + 0.3 * gz_df['morph_norm'] + 0.2 * gz_df['redshift_norm']
    print("Computed cosmo_rank using ellipticity and redshift proxies.")
else:
    print("Warning: ellipticity or redshift missing. Setting cosmo_rank to 0.5.")
    df['cosmo_rank'] = 0.5

# Ensure cosmo_rank is numeric and imputed
=========================================================================================
===================================
df['cosmo_rank'] = pd.to_numeric(df['cosmo_rank'], errors='coerce').replace([np.inf, -np.inf], np.nan).fillna(0.5)
