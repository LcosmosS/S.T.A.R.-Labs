# Step 4: Derive the SFR Formula
def predict_sfr(logmass, z, l_value, order, metallicity=0, environment=0): """ SFR prediction formula with additional features: - Order=1: SFR = a * logmass + b * z + c * l_value + d * metallicity + e * environment - Order=2: SFR = a * logmass + b * z + c * l_value + d * l_value^2 + e * metallicity + f * environment """ a, b, c, d, e, f = 1.0, 0.5, 0.1, 0.05, 0.2, 0.1 # Example coefficients if order == 1: return a * logmass + b * z + c * l_value + d * metallicity + e * environment else: return a * logmass + b * z + c * l_value + d * l_value**2 + e * metallicity + f * environment
# Apply the SFR formula
df['predicted_sfr'] = df.apply(lambda row: predict_sfr(row['logmass'], row['z'], l_1, order, row['metallicity'], row['environment']), axis=1)
# Step 5: Cross-Validation
k = 5 kf = KFold(n_splits=k, shuffle=True, random_state=42) mse_list = []
# Features for cross-validation (extendable)
features = ['logmass', 'z'] if 'metallicity' in df.columns and df['metallicity'].sum() != 0: features.append('metallicity') if 'environment' in df.columns and df['environment'].sum() != 0: features.append('environment')
