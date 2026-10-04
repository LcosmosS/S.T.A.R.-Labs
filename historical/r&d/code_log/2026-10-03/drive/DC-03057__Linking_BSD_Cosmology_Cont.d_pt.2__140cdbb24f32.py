    print("If you haven't exported the data from CasJobs, please do so and place it in /home/pmqr7/data/")
    exit(1)
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit(1)


# --- Post-Processing: Derive Features ---
print("Deriving features...")


# Compute log_SFR_Ha from sfr (already in SDSSDR18_Updated.csv)
df['log_SFR_Ha'] = np.log10(df['sfr'].clip(lower=1e-10))  # Avoid log(0) by clipping


# Compute log_Mass_gas (simplified scaling with SFR, as done previously)
df['log_Mass_gas'] = df['log_SFR_Ha'] + 8.0  # Adjust constant as needed


# Compute OH_Mar13_N2_Re_fit (metallicity) using N2 method
df['N2'] = np.log10(df['nii_6584_flux'] / df['h_alpha_flux'].clip(lower=1e-10))
df['OH_Mar13_N2_Re_fit'] = 8.90 + 0.57 * df['N2']


# Compute Av_gas_Re (dust attenuation) using Balmer decrement
df['Ha_Hb'] = df['h_alpha_flux'] / df['h_beta_flux'].clip(lower=1e-10)
df['Av_gas_Re'] = 2.5 * 3.33 * np.log10(df['Ha_Hb'] / 2.86)


# Approximate log_SFR_ssp (SFR from SSP models) using sfr as a proxy
df['log_SFR_ssp'] = np.log10(df['sfr'].clip(lower=1e-10)) * 0.9  # Simplified scaling


# Use nsa_mstar as mass_stellar_best_fit
df['mass_stellar_best_fit'] = df['nsa_mstar']


# Approximate SFR_0_1Gyr_best_fit (target) using sfr
# Assuming SFR_0_1Gyr_best_fit is a recent SFR, we scale sfr slightly
df['SFR_0_1Gyr_best_fit'] = df['sfr'] * 1.1  # Simplified scaling


# --- Feature Selection ---
features = ['log_Mass_gas', 'log_SFR_Ha', 'log_mass', 'log_SFR_ssp', 'mass_stellar_best_fit']
target = 'SFR_0_1Gyr_best_fit'


# --- Filter and Clean Data ---
print("Cleaning data...")
df_clean = df[features + [target]].dropna()
print(f"Dataset after cleaning: {df_clean.shape[0]} rows, {df_clean.shape[1]} columns")


# --- Train-Test Split ---
X = df_clean[features]
y = df_clean[target]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")


# --- Model Training ---
print("Training models...")


# Gradient Boosting Regressor
gb = GradientBoostingRegressor(random_state=42)
gb.fit(X_train, y_train)


# Random Forest Regressor
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)


# --- Predictions ---
y_pred_gb = gb.predict(X_test)
y_pred_rf = rf.predict(X_test)


# --- Model Evaluation ---
mse_gb = mean_squared_error(y_test, y_pred_gb)
r2_gb = r2_score(y_test, y_pred_gb)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)


print(f"Gradient Boosting - MSE: {mse_gb:.4f}, R²: {r2_gb:.4f}")
print(f"Random Forest - MSE: {mse_rf:.4f}, R²: {r2_rf:.4f}")


# --- Visualize Results ---
# Residual Plot for Gradient Boosting
plt.figure(figsize=(8, 6))
residuals_gb = y_test - y_pred_gb
plt.scatter(y_pred_gb, residuals_gb, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted SFR')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted SFR (Gradient Boosting)')
plt.savefig('/home/pmqr7/data/residuals_gb.png')
plt.close()


# Feature Importance for Random Forest
plt.figure(figsize=(8, 6))
importances = rf.feature_importances_
feature_names = X.columns
sorted_idx = importances.argsort()
plt.barh(feature_names[sorted_idx], importances[sorted_idx])
plt.xlabel('Importance')
plt.title('Feature Importances (Random Forest)')
plt.savefig('/home/pmqr7/data/feature_importance_rf.png')
plt.close()


# --- Check Feature Importance for log_Mass_gas ---
print("\nFeature Importances (Random Forest):")
for name, importance in zip(feature_names, importances):
    print(f"{name}: {importance:.4f}")


# --- Save the Processed Dataset ---
df_clean.to_csv('/home/pmqr7/data/SDSSDR18_Final.csv', index=False)
print("Processed dataset saved to /home/pmqr7/data/SDSSDR18_Final.csv")
