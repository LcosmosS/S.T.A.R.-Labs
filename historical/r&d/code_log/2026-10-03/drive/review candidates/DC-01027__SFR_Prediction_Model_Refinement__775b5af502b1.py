# --- Feature Engineering ---
df['log_Mass_gas^2'] = df['log_Mass_gas'] ** 2
df['log_Mass_gas * nsa_mstar'] = df['log_Mass_gas'] * df['nsa_mstar']
df['log_Mass_gas * OH_Mar13_N2_Re_fit'] = df['log_Mass_gas'] * df['OH_Mar13_N2_Re_fit']


# --- Select Features ---
features = [
    'log_Mass_gas', 'nsa_mstar', 'OH_Mar13_N2_Re_fit', 'Av_gas_Re',
    'log_Mass_gas^2', 'log_Mass_gas * nsa_mstar', 'log_Mass_gas * OH_Mar13_N2_Re_fit'
]


X = df[features]
y = df['log_SFR_Ha']


# --- Train-Test Split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# --- Model Training ---
rf = RandomForestRegressor(random_state=42)
gb = GradientBoostingRegressor(random_state=42)


# --- Hyperparameter Tuning ---
param_grid_rf = {
    'n_estimators': [100, 200],
    'max_depth': [10, None],
    'min_samples_split': [2, 5]
}
param_grid_gb = {
    'learning_rate': [0.01, 0.1],
    'max_depth': [3, 5],
    'n_estimators': [100, 200]
}


print("Tuning Random Forest...")
grid_rf = GridSearchCV(rf, param_grid_rf, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_rf.fit(X_train, y_train)


print("Tuning Gradient Boosting...")
grid_gb = GridSearchCV(gb, param_grid_gb, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_gb.fit(X_train, y_train)


# --- Evaluation ---
models = {'Random Forest': grid_rf.best_estimator_, 'Gradient Boosting': grid_gb.best_estimator_}


for name, model in models.items():
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\n{name} Performance:")
    print(f"MSE: {mse:.4f}, R²: {r2:.4f}")


    # --- Feature Importances ---
    importances = model.feature_importances_
    plt.figure(figsize=(8, 5))
    sns.barplot(x=importances, y=X.columns)
    plt.title(f'{name} Feature Importance')
    plt.tight_layout()
    plt.show()


# --- Residuals Plot (Optional) ---
plt.figure(figsize=(8, 5))
residuals = y_test - grid_rf.predict(X_test)
plt.scatter(grid_rf.predict(X_test), residuals, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted SFR')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted (Random Forest)')
plt.show()
