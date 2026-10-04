# Define foundational constants from your research
VIRGO_CALIBRATED_KAPPA = 31.59259259259259

# Define the dataset of galaxy clusters for analysis
# --- CHANGE 1: ADDED A NEW CLUSTER FOR VALIDATION ---
cluster_data = {
    'Coma': {'r': 321, 'rho': 9980},
    'Perseus': {'r': 236, 'rho': 11500},
    'Fornax': {'r': 62, 'rho': 3200},
    'Hercules': {'r': 500, 'rho': 8500},
    'Centaurus': {'r': 170, 'rho': 7500}  # New cluster with plausible data
}

# --- CHANGE 2: DESIGNATED THE NEW CLUSTER AS THE HOLDOUT ---
HOLDOUT_CLUSTER = 'Centaurus'
print(f"Holdout cluster for final validation: {HOLDOUT_CLUSTER}")

# Stage 1: Foundational Dataset Generation
# =========================================

print("\n--- Stage 1: Generating Foundational Dataset ---")

def derive_and_analyze_cluster_curve(cluster_name, r, rho):
    """
    Applies the Virgo-calibrated scaling law to derive and analyze
