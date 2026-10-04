def predict_sfr_features(logmass, z, l_value, order, dec=0, petrorad_r=0):
*     return [logmass, z, l_value, l_value**2 if order == 2 else 0, dec, petrorad_r]
