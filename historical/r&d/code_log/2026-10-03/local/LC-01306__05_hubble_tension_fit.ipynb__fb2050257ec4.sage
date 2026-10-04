plt.figure(figsize=(7, 5))
plt.errorbar(z, H_obs, yerr=0.05 * H_obs, fmt="o", label="Observed (proxy)")
plt.plot(z, H_eff_vals, "-", lw=2, label="S.T.A.R. H_eff(z)")
plt.xlabel("z")
plt.ylabel("H (km/s/Mpc)")
plt.title("H_eff(z) vs Observed (proxy)")
plt.legend()
plt.grid(True)

plt.savefig("results/hubble_fit.png", dpi=200)
plt.show()

with open("results/hubble_fit_summary.json", "w") as f:
    json.dump({"chi2": float(chi2), "mean_residual": float(np.mean(residuals))}, f)

print("Saved results/hubble_fit.png and results/hubble_fit_summary.json")