# ====================== EXECUTION ======================
synth, real1, real2 = load_data()

synth = add_thesis_features(synth)
real1 = add_thesis_features(real1)
real2 = add_thesis_features(real2, target_col='zphot')

synth = add_optimized_topology(synth, "synth", "synthetic_RA", "synthetic_DE", "synthetic_z")
real1 = add_optimized_topology(real1, "real1", "RAJ2000", "DEJ2000", "Vcmb")
real2 = add_optimized_topology(real2, "real2", "RAdeg", "DEdeg", "zphot")

synth_y = synth['exact_rank']
real1_y = real1['persistence_entropy']
real2_y = real2['persistence_entropy']

common_features = [
    'flux_gr', 'pm_mag_proxy', 'mag_ratio', 'Tully_Fisher',
    'normalized_density', 'T_cosmo', 'local_betti_0', 'local_betti_1', 'local_betti_2'
]

imputer = KNNImputer(n_neighbors=10)
for df in [synth, real1, real2]:
    df[common_features] = imputer.fit_transform(df[common_features])

# ====================== DOMAIN ALIGNMENT ======================
print("\n--- Aligning Domains with Quantile Transformer ---")
# We fit the transformer on the REAL observations (the target domain).
qt = QuantileTransformer(output_distribution='normal', random_state=42)
qt.fit(real2[common_features])

# Transform all datasets to force their distributions to match the Real2 shape.
synth[common_features] = qt.transform(synth[common_features])
real1[common_features] = qt.transform(real1[common_features])
real2[common_features] = qt.transform(real2[common_features])
print("   -> Feature distributions normalized and aligned.")

# ====================== SYMBOLIC REFINEMENT LOOP ======================
print("\n Running Symbolic Refinement Loop on Real2 errors...")
beta = 16.263
lambda_scale = 1.0
engine = ProjectionEngine(beta=beta, lambda_scale=lambda_scale)
print(f"Initial β = {beta:.4f}")
