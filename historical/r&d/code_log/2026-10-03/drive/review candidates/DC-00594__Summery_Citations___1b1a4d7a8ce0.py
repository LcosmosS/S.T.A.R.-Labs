def spherical_mapping(logD, logN, rank):
    theta = np.arccos(1 - 2 * (logN - logN.min()) / (logN.ptp()))
    phi = 2 * np.pi * (logD - logD.min()) / logD.ptp()
    x = (EARTH_EQUATORIAL_RADIUS + rank*1e3) * np.sin(theta) * np.cos(phi)
    y = (EARTH_POLAR_RADIUS + rank*1e3) * np.sin(theta) * np.sin(phi)
    z = (EARTH_POLAR_RADIUS + rank*1e3) * np.cos(theta)
    return x, y, z
