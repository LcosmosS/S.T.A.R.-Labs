# Step 4: Derive the SFR Formula # SFR = f(M, z) * g(L(s=1)), inspired by BSD's link between L-function and rank
def predict_sfr(logmass, z, l_value, order): """ SFR prediction formula: - Order=1: SFR = a * logmass + b * z + c * l_value - Order=2: SFR = a * logmass + b * z + c * l_value + d * l_value^2 Coefficients are placeholders; optimize them for your data. """ a, b, c, d = 1.0, 0.5, 0.1, 0.05 # Example coefficients if order == 1: return a * logmass + b * z + c * l_value else: return a * logmass + b * z + c * l_value + d * l_value**2
# Apply the SFR formula to the dataset
df['predicted_sfr'] = predict_sfr(df['logmass'], df['z'], l_1, order)
# Step 5: Cross-Validation for Model Evaluation
k = 5 kf = KFold(n_splits=k, shuffle=True, random_state=42) mse_list = []
