from qflac import QFLaC


# Load the CSV
q = QFLaC.from_csv('pipe3d_data.csv')


# Preview available flags (automatically detected, if included)
print(q.flags)  # Might detect e.g., 'flag_SFR', 'flag_metallicity', etc.


# Apply default quality cuts (customizable)
q.clean(auto=True)


# Now get the cleaned DataFrame
clean_df = q.df_clean


# For example, subset for SFR modeling
features = ['log_Mass_gas', 'OH_O3N2_cen', 'Av_gas_Re']
target = 'log_SFR_Ha'
model_data = clean_df[features + [target]].dropna()
