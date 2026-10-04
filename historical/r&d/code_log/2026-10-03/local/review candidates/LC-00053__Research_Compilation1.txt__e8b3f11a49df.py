from sklearn.cluster import DBSCAN
data = np.vstack([log_mass, df['z'].replace(-9999, np.nan).dropna().values]).T
db = DBSCAN(eps=0.5, min_samples=5).fit(data)
filtered_log_mass = log_mass[db.labels_ != -1]  # Exclude noise
   * np.savetxt("filtered_log_mass.txt", filtered_log_mass, fmt='%.18f', header="log_mass = [", footer="];", comments='')
   * Use in PARI/GP.
   * Fit to Theory: Focuses on homogeneous groups, potentially log-normal, improving ( K ).
   * Pros: Handles multidimensional data, adaptive. Cons: Eps tuning critical, may exclude valid points.
