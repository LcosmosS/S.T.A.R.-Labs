    return {
        'Virgo Cluster': { # Known "Simple" generator from your papers
            'r': 54, 'vel_disp': 750, 'virial_radius': 2.2, 'virial_mass': 1.5e15
        },
        'Andromeda': { # A large spiral galaxy, likely "Simple"
            'r': 2.5, 'vel_disp': 160, 'virial_radius': 0.3, 'virial_mass': 1.5e12
        },
        'Coma Cluster': { # Known "Recursive" generator from your papers
            'r': 321, 'vel_disp': 978, 'virial_radius': 3.0, 'virial_mass': 2.0e15
        },
        'Perseus Cluster': { # A massive cluster, likely "Recursive"
            'r': 236, 'vel_disp': 1300, 'virial_radius': 3.5, 'virial_mass': 2.5e15
        },
    }


# ==============================================================================
# SECTION 2: FIRST-PRINCIPLES & UCF PREDICTIVE MODELS
# ==============================================================================


def calculate_physical_virial_ratio(mass, vel_disp, radius_mpc):
    """
