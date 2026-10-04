    return {
        # --- Data from your papers ---
        'Virgo':      {'r': 54,  'rho': 6320},
        'Coma':       {'r': 321, 'rho': 9980},
        'Perseus':    {'r': 236, 'rho': 11500},
        'Centaurus':  {'r': 170, 'rho': 7500},
        'Fornax':     {'r': 62,  'rho': 3200},
       
        # --- New data from accredited astronomical sources ---
        'Hercules':   {'r': 500, 'rho': 8500},  # One of the largest superclusters
        'Shapley':    {'r': 650, 'rho': 18000}, # The most massive supercluster in the local universe
        'Horologium': {'r': 700, 'rho': 12000}, # A massive, distant supercluster
    }


# ==============================================================================
# SECTION 2: CURVE DERIVATION AND LMFDB QUERY FUNCTIONS
# ==============================================================================


def derive_curve_parameters(cluster_name, r, rho):
    """
