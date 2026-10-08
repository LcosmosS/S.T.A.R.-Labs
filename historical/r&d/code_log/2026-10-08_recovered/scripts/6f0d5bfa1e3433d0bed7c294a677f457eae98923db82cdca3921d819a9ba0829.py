import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from gplearn.genetic import SymbolicRegressor
import warnings
from numpy.polynomial import Polynomial

warnings.filterwarnings("ignore")

# Load raw dataset
df = pd.read_csv("merged_data.csv")

# Step 1: Initial Data Inspection and Robust Handling
# Convert relevant columns to numeric, coercing errors to NaN
numeric_cols = ['log_SFR_Ha', 'log_Mass_gas', 'Re_kpc', 'nsa_z', 'conf_prob', 'log_Mass',
                'Av_gas_Re', 'Av_ssp_Re', 'OH_O3N2_cen', 'OH_T04_cen', 'OH_dop_cen',
                'Age_LW_Re_fit', 'ZH_LW_Re_fit', 'vel_disp_Ha_cen', 'Lambda_Re',
                'Sigma_Mass_Re', 'EW_Ha_cen', 'Ha_Hb_cen']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Impute missing values in the target (log_SFR_Ha)
df['log_SFR_Ha_imputed'] = df['log_SFR_Ha'].isna()  # Track imputed rows
df['log_SFR_Ha'] = df['log_SFR_Ha'].fillna(df['log_SFR_Ha'].median())
print(f"Number of rows with imputed log_SFR_Ha: {df['log_SFR_Ha_imputed'].sum()}")

# Impute missing values in other numeric columns with median
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Step 2: Cosmo-Rank Construction
gz_df = df.copy()
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 
              'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
# Ensure morph_cols are numeric
for col in morph_cols:
    gz_df[col] = pd.to_numeric(gz_df[col], errors='coerce').fillna(0)
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)
gz_df['Num_w'] = gz_df['conf_prob']
scaler_rank = MinMaxScaler()
# Handle NaN/infinite values before scaling
gz_df[['morph_sum', 'Num_w', 'nsa_z']] = gz_df[['morph_sum', 'Num_w', 'nsa_z']].replace([np.inf, -np.inf], np.nan)
gz_df[['morph_sum_norm', 'Num_w_norm', 'nsa_z_norm']] = scaler_rank.fit_transform(
    gz_df[['morph_sum', 'Num_w', 'nsa_z']].fillna(0)
)
gz_df['cosmo_rank'] = (0.5 * gz_df['Num_w_norm'] + 
                       0.3 * gz_df['morph_sum_norm'] + 
                       0.2 * gz_df['nsa_z_norm'])
df['cosmo_rank'] = gz_df['cosmo_rank']
# Handle NaN/infinite in cosmo_rank
df['cosmo_rank'] = df['cosmo_rank'].replace([np.inf, -np.inf], np.nan).fillna(0)

# Step 3: L_cosmo(s) Construction
alpha = -1.5
M_star = df['log_Mass_gas'].median()
# Handle potential NaN/infinite values in log_Mass_gas
df['log_Mass_gas'] = df['log_Mass_gas'].replace([np.inf, -np.inf], np.nan).fillna(df['log_Mass_gas'].median())
df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
# Use quantile-based binning
bins = pd.qcut(df['Re_kpc'], q=20, labels=False, duplicates='drop') + 1
df['z_bin'] = bins
n_bins = df['z_bin'].nunique()
print(f"Number of unique bins after qcut: {n_bins}")
print("Bin distribution for Re_kpc (after qcut):")
print(df['z_bin'].value_counts().sort_index())

# Compute L_cosmo(s) for multiple s values
s_vals = [0.5, 1.0, 1.5, 2.0]
s_range = np.linspace(0.5, 2, 50)
for s in s_vals:
    col_name = f'L_cosmo_s_{s:.1f}'
    # Compute grouped means and broadcast to original DataFrame
    grouped_means = df.groupby('z_bin')['a_n'].mean()
    df[col_name] = df['z_bin'].map(grouped_means) / (df['z_bin'] ** s)
    # Handle NaN/infinite values
    df[col_name] = df[col_name].replace([np.inf, -np.inf], np.nan).fillna(0)

# Debug: Check columns
print("Columns after creating L_cosmo_s*:")
print(df.columns.tolist())

