    A, B = 4.0, 2.5  # Typical empirical values
    log_M_star = A * np.log10(rotational_velocity) + B
    return 10**log_M_star


def model_fundamental_plane(velocity_dispersion, effective_radius):
    """
    Predicts stellar mass from the Fundamental Plane relation for ellipticals.
