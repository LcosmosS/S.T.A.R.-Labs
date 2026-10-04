# After optimizing GMM components
gmm = GaussianMixture(n_components=optimal_n, random_state=0).fit(logmass.reshape(-1, 1))
groups = gmm.predict(logmass.reshape(-1, 1))


# Plot histograms for all groups
for i in range(gmm.n_components):
    plt.hist(logmass[groups == i], bins=50, density=True, alpha=0.6, label=f"Group {i}")
    plt.legend()
    plt.title(f"Logmass Distribution - Group {i}")
    plt.savefig(f"Group_{i}_logmass.png")
    plt.close()


# Gamma fit for all groups
for i in range(gmm.n_components):
    params = gamma.fit(logmass[groups == i])
    print(f"Group {i} gamma fit: {params}")


# Extended L_cosmo for all groups
for s in [0.5, 1.5, 2]:
    for i in range(gmm.n_components):
        L = compute_L_cosmo(logmass[groups == i], s)
        print(f"Group {i}: L_cosmo(s={s}) = {L:.4f}")
