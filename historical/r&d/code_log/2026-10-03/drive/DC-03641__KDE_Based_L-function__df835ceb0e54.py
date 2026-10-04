import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import psutil
import optuna
from pysr import PySRRegressor
import shap


# -------------------------------
# Helper: System Resource Monitor
def check_system_resources():
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu}%")
    print(f"Memory Usage: {memory.percent}%")
    return cpu, memory.percent


# -------------------------------
# Step 1: Load the GZ dataset
gz_df = pd.read_csv("GZ_gzdv1_2.csv", low_memory=False)
print("Columns in GZ DataFrame:", gz_df.columns)
print(gz_df.head())


# -------------------------------
# Step 2: Select and preprocess relevant features
selected_features = ['z', 'rMag', 'Ar', 'Pth100', 'Smooth', 'Featured']
gz_df = gz_df[selected_features].copy()


# Impute missing values
gz_df[selected_features] = SimpleImputer(strategy='mean').fit_transform(gz_df[selected_features])


# -------------------------------
# Step 3: Feature Engineering
# Create a morphology feature by summing Smooth and Featured
gz_df['morph_sum'] = gz_df[['Smooth', 'Featured']].sum(axis=1)


# Calculate dust-corrected rMag and then compute expected_SFR using a Kennicutt-Schmidt proxy
gz_df['dust_corrected_mag'] = gz_df['rMag'] - gz_df['Ar']
gz_df['expected_SFR'] = 1e-4 * (10 ** (0.4 * (22 - gz_df['dust_corrected_mag'])) ** 1.4)


# Clean expected_SFR: replace infinities with NaN and drop them
gz_df['expected_SFR'].replace([np.inf, -np.inf], np.nan, inplace=True)
gz_df.dropna(subset=['expected_SFR'], inplace=True)


# Define features and target
X = gz_df[['z', 'rMag', 'Ar', 'Pth100', 'morph_sum']]
y = gz_df['expected_SFR']


# -------------------------------
# Step 4: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# -------------------------------
# Step 5: Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# -------------------------------
# Step 6: Random Forest - Optuna
check_system_resources()


def objective_rf(trial):
    model = RandomForestRegressor(
        max_depth=trial.suggest_int("max_depth", 5, 30),
        n_estimators=trial.suggest_int("n_estimators", 50, 500),
        min_samples_split=trial.suggest_int("min_samples_split", 2, 20),
        random_state=42,
        n_jobs=2  # using 2 workers to balance memory use
    )
    return np.mean(cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=2))


study_rf = optuna.create_study(direction="maximize")
study_rf.optimize(objective_rf, n_trials=50)


best_rf = RandomForestRegressor(**study_rf.best_params, random_state=42, n_jobs=2)
best_rf.fit(X_train_scaled, y_train)


# -------------------------------
# Step 7: Gradient Boosting - Optuna
def objective_gb(trial):
    model = GradientBoostingRegressor(
        max_depth=trial.suggest_int("max_depth", 3, 20),
        n_estimators=trial.suggest_int("n_estimators", 50, 500),
        min_samples_split=trial.suggest_int("min_samples_split", 2, 20),
        learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        random_state=42
    )
    return np.mean(cross_val_score(model, X_train_scaled, y_train, cv=3, scoring='r2', n_jobs=2))


study_gb = optuna.create_study(direction="maximize")
study_gb.optimize(objective_gb, n_trials=50)


best_gb = GradientBoostingRegressor(**study_gb.best_params, random_state=42)
best_gb.fit(X_train_scaled, y_train)


# -------------------------------
# Step 8: Evaluate Models
y_pred_rf = best_rf.predict(X_test_scaled)
y_pred_gb = best_gb.predict(X_test_scaled)


print(f"Random Forest - MSE: {mean_squared_error(y_test, y_pred_rf):.4f}, R²: {r2_score(y_test, y_pred_rf):.4f}")
print(f"Gradient Boosting - MSE: {mean_squared_error(y_test, y_pred_gb):.4f}, R²: {r2_score(y_test, y_pred_gb):.4f}")


# -------------------------------
# Step 9: SHAP Analysis
explainer_rf = shap.TreeExplainer(best_rf)
shap_values_rf = explainer_rf.shap_values(X_test_scaled)
shap.summary_plot(shap_values_rf, X_test, feature_names=X.columns, show=False)
plt.title("SHAP Summary - Random Forest")
plt.savefig("shap_summary_rf.png")
plt.close()


explainer_gb = shap.TreeExplainer(best_gb)
shap_values_gb = explainer_gb.shap_values(X_test_scaled)
shap.summary_plot(shap_values_gb, X_test, feature_names=X.columns, show=False)
plt.title("SHAP Summary - Gradient Boosting")
plt.savefig("shap_summary_gb.png")
plt.close()


# Export SHAP values to CSV for further analysis
shap_values_df_rf = pd.DataFrame(shap_values_rf, columns=X.columns)
shap_values_df_rf.to_csv("shap_values_rf.csv", index=False)


shap_values_df_gb = pd.DataFrame(shap_values_gb, columns=X.columns)
shap_values_df_gb.to_csv("shap_values_gb.csv", index=False)


# -------------------------------\n# Step 10: Symbolic Regression with PySR\nsymbolic_model = PySRRegressor(\n    model_selection=\"best\",\n    niterations=500,\n    population_size=2000,\n    binary_operators=[\"+\", \"-\", \"*\", \"/\"],\n    unary_operators=[\"sqrt\", \"log\", \"exp\", \"sin\", \"cos\"],\n    loss=\"loss(x, y) = (x - y)^2\",\n    maxsize=30,\n    verbosity=1,\n    procs=4,\n    random_state=42\n)\n\nsymbolic_model.fit(X_train_scaled, y_train)\nprint(\"Best symbolic models:\\n\", symbolic_model)\n\n# Predict and evaluate symbolic regression model\ny_pysr_pred = symbolic_model.predict(X_test_scaled)\nprint(f\"PySR R² score: {r2_score(y_test, y_pysr_pred):.4f}\")\n\nsymbolic_model.save(\"pysr_model.pkl\")\nsymbolic_model.equations_.to_csv(\"pysr_equations.csv\", index=False)\nprint(\"Top PySR Equations:\\n\", symbolic_model.equations_.head())\n\n# -------------------------------\n# Step 11: Visual Comparison of R² Scores\nmodel_names = [\"Random Forest\", \"Gradient Boosting\", \"PySR\"]\nr2_scores = [\n    r2_score(y_test, y_pred_rf),\n    r2_score(y_test, y_pred_gb),\n    r2_score(y_test, y_pysr_pred)\n]\n\nplt.bar(model_names, r2_scores, color=['skyblue', 'salmon', 'limegreen'])\nplt.ylabel(\"R² Score\")\nplt.title(\"Model Performance Comparison\")\nplt.ylim(0, 1)\nplt.savefig(\"model_comparison_r2.png\")\nplt.close()\n\n# -------------------------------\n# Final system resource check\ncheck_system_resources()"
}
