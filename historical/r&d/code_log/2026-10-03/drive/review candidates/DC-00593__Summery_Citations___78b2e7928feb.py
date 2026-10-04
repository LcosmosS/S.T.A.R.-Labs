# Spherical coordinate mapping with geoid correction
def map_to_geoid(logD, logN, rank):
    phi = 2 * np.pi * (logD - logD.min()) / (logD.max() - logD.min())
    theta = np.arccos(1 - 2 * (logN - logN.min()) / (logN.max() - logN.min()))
    x = (EARTH_EQUATORIAL_RADIUS + rank*1000) * np.sin(theta) * np.cos(phi)
    y = (EARTH_POLAR_RADIUS + rank*1000) * np.sin(theta) * np.sin(phi)
    z = (EARTH_POLAR_RADIUS + rank*1000) * np.cos(theta)
    return x, y, z
