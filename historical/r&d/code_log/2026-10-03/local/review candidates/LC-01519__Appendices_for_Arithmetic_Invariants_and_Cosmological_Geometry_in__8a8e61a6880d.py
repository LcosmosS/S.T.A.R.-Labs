    C_grav_thermo = 0.55
    return C_grav_thermo * np.sqrt(N)

# --- Pathway 2: Cosmological Scaling Laws ---
def model_tully_fisher(rotational_velocity):
    """
    Predicts stellar mass from rotational velocity using the Tully-Fisher relation.
