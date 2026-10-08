import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from pysr import PySRRegressor  # Use PySR instead of gplearn
import warnings
from numpy.polynomial import Polynomial

warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_csv("merged_data.csv")

# Drop rows with missing target or excessive NaNs
df = df.dropna(subset=["log_SFR_Ha"])
df = df.dropna(axis=0, thresh=int(0.8 * df.shape[1]))
df.fillna(df.median(numeric_only=True), inplace=True)

# Step 1: Cosmo-Rank Construction
gz_df = df.copy()
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 
              'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)
gz_df['Num_w'] = gz_df['conf_prob']
scaler_rank = MinMaxScaler()
gz_df[['morph_sum_norm', 'Num_w_norm', 'nsa_z_norm']] = scaler_rank.fit_transform(
    gz_df[['morph_sum', 'Num_w', 'nsa_z']]
)
gz_df['cosmo_rank'] = (0.4 * gz_df['Num_w_norm'] + 
                       0.3 * gz_df['morph_sum_norm'] + 
                       0.3 * gz_df['nsa_z_norm'])
df['cosmo_rank'] = gz_df['cosmo_rank']

# Step 2: L_cosmo(s) Construction
alpha = -1.3
M_star = df['log_Mass_gas'].median()
df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
bins = pd.cut(df['nsa_z'], bins=20, labels=False) + 1
df['z_bin'] = bins
s_vals = [0.5, 1.0, 1.5, 2.0]
for s in s_vals:
    df[f'L_cosmo_s{s}'] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)
df['cosmo_rank_L'] = df['cosmo_rank'] * df['L_cosmo_s1.0']

# Plot L_cosmo(s) vs s
s_range = np.linspace(0.5, 2, 50)
L_vals = [df.groupby('z_bin')['a_n'].mean() / (np.arange(1, 21) ** s) for s in s_range]
L_vals = np.array([sum(l) for l in L_vals])
plt.plot(s_range, L_vals)
plt.xlabel("s")
plt.ylabel("L_cosmo(s)")
plt.title("L_cosmo(s) Behavior")
plt.savefig("L_cosmo_curve.png")
plt.close()

# Step 3: Define features and target
target = "log_SFR_Ha"
base_features = [
    "log_Mass_gas", "log_Mass", "Av_gas_Re", "Av_ssp_Re", 
    "OH_O3N2_cen", "OH_T04_cen", "OH_dop_cen", "Age_LW_Re_fit", 
    "ZH_LW_Re_fit", "Re_kpc", "vel_disp_Ha_cen", "Lambda_Re", 
    "Sigma_Mass_Re", "EW_Ha_cen", "Ha_Hb_cen"
]
df["mass_metallicity"] = df["log_Mass"] * df["OH_O3N2_cen"]
df["dust_metallicity"] = df["Av_gas_Re"] * df["OH_T04_cen"]
df["disp_mass_ratio"] = df["vel_disp_Ha_cen"] / (df["Sigma_Mass_Re"] + 1e-5)
df["age_metallicity"] = df["Age_LW_Re_fit"] * df["ZH_LW_Re_fit"]
df["sqrt_Re_kpc"] = np.sqrt(df["Re_kpc"] + 1e-5)
df["log_mass"] = np.log(df["log_Mass_gas"] + 1e-5)
df["BSD_likelihood"] = (
    df["log_Mass_gas"] * df["OH_O3N2_cen"] /
    (df["Av_gas_Re"] + 1e-5 + df["Age_LW_Re_fit"])
)
features = base_features + [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", 
    "age_metallicity", "sqrt_Re_kpc", "log_mass", "BSD_likelihood", 
    "cosmo_rank", "L_cosmo_s0.5", "L_cosmo_s1.0", "L_cosmo_s1.5", 
    "L_cosmo_s2.0", "cosmo_rank_L"
]

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
explainer_rf = shap.Explainer(rf, X_train_scaled)
shap_values_rf = explainer_rf(X_test_scaled)
explainer_gb = shap.Explainer(gb, X_train_scaled)
shap_values_gb = explainer_gb(X_test_scaled)
shap.summary_plot(shap_values_rf, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - Random Forest")
plt.tight_layout()
plt.savefig("shap_rf_summary.png")
plt.clf()
shap.summary_plot(shap_values_gb, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - Gradient Boosting")
plt.tight_layout()
plt.savefig("shap_gb_summary.png")
plt.clf()

# Symbolic Regression with PySR
symbolic_model = PySRRegressor(
    model_selection="best",
    niterations=40,
    binary_operators=["+", "-", "*", "/", "^2"],
    unary_operators=["exp", "log", "sqrt", "sin", "cos"],
    extra_sympy_mappings={"log": lambda x: np.log(np.abs(x) + 1e-5), "^2": lambda x: x**2},
    loss="loss(x, y) = (x - y)^2",
    maxsize=25,
    parsimony=0.0001,
    verbosity=1,
    random_state=42,
    procs=1
)
symbolic_model.fit(X_train_scaled, y_train)
y_pred_sym = symbolic_model.predict(X_test_scaled)
r2_sym = r2_score(y_test, y_pred_sym)
print(f"PySR R²: {r2_sym:.4f}")
print("Top PySR Equations:\n", symbolic_model.equations_.head())

# Save symbolic expression as polynomial fit plot
x