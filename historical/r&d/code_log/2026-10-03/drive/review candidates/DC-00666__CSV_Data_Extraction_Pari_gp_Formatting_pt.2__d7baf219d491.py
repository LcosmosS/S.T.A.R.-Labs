# Define the SFR formula
def predict_sfr(logmass, z, l_value):
    # Example: SFR = a * logmass + b * z + c * l_value
    a, b, c = 1.0, 0.5, 0.1  # Arbitrary coefficients; replace with actual values
    return a * logmass + b * z + c * l_value


# Compute predicted SFR
df['predicted_sfr'] = predict_sfr(df['logmass'], df['z'], l_1)
