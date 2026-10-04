import pandas as pd import numpy as np import shap import matplotlib.pyplot as plt import seaborn as sns from sklearn.model_selection import train_test_split from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor from sklearn.metrics import r2_score from sklearn.preprocessing import StandardScaler, MinMaxScaler from pysr import PySRRegressor import optuna import warnings
warnings.filterwarnings("ignore")
# Load dataset
df = pd.read_csv("merged_data.csv")
# Drop rows with missing target or excessive NaNs
df = df.dropna(subset=["log_SFR_Ha"]) df = df.dropna(axis=0, thresh=int(0.8 * df.shape[1])) df.fillna(df.median(numeric_only=True), inplace=True)
# Step 1: Cosmo-Rank Construction # Calculate morph_sum as sum of morphological probabilities
gz_df = df.copy() # Assuming df includes the Galaxy Zoo features morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)'] gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)
# Use conf_prob as Num_w (or replace with actual Num_w if defined differently)
gz_df['Num_w'] = gz_df['conf_prob']
# Normalize morph_sum, Num_w, and nsa_z
scaler_rank = MinMaxScaler() gz_df[['morph_sum_norm', 'Num_w_norm', 'nsa_z_norm']] = scaler_rank.fit_transform( gz_df[['morph_sum', 'Num_w', 'nsa_z']] )
# Define cosmo_rank: weighted average with redshift # 40% confidence, 30% morphology, 30% redshift
gz_df['cosmo_rank'] = (0.4 * gz_df['Num_w_norm'] + 0.3 * gz_df['morph_sum_norm'] + 0.3 * gz_df['nsa_z_norm'])
df['cosmo_rank'] = gz_df['cosmo_rank']
# Step 2: Define features and target
target = "log_SFR_Ha" base_features = [ "log_Mass_gas", "log_Mass", "Av_gas_Re", "Av_ssp_Re", "OH_O3N2_cen", "OH_T04_cen", "OH_dop_cen", "Age_LW_Re_fit", "ZH_LW_Re_fit", "Re_kpc", "vel_disp_Ha_cen", "Lambda_Re", "Sigma_Mass_Re", "EW_Ha_cen", "Ha_Hb_cen" ]
# Derived & interaction features
df["mass_metallicity"] = df["log_Mass"] * df["OH_O3N2_cen"] df["dust_metallicity"] = df["Av_gas_Re"] * df["OH_T04_cen"] df["disp_mass_ratio"] = df["vel_disp_Ha_cen"] / (df["Sigma_Mass_Re"] + 1e-5) df["age_metallicity"] = df["Age_LW_Re_fit"] * df["ZH_LW_Re_fit"] df["sqrt_Re_kpc"] = np.sqrt(df["Re_kpc"] + 1e-5) df["log_mass"] = np.log(df["log_Mass_gas"] + 1e-5) df["BSD_likelihood"] = ( df["log_Mass_gas"] * df["OH_O3N2_cen"] / (df["Av_gas_Re"] + 1e-5 + df["Age_LW_Re_fit"]) )
features = base_features + [ "mass_metallicity", "dust_metallicity", "disp_mass_ratio", "age_metallicity", "sqrt_Re_kpc", "log_mass", "BSD_likelihood", "cosmo_rank" ]
X = df[features] y = df[target]
# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Normalize features
scaler = StandardScaler() X_train_scaled = scaler.fit_transform(X_train) X_test_scaled = scaler.transform(X_test)
# Random Forest
rf = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42) rf.fit(X_train_scaled, y_train) y_pred_rf = rf.predict(X_test_scaled) r2_rf = r2_score(y_test, y_pred_rf)
# Gradient Boosting
gb = GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=6, random_state=42) gb.fit(X_train_scaled, y_train) y_pred_gb = gb.predict(X_test_scaled) r2_gb = r2_score(y_test, y_pred_gb)
print(f"R^2 Score (Random Forest): {r2_rf:.4f}") print(f"R^2 Score (Gradient Boosting): {r2_gb:.4f}")
# SHAP
explainer_rf = shap.Explainer(rf, X_train_scaled) shap_values_rf = explainer_rf(X_test_scaled)
explainer_gb = shap.Explainer(gb, X_train_scaled) shap_values_gb = explainer_gb(X_test_scaled)
shap.summary_plot(shap_values_rf, X_test_scaled, plot_type="bar", show=False) plt.title("SHAP Summary - Random Forest") plt.tight_layout() plt.savefig("shap_rf_summary.png") plt.clf()
shap.summary_plot(shap_values_gb, X_test_scaled, plot_type="bar", show=False) plt.title("SHAP Summary - Gradient Boosting") plt.tight_layout() plt.savefig("shap_gb_summary.png") plt.clf()
# PySR Symbolic Regression
X_pysr = X_train.copy() X_pysr["target"] = y_train
model = PySRRegressor( model_selection="best", niterations=100, binary_operators=["+", "-", "*", "/"], unary_operators=["exp", "log", "sqrt"], extra_sympy_mappings={"log": lambda x: np.log(np.abs(x) + 1e-5)}, loss="loss(x, y) = (x - y)^2", maxsize=20, verbosity=1, random_state=42, )
model.fit(X_train, y_train) print(model)
# Plot predictions vs true
y_pred_sym = model.predict(X_test) plt.scatter(y_test, y_pred_rf, alpha=0.5, label="RF", marker="o") plt.scatter(y_test, y_pred_gb, alpha=0.5, label="GB", marker="s") plt.scatter(y_test, y_pred_sym, alpha=0.5, label="PySR", marker="^") plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--") plt.xlabel("True log_SFR_Ha") plt.ylabel("Predicted") plt.title("Model Predictions vs True Values") plt.legend() plt.tight_layout() plt.savefig("model_comparison.png")
(myenv) root@BigsbyGaming:/home/pmqr7# python model18.py Detected IPython. Loading juliacall extension. See https://juliapy.github.io/PythonCall.jl/stable/compat/#IPython R^2 Score (Random Forest): 0.9261 R^2 Score (Gradient Boosting): 0.9463 97%|=================== | 1316/1358 [00:15<00:00]
