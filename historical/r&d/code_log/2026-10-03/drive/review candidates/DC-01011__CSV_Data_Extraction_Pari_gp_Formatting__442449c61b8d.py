def bsd_predicted_sfr(logmass, z, poly_terms=False): base_sfr = 0.5 * logmass - 0.1 * z if poly_terms: return base_sfr + 0.01 * logmass2 - 0.005 * z2 else: return base_sfr
