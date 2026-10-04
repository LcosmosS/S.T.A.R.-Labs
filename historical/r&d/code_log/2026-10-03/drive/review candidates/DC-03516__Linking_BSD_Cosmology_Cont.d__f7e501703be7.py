def predict_sfr_features(row, l_value, order):
    features = [row['logmass'], row['z'], l_value, row['dec'], row['petrorad_r'], row['environment'], 
                row['logmass'] * row['z'], row['logmass']**2, row['z']**2]
    if order == 2:
        features.insert(3, l_value**2)
   *     return features
