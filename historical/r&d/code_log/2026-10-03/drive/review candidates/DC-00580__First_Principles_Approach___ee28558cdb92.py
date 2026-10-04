    # Coefficients from astrophysical studies
    A, B = 1.4, 0.9
    # Simplified relation to predict mass
    log_M_star = A * np.log10(velocity_dispersion) + B * np.log10(effective_radius) + 3.0
    return 10**log_M_star


# --- Pathway 4: Mathematical Fine-Tuning ---
def model_universe_stability(rank, regulator):
    """
    A simplified model to test the Anthropic Principle.
