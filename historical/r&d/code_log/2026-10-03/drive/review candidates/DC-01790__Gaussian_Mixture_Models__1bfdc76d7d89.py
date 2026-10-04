means = best_gmm.means_.flatten()
covariances = best_gmm.covariances_.flatten()
for i in range(optimal_n):
    print(f"Component {i}: mean logmass = {means[i]:.3f}, std logmass = {np.sqrt(covariances[i]):.3f}")
