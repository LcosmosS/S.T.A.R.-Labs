    return 0.5 * logmass - 0.1 * z


# Calculate predicted SFR based on the BSD model
df['predicted_sfr'] = bsd_predicted_sfr(df[logmass_col], df[z_col])


# Compute Mean Squared Error (MSE) between observed and predicted SFR
mse = mean_squared_error(df[sfr_col], df['predicted_sfr'])
print(f"\nMean Squared Error between observed and predicted SFR: {mse:.4f}")


# Plot observed vs. predicted SFR
plt.figure(figsize=(6, 6))
plt.scatter(df[sfr_col], df['predicted_sfr'], alpha=0.5)
plt.xlabel('Observed SFR')
plt.ylabel('Predicted SFR')
plt.title('Observed vs. Predicted SFR')
plt.plot([df[sfr_col].min(), df[sfr_col].max()], 
         [df[sfr_col].min(), df[sfr_col].max()], 'r--')  # Diagonal line for reference
plt.savefig('observed_vs_predicted_sfr.png')
plt.close()
print("Saved observed vs. predicted SFR plot as 'observed_vs_predicted_sfr.png'.")


print("\nScript completed successfully!")
