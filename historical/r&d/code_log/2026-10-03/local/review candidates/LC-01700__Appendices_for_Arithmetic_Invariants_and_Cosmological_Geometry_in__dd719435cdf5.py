        print(f"compute_3selmer_rank: Skipped - Invalid delta={delta},
conductor={conductor}, logmass={logmass}, entropy={entropy}, betti_1={betti_1},
entropy_gradient={entropy_gradient}")
        return np.nan, 'invalid_input', np.nan, np.nan, np.nan
    try:
        scale_factor = max(1e3, delta / np.sqrt(MAX_CONDUCTOR))
        delta_scaled = int(delta / scale_factor)
        conductor_scaled = delta_scaled**2
        if conductor_scaled > MAX_CONDUCTOR:
            print(f"compute_3selmer_rank: Skipped - Scaled
conductor={conductor_scaled} > MAX_CONDUCTOR")
            return np.nan, 'large_conductor', np.nan, np.nan, np.nan
        a = -delta_scaled
        b = delta_scaled**2 + entropy * logmass + COHOMOLOGY_WEIGHT * betti_1 +
