# Overall MSE with quenching
mse_base = mean_squared_error(df[sfr_col], df['predicted_sfr'])
print(f"\nOverall MSE with Quenching: {mse_base:.4f}")


# Residual plots
plt.scatter(df[logmass_col], df[sfr_col] - df['predicted_sfr'], alpha=0.5)
plt.xlabel('Logmass')
plt.ylabel('Residual (Observed - Predicted SFR)')
plt.title('Residuals vs. Logmass')
plt.savefig('residuals_vs_logmass.png')
plt.close()


plt.scatter(df[z_col], df[sfr_col] - df['predicted_sfr'], alpha=0.5)
plt.xlabel('Redshift (z)')
plt.ylabel('Residual (Observed - Predicted SFR)')
plt.title('Residuals vs. z')
plt.savefig('residuals_vs_z.png')
plt.close()
print("Saved residual plots ('residuals_vs_logmass.png', 'residuals_vs_z.png').")


print("\nScript completed successfully!")
