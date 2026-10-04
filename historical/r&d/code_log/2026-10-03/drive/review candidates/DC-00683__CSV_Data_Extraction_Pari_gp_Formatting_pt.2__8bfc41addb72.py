# Step 4: Derive the SFR Formula with Additional Factors
def predict_sfr(logmass, z, l_value, order, petrorad_r=0, environment=0): """ SFR prediction formula with additional physical factors: - Order=1: SFR = a * logmass + b * z + c * l_value + d * petrorad_r + e * environment - Order=2: SFR = a * logmass + b * z + c * l_value + d * l_value^2 + e * petrorad_r + f * environment Coefficients will be optimized via regression. """ return [logmass, z, l_value, l_value**2 if order == 2 else 0, petrorad_r, environment]
# Prepare features for regression (to optimize coefficients)
features = ['logmass', 'z', 'l_value', 'l_value2', 'petrorad_r', 'environment'] df['l_value'] = l_1 df['l_value2'] = l_1**2 if order == 2 else 0 X = np.array([predict_sfr(row['logmass'], row['z'], l_1, order, row['petrorad_r'], row['environment']) for _, row in df.iterrows()]) y = df['sfr'].values
# Step 5: Cross-Validation with Optimized Coefficients
k = 5 kf = KFold(n_splits=k, shuffle=True, random_state=42) mse_list = []
