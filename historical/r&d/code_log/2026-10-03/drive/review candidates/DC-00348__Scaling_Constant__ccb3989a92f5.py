    return {
        'Virgo Cluster': { # Benchmark "Simple" case
            'r': 54, 'vel_disp': 750, 'virial_radius': 2.2, 'virial_mass': 1.5e15
        },
        'Andromeda': { # Expected "Simple"
            'r': 2.5, 'vel_disp': 160, 'virial_radius': 0.3, 'virial_mass': 1.5e12
        },
        'Coma Cluster': { # Benchmark "Recursive" case
            'r': 321, 'vel_disp': 978, 'virial_radius': 3.0, 'virial_mass': 2.0e15
        },
        'Perseus Cluster': { # Expected "Recursive"
            'r': 236, 'vel_disp': 1300, 'virial_radius': 3.5, 'virial_mass': 2.5e15
        },
    }


# ==============================================================================
# SECTION 2: FIRST-PRINCIPLES & UCF PREDICTIVE MODELS
# ==============================================================================


def calculate_physical_virial_ratio(mass, vel_disp, radius_mpc):
    """
    Calculates the true, dimensionless Virial Ratio (2T / |U|).
