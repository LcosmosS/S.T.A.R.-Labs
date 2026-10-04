    kinetic_energy = 0.5 * mass * (vel_disp**2)
    potential_energy = - (3.0/5.0) * G * (mass**2) / radius_mpc
    return 2 * kinetic_energy + potential_energy


def model_rho_from_virial_state(mass, vel_disp, radius_mpc):
    """
    The refined model for the 'b' coefficient ('rho'), representing the full
