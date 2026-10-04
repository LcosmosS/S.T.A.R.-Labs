# Handle missing values by imputing with the mean
imputer = SimpleImputer(strategy='mean') df[[logmass_col, z_col, sfr_col]] = imputer.fit_transform(df[[logmass_col, z_col, sfr_col]])
# Step 1: Explore Trends # Plot logmass vs. SFR and z vs. SFR to identify patterns
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1) plt.scatter(df[logmass_col], df[sfr_col], alpha=0.5) plt.xlabel('Log Stellar Mass') plt.ylabel('Star Formation Rate') plt.title('Logmass vs. SFR')
plt.subplot(1, 2, 2) plt.scatter(df[z_col], df[sfr_col], alpha=0.5) plt.xlabel('Redshift (z)') plt.ylabel('Star Formation Rate') plt.title('z vs. SFR')
plt.tight_layout() plt.savefig('trends_plot.png') plt.close() print("Saved trends plot as 'trends_plot.png'.")
# Step 2: Group Analysis # Check if 'group' column exists; if not, create groups by binning logmass
if 'group' not in df.columns: df['group'] = pd.cut(df[logmass_col], bins=4, labels=['Low', 'Mid-Low', 'Mid-High', 'High']) print("Created 'group' column by binning logmass into 4 quartiles.")
# Calculate and print group statistics
group_stats = df.groupby('group').agg({ logmass_col: ['mean', 'median', 'std'], z_col: ['mean', 'median', 'std'], sfr_col: ['mean', 'median', 'std'] }) print("\nGroup Statistics:") print(group_stats)
# Step 3: Theory Testing # Define the BSD Cosmology model to predict SFR # *** REPLACE THIS WITH THE ACTUAL BSD FORMULA ***
def bsd_predicted_sfr(logmass, z): """ Placeholder for BSD Cosmology model to predict SFR from logmass and redshift. Replace this with the actual theoretical formula. Example: SFR = 0.5 * logmass - 0.1 * z (arbitrary for demonstration). """ return 0.5 * logmass - 0.1 * z
# Calculate predicted SFR based on the BSD model
df['predicted_sfr'] = bsd_predicted_sfr(df[logmass_col], df[z_col])
# Compute Mean Squared Error (MSE) between observed and predicted SFR
mse = mean_squared_error(df[sfr_col], df['predicted_sfr']) print(f"\nMean Squared Error between observed and predicted SFR: {mse:.4f}")
# Plot observed vs. predicted SFR
plt.figure(figsize=(6, 6)) plt.scatter(df[sfr_col], df['predicted_sfr'], alpha=0.5) plt.xlabel('Observed SFR') plt.ylabel('Predicted SFR') plt.title('Observed vs. Predicted SFR') plt.plot([df[sfr_col].min(), df[sfr_col].max()], [df[sfr_col].min(), df[sfr_col].max()], 'r--') # Diagonal line for reference plt.savefig('observed_vs_predicted_sfr.png') plt.close() print("Saved observed vs. predicted SFR plot as 'observed_vs_predicted_sfr.png'.")
print("\nScript completed successfully!")
