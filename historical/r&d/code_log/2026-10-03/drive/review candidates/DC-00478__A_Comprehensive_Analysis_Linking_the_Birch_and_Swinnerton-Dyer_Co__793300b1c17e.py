    l_at_1 = cosmological_l_function(data, 1)
    l_at_1_plus_delta = cosmological_l_function(data, 1.001)  #small delta
    derivative = (l_at_1_plus_delta - l_at_1) / 0.001
    
    if np.abs(derivative) > 1e-5:  # threshold
        return 1
    else:
        return 2


def predict_sfr(galaxy, l_value, rank):
    """
    Predicts the star formation rate (SFR) for a galaxy.
