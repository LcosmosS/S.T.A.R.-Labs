    return {
        'Virgo_Analogue': np.array([1, 0.025, 1.57e5, 0.025, 6320, 0]),  # Simple
        'Coma_Analogue': np.array([1, 0.98, 3.31e7, 0.98, 9980, 1]),   # Recursive
        'Fibonacci_Rank3': np.array([3, 6.177, 9.75e5, 1.0, 6177, 1]),  # Recursive
        'Fibonacci_Rank2': np.array([2, 2.5, 5.00e5, 1.0, 4500, 0]),   # Simple
    }


def get_cosmological_bsd_analogue_data():
    """Provides data for the Cosmological BSD Analogue."""
    return {
        'Large_Scale_Study': np.array([12500.0, 12525.0, 0.998]),
    }




# ==============================================================================
# SECTION 2: SOPHISTICATED, TYPE-AWARE MODELS
# These models are more advanced, reflecting the non-linear "recursive encoding"
# and the importance of arithmetic invariants.
# ==============================================================================


def model_qft_by_type(invariants):
    """
    Models state complexity based on generator type.