# Check for NaN/infinite values before creating cosmo_rank_L
print("Checking for NaN/infinite values in cosmo_rank and L_cosmo_s_1.0:")
print("cosmo_rank NaN count:", df['cosmo_rank'].isna().sum())
print("L_cosmo_s_1.0 NaN count:", df['L_cosmo_s_1.0'].isna().sum())
print("cosmo_rank infinite count:", np.isinf(df['cosmo_rank']).sum())
print("L_cosmo_s_1.0 infinite count:", np.isinf(df['L_cosmo_s_1.0']).sum())

# Create cosmo_rank_L and handle NaN/infinite values
df['cosmo_rank_L'] = df['cosmo_rank'] * df['L_cosmo_s_1.0']
df['cosmo_rank_L'] = df['cosmo_rank_L'].replace([np.inf, -np.inf], np.nan).fillna(0)
print("cosmo_rank_L created, NaN count:", df['cosmo_rank_L'].isna().sum())

# Plot L_cosmo(s) vs s
grouped_means = df.groupby('z_bin')['a_n'].mean().reindex(range(1, n_bins + 1), fill_value=0)
L_vals = [grouped_means / (np.arange(1, n_bins + 1) ** s) for s in s_range]
L_vals = np.array([sum(l) for l in L_vals])
plt.plot(s_range, L_vals)
plt.xlabel("s")
plt.ylabel("L_cosmo(s)")
plt.title("L_cosmo(s) Behavior")
plt.savefig("L_cosmo_curve.png")
plt.close()

# Scatter plot of L_cosmo_s_1.0 vs log_SFR_Ha
plt.scatter(df['L_cosmo_s_1.0'], df['log_SFR_Ha'], alpha=0.5)
plt.xlabel("L_cosmo_s_1.0")
plt.ylabel("log_SFR_Ha")
plt.title("L_cosmo_s_1.0 vs log_SFR_Ha")
plt.savefig("L_cosmo_s1_vs_SFR.png")
plt.close()

# Step 4: Define features and target
target = "log_SFR_Ha"
base_features = [
    "log_Mass_gas", "log_Mass", "Av_gas_Re", "Av_ssp_Re", 
    "OH_O3N2_cen", "OH_T04_cen", "OH_dop_cen", "Age_LW_Re_fit", 
    "ZH_LW_Re_fit", "Re_kpc", "vel_disp_Ha_cen", "Lambda_Re", 
    "Sigma_Mass_Re", "EW_Ha_cen", "Ha_Hb_cen"
]
# Create derived features with robust handling
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
# Boost BSD features with interactions and scaling
df["cosmo_rank_mass"] = df["cosmo_rank"] * df["log_Mass"]
df["L_cosmo_s1_mass"] = df["L_cosmo_s_1.0"] * df["log_Mass"]
df["cosmo_rank_EW"] = df["cosmo_rank"] * df["EW_Ha_cen"]
df["L_cosmo_s1_EW"] = df["L_cosmo_s_1.0"] * df["EW_Ha_cen"]
df["cosmo_rank_scaled"] = df["cosmo_rank"] * 20
df["L_cosmo_s1_scaled"] = df["L_cosmo_s_1.0"] * 20
df["cosmo_rank_L_mass"] = df["cosmo_rank_L"] * df["log_Mass"]
df["L_cosmo_s1_metallicity"] = df["L_cosmo_s_1.0"] * df["OH_O3N2_cen"]

# Handle NaN/infinite values in derived features
derived_features = ["mass_metallicity", "dust_metallicity", "disp_mass_ratio", 
                    "age_metallicity", "sqrt_Re_kpc", "log_mass", "BSD_likelihood",
                    "cosmo_rank_mass", "L_cosmo_s1_mass", "cosmo_rank_EW", 
                    "L_cosmo_s1_EW", "cosmo_rank_scaled", "L_cosmo_s1_scaled",
                    "cosmo_rank_L_mass", "L_cosmo_s1_metallicity"]
for col in derived_features:
    df[col] = df[col].replace([np.inf, -np.inf], np.nan).fillna(0)

features = base_features + derived_features + [
    "cosmo_rank", "L_cosmo_s_0.5", "L_cosmo_s_1.0", "L_cosmo_s_1.5", 
    "L_cosmo_s_2.0", "cosmo_rank_L"
]

X = df[features]
y = df[target]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features
scaler = StandardScaler()
# Replace NaN/infinite values before scaling
X_train = X_train.replace([np.inf, -np.inf], np.nan).fillna(0)
X_test = X_test.replace([np.inf, -np.inf], np.nan).fillna(0)
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

