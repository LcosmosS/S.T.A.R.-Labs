    return kappa_derived

# Execute the new unified setup
Reg_cosmo_val, T_cosmo_val = calculate_data_driven_invariants()
DATA_DRIVEN_KAPPA = derive_kappa_from_invariants(Reg_cosmo_val, T_cosmo_val)

# Define the cluster set for testing this new KAPPA
cluster_data = {
    'Coma': {'r': 321, 'rho': 9980},
    'Perseus': {'r': 236, 'rho': 11500},
    'Centaurus': {'r': 170, 'rho': 7500},
    # Virgo is our calibration point, but we still test it
    'Virgo': {'r': 54, 'rho': 6320},
    'Hydra': {'r': 190, 'rho': 9000},
}

# Stage 1: Testing the Data-Driven KAPPA
# =========================================
print("\n--- Stage 1: Testing Data-Driven KAPPA against Clusters ---")

def test_cluster_with_kappa(cluster_name, r, rho, kappa_value):
    print(f"\nProcessing {cluster_name} with data-driven KAPPA = {kappa_value:.2f}")
    try:
        a_predicted = -kappa_value * r
        b_predicted = rho
        # For Virgo, the original 'a' was -1706. Let's see how close our derived 'a'
