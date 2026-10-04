    print("\n--- Deriving Geometric KAPPA from Statistical Invariants ---")

    # Original kappa was empirically fitted to Virgo
    ORIGINAL_KAPPA = 31.59259

    # Hypothesis: KAPPA is proportional to the product of the key invariants.
    # KAPPA = C * Reg_cosmo * T_cosmo
    # We can find the constant of proportionality, C, from the original Virgo fit.
    C = ORIGINAL_KAPPA / (Reg_cosmo * T_cosmo)

    print(f"  Calibrating proportionality constant C = {C:.4f}")

    # Now, we define our new, data-driven KAPPA
    kappa_derived = C * Reg_cosmo * T_cosmo
