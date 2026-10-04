import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from pysr import PySRRegressor
import optuna
import warnings


warnings.filterwarnings("ignore")


# Load dataset
zoo_df = pd.read_csv("SDSSDR18_200000.csv")
merged_df = pd.read_csv("merged_output.csv")


# Merge identifiers from new Galaxy Zoo CSV by 'objID'
df = pd.merge(merged_df, zoo_df, on="objID", how="left")


# Drop rows with missing target or excessive NaNs
df = df.dropna(subset=["log_SFR_Ha"])
df = df.dropna(axis=0, thresh=int(0.8 * df.shape[1]))


# Fill remaining NaNs with feature medians
df.fillna(df.median(numeric_only=True), inplace=True)


# Define features and target
target = "log_SFR_Ha"
base_features = [
    "Smooth", "Featured", "Ar", "z", "rMag", "pS", "fM", "Pth100"
]


# Derived and interaction features
df["morph_sum"] = df[["Smooth", "Featured"]].sum(axis=1)
df["Ar_rMag_ratio"] = df["Ar"] / (df["rMag"] + 1e-5)
df["z_Pth100"] = df["z"] * df["Pth100"]
df["rMag_morph"] = df["rMag"] * df["morph_sum"]


features = base_features + ["morph_sum", "Ar_rMag_ratio", "z_Pth100", "rMag_morph"]


X = df[features]
y = df[target]


# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Random Forest
rf = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42)
rf.fit(X_train_scaled, y_train)
y_pred_rf = rf.predict(X_test_scaled)
r2_rf = r2_score(y_test, y_pred_rf)


# Gradient Boosting
gb = GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=6, random_state=42)
gb.fit(X_train_scaled, y_train)
y_pred_gb = gb.predict(X_test_scaled)
r2_gb = r2_score(y_test, y_pred_gb)


print(f"R^2 Score (Random Forest): {r2_rf:.4f}")
print(f"R^2 Score (Gradient Boosting): {r2_gb:.4f}")


# SHAP
explainer_rf = shap.Explainer(rf, X_train)
shap_values_rf = explainer_rf(X_test)


explainer_gb = shap.Explainer(gb, X_train)
shap_values_gb = explainer_gb(X_test)


shap.summary_plot(shap_values_rf, X_test, plot_type="bar", show=False)
plt.title("SHAP Summary - Random Forest")
plt.tight_layout()
plt.savefig("shap_rf_summary.png")
plt.clf()


shap.summary_plot(shap_values_gb, X_test, plot_type="bar", show=False)
plt.title("SHAP Summary - Gradient Boosting")
plt.tight_layout()
plt.savefig("shap_gb_summary.png")
plt.clf()


# PySR Symbolic Regression
X_pysr = X_train.copy()
X_pysr["target"] = y_train


model = PySRRegressor(
    model_selection="best",
    niterations=100,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["exp", "log", "sqrt"],
    extra_sympy_mappings={"log": lambda x: np.log(np.abs(x) + 1e-5)},
    loss="loss(x, y) = (x - y)^2",
    maxsize=20,
    verbosity=1,
    random_state=42,
)


model.fit(X_train_scaled, y_train)
print(model)


# Plot predictions vs true
y_pred_sym = model.predict(X_test_scaled)
plt.scatter(y_test, y_pred_rf, alpha=0.5, label="RF", marker="o")
plt.scatter(y_test, y_pred_gb, alpha=0.5, label="GB", marker="s")
plt.scatter(y_test, y_pred_sym, alpha=0.5, label="PySR", marker="^")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--")
plt.xlabel("True log_SFR_Ha")
plt.ylabel("Predicted")
plt.title("Model Predictions vs True Values")
plt.legend()
plt.tight_layout()
plt.savefig("model_comparison.png")
