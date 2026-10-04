try:
    from src.physics.hubble_effective import HubbleEffective
    from src.physics.hubble_tension_fit import HubbleTensionFit

    HE = HubbleEffective()
    HT = HubbleTensionFit()

    # Build simple invariants and entropy_curvature arrays (synthetic)
    invariants_list = [{"omega": 1.0, "rank": np.random.randint(1, 3)} for _ in z]
    entropy_curvatures = np.random.normal(scale=0.1, size=len(z))

    H_eff_vals = np.array(
        [
            HE.H_eff(zi, inv, ec)
            for zi, inv, ec in zip(z, invariants_list, entropy_curvatures)
        ]
    )

    # Observed H from distances: H_obs = (c*z)/d
    H_obs = (3e5 * z) / (dist + 1e-12)

    residuals = H_eff_vals - H_obs
    chi2 = HT.chi_squared(residuals, sigma=np.maximum(1.0, 0.05 * H_obs))

    print("Computed H_eff and residuals. chi2:", chi2)

except Exception as e:
    print("Hubble modules not available; using fallback linear H(z) model.", e)

    H_eff_vals = 70.0 * np.ones_like(z)
    H_obs = (3e5 * z) / (dist + 1e-12)
    residuals = H_eff_vals - H_obs
    chi2 = np.sum((residuals / np.maximum(1.0, 0.05 * H_obs)) ** 2)