        return np.nan
    angle_rad = (angular_size_arcsec * u.arcsec).to(u.rad).value
    radius_mpc = distance_mpc * angle_rad
    return (radius_mpc * u.Mpc).to(u.lyr).value

def calculate_virial_energy(mass_sm, radius_ly):
    """Calculates the Virial Energy in Joules."""
    if not np.isfinite(mass_sm) or not np.isfinite(radius_ly) or mass_sm <= 0 or
