# Step 3: Compute Topological Signature
D_arith = persistent_diagram(points)

# Step 4: Load Observational Dataset
obs_points = load_sdss_coordinates(z_max=0.1)
D_cosmo = persistent_diagram(obs_points)

# Step 5: Compare Diagrams
W_distance = wasserstein_distance(D_arith, D_cosmo)

# Step 6: Evaluate Hypothesis
if W_distance < 0.01:
    print("Support for ACSC")
else:
    print("Reject or refine ACSC")
