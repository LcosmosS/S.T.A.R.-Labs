    return {
        'Andromeda': {
            'r': 2.5,
            'vel_disp': 160, # Velocity dispersion of its globular cluster system
            'virial_radius': 0.3 # Estimated virial radius
        },
        'Coma Cluster': {
            'r': 321,
            'vel_disp': 978, # A well-measured value for the cluster
            'virial_radius': 3.0 # Estimated virial radius for the cluster
        },
        'Perseus Cluster': {
            'r': 236,
            'vel_disp': 1300, # One of the most massive clusters
            'virial_radius': 3.5
        },
    }


# ==============================================================================
# SECTION 2: FIRST-PRINCIPLES VIRIAL THEOREM MODEL
# ==============================================================================


def calculate_physical_virial_ratio(vel_disp, virial_radius):
    """
    Calculates a proxy for the virial ratio from physical observables.
