    G = 4.30091e-6 # (Mpc * (km/s)^2 / M_sun)
    kinetic_energy = 0.5 * mass * (vel_disp**2)
    potential_energy = - (3.0/5.0) * G * (mass**2) / radius_mpc
    if potential_energy == 0: return 0
    return abs(2 * kinetic_energy / potential_energy)


def model_rho_from_virial_state(mass, vel_disp, radius_mpc):
    """
    A more sophisticated model for the 'b' coefficient ('rho'), representing
