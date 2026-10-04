def predict_sfr_features(logmass, z, l_value, order, dec=0, petrorad_r=0, environment=0, gas_density=0, metallicity=0):
    features = [logmass, z, l_value, dec, petrorad_r, environment, logmass * z, gas_density, metallicity]
    if order == 2:
        features.insert(3, l_value**2)
*     return features
* Update the feature preparation section to include these columns if they exist in your dataset:
* python
* optional_columns = ['dec', 'petrorad_r', 'ra', 'gas_density', 'metallicity']
