import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error


import sympy as sp


# === Load and clean data ===
df = pd.read_csv("pipe3d_data.csv")
features = ['log_Mass_gas', 'metallicity', 'dust_attenuation', 'SFR', 'stellar_mass', 'age_lightW', 'Av_ssp']
df = df[features].dropna()


# === Separate features and target ===
X = df.drop(columns='SFR')
y = df['SFR'].values


# === Standardize the features ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# === Dimensionality reduction for visualization ===
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)


# === Split the dataset ===
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# === Train Gradient Boosting Model ===
gb_model = GradientBoostingRegressor()
gb_model.fit(X_train, y_train)
gb_preds = gb_model.predict(X_test)


# === Train Random Forest Model ===
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)


# === Evaluation ===
print("\n--- Gradient Boosting ---")
print(f"R^2: {r2_score(y_test, gb_preds):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, gb_preds)):.4f}")


print("\n--- Random Forest ---")
print(f"R^2: {r2_score(y_test, rf_preds):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, rf_preds)):.4f}")


# === Visualize PCA projection ===
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=df['SFR'], palette='viridis')
plt.title("PCA Projection of Galactic Features")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.colorbar(label='SFR')
plt.grid(True)
plt.tight_layout()
plt.show()


# === Visualize Feature Importances ===
def plot_feature_importances(model, model_name):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    plt.figure(figsize=(8, 4))
    sns.barplot(x=[features[i] for i in indices], y=importances[indices])
    plt.title(f"{model_name} Feature Importances")
    plt.ylabel("Importance")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


plot_feature_importances(gb_model, "Gradient Boosting")
plot_feature_importances(rf_model, "Random Forest")


# === Estimate symbolic cosmic structure ===
x, y_sym = sp.symbols('x y')
L_cosmos_expr = x**3 + sp.Function('a')(x)*x + sp.Function('b')(x)
print(f"\nSymbolic form (L_cosmos): L(x) = {L_cosmos_expr}")


# === Compute pseudo-L(cosmos) from data ===
pseudo_L = np.sum(1 / (1 + df['SFR']))
print(f"\nPseudo L(cosmos) ≈ Σ 1/(1 + SFR) = {pseudo_L:.5f}")


# === Print placeholder symbolic SFR model ===
log_M, Z, Av = sp.symbols('log_M Z Av')
SFR_expr = log_M**2 + Z*Av - log_M*Z
print("\nSymbolic SFR model (hypothetical):")
sp.pretty_print(SFR_expr)
