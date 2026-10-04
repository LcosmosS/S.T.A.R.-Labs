# Step 4: Derive the SFR Formula with Additional Factors
def predict_sfr_features(logmass, z, l_value, order, dec=0, petrorad_r=0): """ Generate features for SFR prediction: - Order=1: [logmass, z, l_value, dec, petrorad_r] - Order=2: [logmass, z, l_value, l_value^2, dec, petrorad_r] Coefficients will be optimized via regression. """ features = [logmass, z, l_value, dec, petrorad_r] if order == 2: features.insert(3, l_value**2) # Add l_value^2 for order 2 return features
# Prepare features for regression
features = ['logmass', 'z', 'l_value', 'l_value2', 'dec', 'petrorad_r'] df['l_value'] = l_1 df['l_value2'] = l_1**2 if order == 2 else 0 X = np.array([predict_sfr_features(row['logmass'], row['z'], l_1, order, row['dec'], row['petrorad_r']) for _, row in df.iterrows()]) y = df['sfr'].values
# Step 5: Cross-Validation with Optimized Coefficients
k = 5 kf = KFold(n_splits=k, shuffle=True, random_state=42) mse_list = []
