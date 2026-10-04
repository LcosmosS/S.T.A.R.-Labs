    log_mass_sample = np.random.normal(loc=10.5, scale=0.5, size=num_galaxies)
    mass_sample = 10**log_mass_sample
   
    # Calculate invariants from the data-driven model [1]
    N = len(mass_sample)
    M0 = np.median(mass_sample)
    mass_ratios = mass_sample / M0
   
    Reg_cosmo = np.mean(mass_ratios)
    L_cosmo_norm_1 = np.mean(M0 / mass_sample)
   
    # --- Central Test ---
    # Instead of an empirical T_cosmo, we model it as a fluctuation term.
    # The absolute fluctuation of an extensive quantity scales with sqrt(N).
    # We'll define our fluctuation term based on the standard deviation of mass ratios.
    fluctuation_amplitude = np.std(mass_ratios)
    T_fluctuation = fluctuation_amplitude * sqrt(N)
   
    # Calculate the right side of the cosmological BSD analogue using this new term
    right_side = (OMEGA_TILDE * Reg_cosmo * N * SHA_COSMO) / (T_fluctuation**2)
   
    # Derive the resulting normalization constant K
    K = right_side / L_cosmo_norm_1
   
    print(f"Analysis for N = {N} galaxies:")
    print(f"  Data-Driven L_cosmo_norm(1) = {L_cosmo_norm_1:.4f}")
    print(f"  Data-Driven Reg_cosmo = {Reg_cosmo:.4f}")
    print(f"  Hypothesized T_fluctuation = {RR(T_fluctuation):.4f} (from std dev * sqrt(N))")
    print(f"  Calculated Right Side = {right_side:.4f}")
    print(f"  Resulting Normalization Constant K = {K:.4f}\n")
   
    if 0.9 < K < 1.1:
        print("RESULT: Strong Support for Hypothesis.")
        print("The normalization constant K is very close to 1. This suggests the T_cosmo parameter")
        print("is indeed a measure of statistical fluctuations within the galaxy distribution, providing")
        print("a first-principles connection to the statistical mechanics of self-gravitating systems.")
    else:
        print("RESULT: Hypothesis Not Supported by this Model.")
        print(f"The calculated K = {K:.4f} deviates significantly from 1. The link between T_cosmo")
        print("and simple statistical fluctuations may be more complex or other factors are involved.")


test_statistical_fluctuation_hypothesis()
print("--- Complete. ---\n")




# ------------------------------------------------------------------------------
# STAGE 2: COSMOLOGICAL SCALING LAW CORRELATION (TULLY-FISHER RELATION)
# ------------------------------------------------------------------------------
print("--- Testing Correlation with Established Cosmological Scaling Laws ---")
print("Hypothesis: The framework's arithmetic invariants should correlate with physical observables in a way that reproduces known scaling laws, like the Tully-Fisher relation.\n")


def test_tully_fisher_correlation():
    """
    Tests for a correlation between an arithmetic invariant (regulator) and a
