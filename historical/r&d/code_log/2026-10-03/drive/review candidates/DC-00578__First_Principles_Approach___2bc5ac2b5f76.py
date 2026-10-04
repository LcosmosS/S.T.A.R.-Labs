    # Proportionality constant (C) derived from gravitational thermodynamics theory
    # This would be a major theoretical result in a full paper. We'll use a plausible value.
    C_grav_thermo = 0.55
    return C_grav_thermo * np.sqrt(N)


# --- Pathway 2: Cosmological Scaling Laws ---
def model_tully_fisher(rotational_velocity):
    """
    Predicts stellar mass from rotational velocity using the Tully-Fisher relation.