# SHAP for feature selection
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

# Feature selection based on SHAP
shap_values_rf_mean = np.abs(shap_values_rf.values).mean(axis=0)
feature_importance = pd.DataFrame({"feature": features, "importance": shap_values_rf_mean})
feature_importance = feature_importance.sort_values("importance", ascending=False)
top_features = feature_importance["feature"].head(10).tolist()
# Ensure BSD features are included
bsd_features = ["cosmo_rank", "L_cosmo_s_1.0", "cosmo_rank_L", "cosmo_rank_scaled", "L_cosmo_s1_scaled", "cosmo_rank_L_mass", "L_cosmo_s1_metallicity"]
for bsd_feature in bsd_features:
    if bsd_feature not in top_features:
        top_features.append(bsd_feature)
X_selected = df[top_features]
X_train_selected, X_test_selected, _, _ = train_test_split(X_selected, y, test_size=0.2, random_state=42)
X_train_selected_scaled = scaler.fit_transform(X_train_selected.replace([np.inf, -np.inf], np.nan).fillna(0))
X_test_selected_scaled = scaler.transform(X_test_selected.replace([np.inf, -np.inf], np.nan).fillna(0))

# Symbolic Regression with gplearn
symbolic_model = SymbolicRegressor(
    population_size=3000,
    generations=150,
    stopping_criteria=0.01,
    p_crossover=0.7,
    p_subtree_mutation=0.1,
    p_hoist_mutation=0.05,
    p_point_mutation=0.1,
    max_samples=0.9,
    verbose=1,
    parsimony_coefficient=0.0001,
    random_state=42,
    n_jobs=-1,
    function_set=('add', 'sub', 'mul', 'div', 'sqrt', 'log', 'sin', 'cos')
)
symbolic_model.fit(X_train_selected_scaled, y_train)
y_pred_sym = symbolic_model.predict(X_test_selected_scaled)
r2_sym = r2_score(y_test, y_pred_sym)
print(f"gplearn R²: {r2_sym:.4f}")
print("Symbolic Expression:")
print(symbolic_model._program)

# Save symbolic expression as polynomial fit plot
x = np.linspace(min(y_test), max(y_test), 500)
y_expr = symbolic_model.predict(scaler.transform(np.tile(X_test_selected.mean().values, (500,1))))
p = Polynomial.fit(y_test, y_pred_sym, deg=3)
plt.plot(*p.linspace(), label="Polynomial Fit")
plt.scatter(y_test, y_pred_sym, s=10, alpha=0.5, label="Symbolic Predictions")
plt.xlabel("True log_SFR_Ha")
plt.ylabel("Predicted log_SFR_Ha")
plt.title("Symbolic Regression Fit")
plt.legend()
plt.tight_layout()
plt.savefig("gplearn_expression_plot.png")
plt.clf()

# Plot predictions vs true
plt.scatter(y_test, y_pred_rf, alpha=0.5, label="RF", marker="o")
plt.scatter(y_test, y_pred_gb, alpha=0.5, label="GB", marker="s")
plt.scatter(y_test, y_pred_sym, alpha=0.5, label="Symbolic", marker="^")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--")
plt.xlabel("True log_SFR_Ha")
plt.ylabel("Predicted")
plt.title("Model Predictions vs True Values")
plt.legend()
plt.tight_layout()
plt.savefig("model_comparison.png")
plt.clf()

# Residuals and Correlation Analysis
residuals = pd.DataFrame({
    "True": y_teimport pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from gplearn.genetic import SymbolicRegressor
import optuna
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
# Calculate morph_sum as sum of morphological probabilities
gz_df = df.copy()  # Assuming df includes the Galaxy Zoo features
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 
              'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)

# Use conf_prob as Num_w (or replace with actual Num_w if defined differently)
gz_df['Num_w'] = gz_df['conf_prob']

# Normalize morph_sum, Num_w, and nsa_z
scaler_rank = MinMaxScaler()
gz_df[['morph_sum_norm', 'Num_w_norm', 'nsa_z_norm']] = scaler_rank.fit_transform(
    gz_df[['morph_sum', 'Num_w', 'nsa_z']]
)

# Define cosmo_rank: weighted average with redshift
# 40% confidence, 30% morphology, 30% redshift
gz_df['cosmo_rank'] = (0.4 * gz_df['Num_w_norm'] + 
                       0.3 * gz_df['morph_sum_norm'] + 
                       0.3 * gz_df['nsa_z_norm'])

df['cosmo_rank'] = gz_df['cosmo_rank']

# Step 2: L_cosmo(s) Construction
# Schechter-inspired a_n
alpha = -1.3
M_star = df['log_Mass_gas'].median()
df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))

