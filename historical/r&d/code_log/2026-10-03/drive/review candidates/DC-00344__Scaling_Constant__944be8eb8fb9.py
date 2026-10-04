    # Gravitational constant in appropriate units (Mpc * (km/s)^2 / M_sun)
    G = 4.30091e-6


    # Convert radius from Mpc to the same unit system
    radius = radius_mpc
   
    # Kinetic Energy (T) = 0.5 * M * sigma^2
    kinetic_energy = 0.5 * mass * (vel_disp**2)
   
    # Potential Energy (U) = - (3/5) * G * M^2 / R
    potential_energy = - (3.0/5.0) * G * (mass**2) / radius
   
    if potential_energy == 0: return 0
   
    return abs(2 * kinetic_energy / potential_energy)


def derive_and_analyze_curve(name, r, vel_disp):
    """
    Derives a UCF elliptic curve and analyzes its key arithmetic invariants,
