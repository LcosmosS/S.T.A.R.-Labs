# Train a linear model
model = LinearRegression()
model.fit(train_df[features], train_df['sfr'])


# Predict and evaluate
test_pred = model.predict(test_df[features])
mse = mean_squared_error(test_df['sfr'], test_pred)
mse_list.append(mse)
print(f"Fold {fold+1} MSE: {mse:.4f}")
# Report results
avg_mse = np.mean(mse_list) std_mse = np.std(mse_list) print(f"\nAverage MSE: {avg_mse:.4f}") print(f"Standard Deviation of MSE: {std_mse:.4f}")
# Step 6: Diagnostic Plots # Observed vs. Predicted SFR
plt.scatter(df['sfr'], df['predicted_sfr'], alpha=0.5) plt.xlabel('Observed SFR') plt.ylabel('Predicted SFR') plt.title('Observed vs. Predicted SFR') plt.plot([df['sfr'].min(), df['sfr'].max()], [df['sfr'].min(), df['sfr'].max()], 'r--') plt.savefig('observed_vs_predicted_sfr.png') plt.close()
# Residuals vs. Logmass
residuals = df['sfr'] - df['predicted_sfr'] plt.scatter(df['logmass'], residuals, alpha=0.5) plt.xlabel('Logmass') plt.ylabel('Residuals (Observed - Predicted SFR)') plt.title('Residuals vs. Logmass') plt.axhline(0, color='r', linestyle='--') plt.savefig('residuals_vs_logmass.png') plt.close()
# Residuals vs. Redshift
plt.scatter(df['z'], residuals, alpha=0.5) plt.xlabel('Redshift (z)') plt.ylabel('Residuals (Observed - Predicted SFR)') plt.title('Residuals vs. z') plt.axhline(0, color='r', linestyle='--') plt.savefig('residuals_vs_z.png') plt.close()
print("Saved diagnostic plots: 'observed_vs_predicted_sfr.png', 'residuals_vs_logmass.png', 'residuals_vs_z.png'") print("Script completed successfully!")