# Bin by redshift for physical n
bins = pd.cut(df['nsa_z'], bins=20, labels=False) + 1  # 1 to 20
df['z_bin'] = bins

# Compute L_cosmo(s) for multiple s values
s_vals = [0.5, 1.0, 1.5, 2.0]
for s in s_vals:
    df[f'L_cosmo_s{s}'] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)

# Plot L_cosmo(s) vs s
L_vals = [df.groupby('z_bin')['a_n'].mean() / (np.arange(1, 21) ** s) for s in np.linspace(0.5, 2, 50)]
L_vals = np.array([sum(l) for l in L_vals])
plt.plot(np.linspace(0.5, 2, 50), L_vals)
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

# Derived & interaction features
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
df["cosmo_rank_L"] = df["cosmo_rank"] * df["log_Mass_gas"]  # Cosmo rank interaction with mass (example)

# Include L_cosmo_s0.5, L_cosmo_s1.0, L_cosmo_s1.5, L_cosmo_s2.0 as features
features = base_features + [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", 
    "age_metallicity", "sqrt_Re_kpc", "log_mass", "BSD_likelihood", 
    "cosmo_rank", "cosmo_rank_L", "L_cosmo_s0.5", "L_cosmo_s1.0", "L_cosmo_s1.5", "L_cosmo_s2.0"
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

# Symbolic Regression with gplearn
symbolic_model = SymbolicRegressor(
    population_size=1000,
    generations=20,
    stopping_criteria=0.01,
    p_crossover=0.7,
    p_subtree_mutation=0.1,
    p_hoist_mutation=0.05,
    p_point_mutation=0.1,
    max_samples=0.9,
    verbose=1,
    parsimony_coefficient=0.01,
    random_state=42,
    n_jobs=-1
)
symbolic_model.fit(X_train_scaled, y_train)
y_pred_sym = symbolic_model.predict(X_test_scaled)

# Print the symbolic expression
print("Symbolic Expression:")
print(symbolic_model._program)

# Save symbolic expression as polynomial fit plot
x = np.linspace(min(y_test), max(y_test), 500)
y_expr = symbolic_model.predict(scaler.transform(np.tile(X_test.mean().values, (500,1))))
p = Polynomial.fit(y_test, y_pred_sym, deg=3)
plt.plot(*p.linspace(), label="Polynomial Fit")
plt.scatter(y_test, y_pred_sym, s=10, alpha=0.5, label="Symbolic Predictions")
plt.xlabel("True log_SFR_Ha")
plt.ylabel("Predicted log_SFR_Ha")
plt.title("Symbolic Regression Fit")
plt.legend()
plt.tight_layout()
plt.savefig("pysr_expression_plot.png")
plt.clf()

# Plot predictions vs true
plt.scatter(y_test, y_pred_rf, alpha=0.5, label="RF", marker="o")
plt.scatter(y_test, y_pred_gb, alpha=0.5, label="GB", marker="s")
plt.scatter(y_test, y_pred_sym, alpha=0.5, label="Symbolic", marker="^")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--")
plt.xlabel("True log_SFR_Ha")
plt.ylabel("Predicted")
plt.title("Model Predictions vs True Values")
plt.legend()
plt.tight_layout()
plt.savefig("model_comparison.png")
st,
    "RF": y_pred_rf - y_test,
    "GB": y_pred_gb - y_test,
    "Symbolic": y_pred_sym - y_test,
    "cosmo_rank": X_test["cosmo_rank"],
    "L_cosmo_s1": X_test["L_cosmo_s_1.0"]
})
sns.scatterplot(data=residuals, x="True", y="Symbolic", hue="cosmo_rank", size="L_cosmo_s1", alpha=0.6)
plt.axhline(0, color="black", linestyle="--")
plt.title("Symbolic Residuals vs True log_SFR_Ha")
plt.savefig("residuals_sym.png")
plt.clf()

print("Correlation of BSD Features with Residuals:")
print(residuals[["RF", "GB", "Symbolic", "cosmo_rank", "L_cosmo_s1"]].corr()[["RF", "GB", "Symbolic"]])