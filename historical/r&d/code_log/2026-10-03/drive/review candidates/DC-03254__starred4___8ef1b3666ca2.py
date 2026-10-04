def bsd_predicted_sfr(logmass, z):
    base_sfr = 4.25 * logmass + 49.04 * z - 0.22 * logmass**2 - 3.94 * logmass * z + 1.30 * z**2
*     return base_sfr
