bsd_shap_rf = shap_values_rf[:, features.index("BSD_likelihood")]
bsd_shap_gb = shap_values_gb[:, features.index("BSD_likelihood")]


print(f"Mean SHAP (RF) for BSD_likelihood: {np.mean(np.abs(bsd_shap_rf)):.4f}")
print(f"Mean SHAP (GB) for BSD_likelihood: {np.mean(np.abs(bsd_shap_gb)):.4f}")
