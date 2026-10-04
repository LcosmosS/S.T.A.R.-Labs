# Step 3: Theory Testing # Define a placeholder function for BSD Cosmology SFR prediction
def bsd_predicted_sfr(logmass, z): """ Placeholder for BSD Cosmology model to predict SFR from logmass and redshift. Replace this with the actual theoretical formula. Example: SFR = 0.5 * logmass - 0.1 * z (arbitrary for demonstration). """ return 0.5 * logmass - 0.1 * z
# Calculate predicted SFR based on the BSD model
df['predicted_sfr'] = bsd_predicted_sfr(df[logmass_col], df[z_col])
# Compare observed and predicted SFR using Mean Squared Error
mse = mean_squared_error(df[sfr_col], df['predicted_sfr']) print(f"\nMean Squared Error between observed and predicted SFR: {mse:.4f}")
# Visualize observed vs. predicted SFR
plt.figure(figsize=(6, 6)) plt.scatter(df[sfr_col], df['predicted_sfr'], alpha=0.5) plt.xlabel('Observed SFR') plt.ylabel('Predicted SFR') plt.title('Observed vs. Predicted SFR') plt.plot([df[sfr_col].min(), df[sfr_col].max()], [df[sfr_col].min(), df[sfr_col].max()], 'r--') # Diagonal line for reference plt.show()
print("Script completed!")
