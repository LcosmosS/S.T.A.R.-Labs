    print("Running QFT Correlation Test...")
    ucf_regulators = np.array([data[1] for data in ucf_data.values()])


    # Use comoving volume as a proxy for the energy scale of the structure
    ucf_volumes = np.array([data[2] for data in ucf_data.values()])
    qft_complexities = model_quantum_field_theory(ucf_volumes)


    correlation, p_value = pearsonr(ucf_regulators, qft_complexities)
    print(f"  > Pearson Correlation (Regulator vs QFT Complexity): {correlation:.4f}")
    print(f"  > P-value: {p_value:.4f}")
    return {"correlation": correlation, "p_value": p_value}


def test_gr_correlation(ucf_data):
    """
    Tests for a correlation between the UCF's comoving volume (geometry) and
