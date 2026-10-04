    regulator, l_value, generator_type = invariants
    if generator_type == 0:  # Simple
        return 5 * regulator + 0.1 # Simple linear model
    else:  # Recursive
        # Non-linear model reflecting "recursive encoding"
        # Using a ratio is a toy model for this complex interaction
        return np.log(1 + regulator) * (l_value + 1)**2


def model_gr_unified(density_height):
    """
    A more direct GR model. Instead of inferring density from volume,
