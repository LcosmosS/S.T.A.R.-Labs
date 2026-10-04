logmass = df['logmass']
z = df['z']
features = pd.DataFrame({
    'logmass': logmass,
    'z': z,
    'logmass2': logmass**2,           # Non-linear term
    'z2': z**2,                       # Non-linear term
    'logmass_z': logmass * z,         # Interaction term
    'quenching': np.maximum(logmass - high_mass_threshold, 0),  # High-mass adjustment
    'low_mass': (logmass < low_mass_threshold).astype(int) * logmass  # Low-mass adjustment
})


# Include additional features if present
for feat in additional_features:
    if feat in df.columns:
        features[feat] = df[feat]


return features
def plot_diagnostics(fold, test_df, test_pred, mse): """ Generate diagnostic plots for each fold.
