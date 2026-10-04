def predict_sfr(logmass, z, l_value, order, petrorad_r=0, environment=0):
*     return [logmass, z, l_value, l_value**2 if order == 2 else 0, petrorad_r, environment]
