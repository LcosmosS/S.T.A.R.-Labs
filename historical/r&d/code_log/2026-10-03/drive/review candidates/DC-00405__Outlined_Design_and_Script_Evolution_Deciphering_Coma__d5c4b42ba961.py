    print("\n--- Calculating Data-Driven Invariants (from N=978 sample) ---")
    
    # [cite_start]These values are taken directly from your successful validation [cite: 2004]
    N = 978
    Reg_cosmo = 2.51
    
    # T_cosmo is derived from the scaling law T_cosmo = C * sqrt(N)
    # [cite_start]Your N=978 paper used T_cosmo = 17.18 [cite: 2004]
    T_cosmo = 17.18
    
    print(f"  Using N={N}, Reg_cosmo={Reg_cosmo}, T_cosmo={T_cosmo}")
    return Reg_cosmo, T_cosmo


# -- Part 2: Formulate the KAPPA Derivation Hypothesis --


def derive_kappa_from_invariants(Reg_cosmo, T_cosmo):
    """
    Derives the geometric KAPPA scaling factor from the statistical invariants.
