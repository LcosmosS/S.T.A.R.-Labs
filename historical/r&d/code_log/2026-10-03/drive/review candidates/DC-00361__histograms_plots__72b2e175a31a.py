    features = [logmass, z, l_value, dec, petrorad_r]
    if order == 2:
        features.insert(3, l_value**2)  # Add l_value^2 for order 2
    return features


# Prepare features for regression
features = ['logmass', 'z', 'l_value', 'l_value2', 'dec', 'petrorad_r']
df['l_value'] = l_1
df['l_value2'] = l_1**2 if order == 2 else 0
X = np.array([predict_sfr_features(row['logmass'], row['z'], l_1, order, row['dec'], row['petrorad_r']) 
              for _, row in df.iterrows()])
y = df['sfr'].values


# Step 5: Cross-Validation with Optimized Coefficients
k = 5
kf = KFold(n_splits=k, shuffle=True, random_state=42)
mse_list = []


for fold, (train_idx, test_idx) in enumerate(kf.split(X)):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    # Train a linear model to optimize coefficients
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict and evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mse_list.append(mse)
    print(f"Fold {fold+1} MSE: {mse:.4f}")


# Report cross-validation results
avg_mse = np.mean(mse_list)
std_mse = np.std(mse_list)
print(f"\nAverage MSE: {avg_mse:.4f}")
print(f"Standard Deviation of MSE: {std_mse:.4f}")


# Print optimized coefficients
coeff_names = ['logmass', 'z', 'l_value', 'dec', 'petrorad_r'] if order == 1 else ['logmass', 'z', 'l_value', 'l_value2', 'dec', 'petrorad_r']
print("\nOptimized Coefficients:")
for name, coef in zip(coeff_names, model.coef_):
    print(f"{name}: {coef:.4f}")
print(f"Intercept: {model.intercept_:.4f}")


# Step 6: Diagnostic Plots
# Observed vs. Predicted SFR
df['predicted_sfr'] = model.predict(X)
plt.scatter(df['sfr'], df['predicted_sfr'], alpha=0.5)
plt.xlabel('Observed SFR')
plt.ylabel('Predicted SFR')
plt.title('Observed vs. Predicted SFR')
plt.plot([df['sfr'].min(), df['sfr'].max()], [df['sfr'].min(), df['sfr'].max()], 'r--')
plt.savefig('observed_vs_predicted_sfr.png')
plt.close()


# Residuals vs. Logmass
residuals = df['sfr'] - df['predicted_sfr']
plt.scatter(df['logmass'], residuals, alpha=0.5)
plt.xlabel('Logmass')
plt.ylabel('Residuals (Observed - Predicted SFR)')
plt.title('Residuals vs. Logmass')
plt.axhline(0, color='r', linestyle='--')
plt.savefig('residuals_vs_logmass.png')
plt.close()


# Residuals vs. Redshift
plt.scatter(df['z'], residuals, alpha=0.5)
plt.xlabel('Redshift (z)')
plt.ylabel('Residuals (Observed - Predicted SFR)')
plt.title('Residuals vs. z')
plt.axhline(0, color='r', linestyle='--')
plt.savefig('residuals_vs_z.png')
plt.close()


print("Saved diagnostic plots: 'observed_vs_predicted_sfr.png', 'residuals_vs_logmass.png', 'residuals_vs_z.png'")
print("Script completed successfully!")
