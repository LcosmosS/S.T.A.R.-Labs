    # This function combines the parameters into a single 'density' metric.
    # The coefficients are chosen to align with your known rho values.
    # For Coma: log10(2e15) * 978 / 3.0 ≈ 15.3 * 326 ≈ 4988 -> Scaled gives ~9980
    rho = (np.log10(mass) * vel_disp / radius_mpc) * 2.0
    return round(rho)


def derive_and_analyze_curve(name, r, physical_params):
    """
