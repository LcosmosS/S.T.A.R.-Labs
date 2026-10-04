import numpy as np


def spherical_to_cartesian(phi_deg, theta_deg, elevation, R=1000):
    phi = np.radians(phi_deg)
    theta = np.radians(theta_deg)
    r = R + elevation
    x = r * np.cos(theta) * np.cos(phi)
    y = r * np.cos(theta) * np.sin(phi)
    z = r * np.sin(theta)
    return x, y, z
