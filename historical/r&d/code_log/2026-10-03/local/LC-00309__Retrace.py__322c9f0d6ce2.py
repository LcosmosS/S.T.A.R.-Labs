import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# --- 1. Load Data ---
print("Loading dataset...")
df = pd.read_csv('compiled_sfr_dataset.csv')
print(f"Columns in compiled_sfr_dataset.csv: {list(df.columns)}")

# --- 2. Define Target and Features ---
target = 'log_SFR_Ha'
features = [
    'log_Mass_gas', 'nsa_mstar', 'log_Mass', 'vel_sigma_Re',
    'OH_Mar13_N2_Re_fit', 'Av_gas_Re', 'zcomp_1Mpc', 'LOGMSTARS',
    'SFR_PETRORAD_R'
]
print(f"Selected features: {features}")

# --- 3. Preprocess Data ---
# Drop rows where target is NaN
df = df.dropna(subset=[target])
print(f"Rows after filtering invalid {target}: {df.shape[0]}")

# Select features and target, dropping rows with NaN in features
X = df[features].dropna()
y = df.loc[X.index, target]
print(f"Rows after dropping NaN in features: {X.shape[0]}")

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- 4. Split Data ---
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
print(f"Training set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")

# --- 5. Model Training with Hyperparameter Tuning ---
rf_params = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

gb_params = {
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7],
    'n_estimators': [100, 200, 300]
}

print("Tuning Random Forest...")
rf = RandomForestRegressor(random_state=42)
rf_random = RandomizedSearchCV(
    rf, rf_params, n_iter=10, cv=3, scoring='neg_mean_squared_error',
    n_jobs=-1, random_state=42
)
rf_random.fit(X_train, y_train)
best_rf = rf_random.best_estimator_
print(f"Best RF params: {rf_random.best_params_}")

print("Tuning Gradient Boosting...")
gb = GradientBoostingRegressor(random_state=42, loss='huber')
gb_random = RandomizedSearchCV(
    gb, gb_params, n_iter=10, cv=3, scoring='neg_mean_squared_error',
    n_jobs=-1, random_state=42
)
gb_random.fit(X_train, y_train)
best_gb = gb_random.best_estimator_
print(f"Best GB params: {gb_random.best_params_}")

# --- 6. Evaluate Models ---
def evaluate_model(model, X_test, y_test, model_name):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    residuals = y_test - y_pred
    print(f"\n{model_name} Performance:")
    print(f"MSE: {mse:.4f}, R²: {r2:.4f}")
    return y_pred, residuals

rf_pred, rf_residuals = evaluate_model(best_rf, X_test, y_test, "Random Forest")
gb_pred, gb_residuals = evaluate_model(best_gb, X_test, y_test, "Gradient Boosting")

# --- 7. Residual Plots ---
plt.figure(figsize=(8, 6))
plt.scatter(rf_pred, rf_residuals, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted log_SFR_Ha')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted (Random Forest)')
plt.savefig('rf_residuals.png')
plt.close()

plt.figure(figsize=(8, 6))
plt.scatter(gb_pred, gb_residuals, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted log_SFR_Ha')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted (Gradient Boosting)')
plt.savefig('gb_residuals.png')
plt.close()

# --- 8. Feature Importance ---
rf_importance = pd.DataFrame({
    'Feature': features,
    'Importance': best_rf.feature_importances_
}).sort_values(by='Importance', ascending=False)
print("\nTop Features (Random Forest):")
print(rf_importance)

gb_importance = pd.DataFrame({
    'Feature': features,
    'Importance': best_gb.feature_importances_
}).sort_values(by='Importance', ascending=False)
print("\nTop Features (Gradient Boosting):")
print(gb_importance)