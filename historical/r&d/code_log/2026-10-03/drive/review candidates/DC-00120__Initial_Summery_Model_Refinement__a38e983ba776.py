residuals = pd.DataFrame({
    "True": y_test,
    "RF": y_pred_rf - y_test,
    "GB": y_pred_gb - y_test,
    "Symbolic": y_pred_sym - y_test,
    "cosmo_rank": X_test["cosmo_rank"],
    "L_cosmo_s1": X_test["L_cosmo_s1.0"]
})
sns.scatterplot(data=residuals, x="True", y="RF", hue="cosmo_rank", size="L_cosmo_s1", alpha=0.6)
plt.axhline(0, color="black", linestyle="--")
plt.title("RF Residuals vs True log_SFR_Ha")
plt.savefig("residuals_rf.png")
plt.clf()


print("Correlation of BSD Features with Residuals:")
   * print(residuals[["RF", "GB", "Symbolic", "cosmo_rank", "L_cosmo_s1"]].corr()[["RF", "GB", "Symbolic"]])
