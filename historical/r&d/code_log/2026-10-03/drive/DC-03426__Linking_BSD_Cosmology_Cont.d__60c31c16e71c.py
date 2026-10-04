# Theory Testing: Define a placeholder for BSD Cosmology model
def bsd_predicted_sfr(logmass, z): # Replace this with the actual BSD Cosmology model formula return 0.5 * logmass - 0.1 * z # Example linear combination
# Calculate predicted SFR and compare to observed
df['predicted_sfr'] = bsd_predicted_sfr(df[logmass_col], df[z_col]) mse = mean_squared_error(df[sfr_col], df['predicted_sfr']) print(f"\nMean Squared Error between observed and predicted SFR: {mse:.4f}")
# Plot observed vs. predicted SFR
plt.figure(figsize=(6, 6)) plt.scatter(df[sfr_col], df['predicted_sfr'], alpha=0.5) plt.xlabel('Observed SFR') plt.ylabel('Predicted SFR') plt.title('Observed vs. Predicted SFR') plt.plot([df[sfr_col].min(), df[sfr_col].max()], [df[sfr_col].min(), df[sfr_col].max()], 'r--') plt.show()
print("Script completed!")
