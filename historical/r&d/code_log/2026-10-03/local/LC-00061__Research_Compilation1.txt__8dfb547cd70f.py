from sklearn.mixture import GaussianMixture
log_mass = log_mass.reshape(-1, 1)
gmm = GaussianMixture(n_components=2, random_state=0).fit(log_mass)
labels = gmm.predict(log_mass)
main_component = labels == np.argmax(gmm.weights_)  # Largest component
filtered_log_mass = log_mass[main_component].flatten()
   * np.savetxt("filtered_log_mass.txt", filtered_log_mass, fmt='%.18f', header="log_mass = [", footer="];", comments='')
   * Use in PARI/GP as above.
   * Fit to Theory: Separates log-normal core, enhancing symmetry for BSD analogy.
   * Pros: Identifies sub-populations, data-driven. Cons: Assumes Gaussian components, needs component selection.
