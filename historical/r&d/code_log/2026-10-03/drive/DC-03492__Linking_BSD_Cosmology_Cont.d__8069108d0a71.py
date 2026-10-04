def predict_sfr_features(row, l_value, order):
    features = [row['logmass'], row['z'], l_value, row['dec'], row['petrorad_r'], row['environment'], 
                row['logmass'] * row['z'], row['logmass']**2, row['z']**2]
    if order == 2:
        features.insert(3, l_value**2)
   *     return features
   * Interactions: If errors vary with specific combinations, add more interaction terms (e.g., petrorad_r * z).
* Update Script: Modify the predict_sfr_features function and re-run the cross-validation to test the impact.
