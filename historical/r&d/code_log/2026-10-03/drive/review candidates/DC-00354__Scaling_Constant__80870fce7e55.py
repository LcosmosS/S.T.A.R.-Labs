    return {
        'Virgo Cluster': { # The benchmark case for calibration
            'r': 54, 'vel_disp': 750, 'virial_radius': 2.2, 'virial_mass': 1.5e15
        },
        'Andromeda': { # A "Simple" structure to test the calibrated constant
            'r': 2.5, 'vel_disp': 160, 'virial_radius': 0.3, 'virial_mass': 1.5e12
        },
        'Coma Cluster': { # The benchmark "Recursive" structure
            'r': 321, 'vel_disp': 978, 'virial_radius': 3.0, 'virial_mass': 2.0e15
        },
        'Perseus Cluster': { # A massive "Recursive" structure
            'r': 236, 'vel_disp': 1300, 'virial_radius': 3.5, 'virial_mass': 2.5e15
        },
    }


# ==============================================================================
# SECTION 2: IMPLEMENTATION OF THE NEW PHYSICAL LAW
# ==============================================================================


def calculate_virial_imbalance(mass, vel_disp, radius_mpc):
    """
    Calculates the 'Virial Imbalance' (2T + U), the energy term that,
