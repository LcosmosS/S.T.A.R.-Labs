plt.scatter(df['z'], residuals, alpha=0.5) plt.xlabel('Redshift (z)') plt.ylabel('Residuals (Observed - Predicted SFR)') plt.title('Residuals vs. z') plt.axhline(0, color='r', linestyle='--') plt.savefig('residuals_vs_z.png') plt.close()
print("Saved diagnostic plots: 'observed_vs_predicted_sfr.png', 'residuals_vs_logmass.png', 'residuals_vs_z.png'") print("Script completed successfully!")
