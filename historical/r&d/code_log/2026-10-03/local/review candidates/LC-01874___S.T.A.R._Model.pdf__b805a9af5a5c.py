# Drop the intermediate columns
sdss_merged = sdss_merged[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag',
'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']]

# Save the merged dataset for future use
sdss_merged.to_csv("sdss_merged.csv", index=False)
print(f"Merged SDSS dataset created with {len(sdss_merged)} rows.")

# Load the other datasets
twomass = pd.read_csv("2Mass.csv")  # II/246: 2MASS Extended Source Catalogue
gama = pd.read_csv("II356xmmom41s.csv")  # II/356: GAMA DR3

# Print columns for debugging
print("Columns in merged_data.csv:", df.columns.tolist())
print("Columns in sdss_merged (V/147 + V/154):", sdss_merged.columns.tolist())
print("Columns in twomass (II/246):", twomass.columns.tolist())
print("Columns in gama (II/356):", gama.columns.tolist())

# Function to clean DataFrame by removing rows with NaN or inf in RA/Dec columns
def clean_coordinates(df, ra_col, dec_col):
    initial_len = len(df)