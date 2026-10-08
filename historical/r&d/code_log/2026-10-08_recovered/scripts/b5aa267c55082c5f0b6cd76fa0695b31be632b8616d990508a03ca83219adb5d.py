# S.T.A.R. Model for predicting log_SFR_Ha using the STAR framework

# STAR: Symbolicly. Tuned. Astronomical. Regressors.
# - S: Symbolic-Regression via gplearn
# - T: Tuned hyperparameter optimization with Optuna
# - A: Astronomical predictions of star formation rates in galaxies
# - R: Regressors - HistGradientBoostingRegressor, LightGBM, XGBoost, CatBoost

import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import HistGradientBoostingRegressor
from gplearn.genetic import SymbolicRegressor
import optuna
import warnings
from numpy.polynomial import Polynomial
from scipy.spatial import cKDTree
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor

warnings.filterwarnings("ignore")

# List of CSV files
csv_files = [
    "ALLWISE_SDSSDR16.csv",
    "TwoMass_SDSSDR16.csv",
    "STARHORSE2021_SDSSDR16.csv",
    "GALAXGR6+7AIS_SDSSDR16.csv",
    "UKIDSSDR9LAS_SDSSDR16.csv",
    "GAIADR3AP_SDSSDR16.csv",
    "PanST2DR1_SDSSDR16.csv",
    "PanSTDR1_SDSSDR16.csv"
]

# Column mappings for each file
column_mappings = {
    "ALLWISE_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag', 'flux_Ha', 'e_flux_Ha', 'flux_Hb', 'flux_[OIII]5007', 'flux_[NII]6584'],
    "TwoMass_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'Jmag', 'Kmag', 'e_Jmag', 'e_Kmag'],
    "STARHORSE2021_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'logMass'],
    "GALAXGR6+7AIS_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS'],
    "UKIDSSDR9LAS_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS'],
    "GAIADR3AP_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS'],
    "PanST2DR1_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'kronRad', 'P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)', 'conf_prob', 'nsa_z'],
    "PanSTDR1_SDSSDR16.csv": ['RA_ICRS', 'DE_ICRS', 'kronRad', 'P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)', 'conf_prob', 'nsa_z']
}

# Function to standardize RA/Dec
def standardize_columns(df, cols):
    df = df[cols].rename(columns={"RA_ICRS": "objra_y", "DE_ICRS": "objdec"})
    return df

# Incremental merge
print("Starting incremental merge...")
merged_df = None
for i, file in enumerate(csv_files):
    print(f"Loading {file} ({i+1}/{len(csv_files)})...")
    try:
        df = pd.read_csv(file, usecols=column_mappings[file], low_memory=False)
        df = standardize_columns(df, column_mappings[file])
        print(f"Rows in {file}: {len(df)}, Columns: {len(df.columns)}")
    except ValueError as e:
        print(f"Error loading {file}: {e}. Check column names.")
        continue
    
    if merged_df is None:
        merged_df = df
    else:
        merged_df = merged_df.merge(df, on=['objra_y', 'objdec'], how='left', suffixes=('', f'_dup_{i}'))
        dup_cols = [col for col in merged_df.columns if f'_dup_{i}' in col]
        merged_df = merged_df.drop(columns=dup_cols)
    
    merged_df = merged_df.drop_duplicates(subset=['objra_y', 'objdec'], keep='first')
    print(f"Rows after merging {file}: {len(merged_df)}")
    
    # Save intermediate result
    temp_file = f"temp_merge_step_{i+1}.csv"
    merged_df.to_csv(temp_file, index=False)
    print(f"Saved to {temp_file}")

# Rename merged_df to df for processing
df = merged_df

# Ensure RA/Dec are numeric and impute NaN/infinities with medians
df['objra_y'] = pd.to_numeric(df['objra_y'], errors='coerce')
df['objdec'] = pd.to_numeric(df['objdec'], errors='coerce')
print(f"Initial df: objra_y dtype: {df['objra_y'].dtype}, objdec dtype: {df['objdec'].dtype}")
print(f"NaN in objra_y: {df['objra_y'].isna().sum()}, NaN in objdec: {df['objdec'].isna().sum()}")
df['objra_y'] = df['objra_y'].replace([np.inf, -np.inf], np.nan).fillna(df['objra_y'].median(skipna=True))
df['objdec'] = df['objdec'].replace([np.inf, -np.inf], np.nan).fillna(df['objdec'].median(skipna=True))
print(f"Rows after RA/Dec imputation: {len(df)}")

# Impute NaN/infinities for all numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    df[col] = df[col].replace([np.inf, -np.inf], np.nan).fillna(df[col].median(skipna=True))

# Recompute log_SFR_Ha and metallicity
flux_cols = ['flux_Ha', 'flux_Hb', 'flux_[OIII]5007', 'flux_[NII]6584', 'e_flux_Ha']
for col in flux_cols:
    print(f"NaN count in {col} after imputation: {df[col].isna().sum()}")

df['Ha_Hb_observed'] = df['flux_Ha'] / df['flux_Hb']
Ha_Hb_intrinsic = 2.86
k_Ha = 2.468
k_Hb = 3.634
df['A_Ha'] = 2.5 * np.log10(df['Ha_Hb_observed'] / Ha_Hb_intrinsic) * (k_Ha / (k_Hb - k_Ha))
df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * df['A_Ha'])
H0 = 70  # km/s/Mpc
c = 3e5  # km/s
df['DL'] = (c * df['zsp'] / H0) * 3.0856e24  # cm
df['L_Ha'] = df['flux_Ha_corr'] * 4 * np.pi * df['DL']**2  # erg/s
df['log_SFR_Ha_raw'] = np.log10(df['L_Ha'] * 7.9e-42)  # M_sun/yr
df['log_O3N2_raw'] = np.log10((df['flux_[OIII]5007'] / df['flux_Hb']) / (df['flux_[NII]6584'] / df['flux_Ha']))
df['OH_O3N2_raw'] = 8.533 - 0.214 * df['log_O3N2_raw']
print(f"NaN in L_Ha: {df['L_Ha'].isna().sum()}")
print(f"NaN in log_SFR_Ha_raw: {df['log_SFR_Ha_raw'].isna().sum()}")

# Add raw fluxes as features
df['log_flux_Ha'] = np.log10(df['flux_Ha'] + 1e-10)
df['log_flux_Hb'] = np.log10(df['flux_Hb'] + 1e-10)
df['log_flux_OIII_5007'] = np.log10(df['flux_[OIII]5007'] + 1e-10)
df['log_flux_NII_6584'] = np.log10(df['flux_[NII]6584'] + 1e-10)
df['log_e_flux_Ha'] = np.log10(df['e_flux_Ha'] + 1e-10)

# Add photometric colors
if 'umag' in df.columns:
    df['color_ug'] = df['umag'] - df['gmag']
    df['color_gr'] = df['gmag'] - df['rmag']
    df['color_ri'] = df['rmag'] - df['imag']
    df['color_iz'] = df['imag'] - df['zmag']
    df['e_color_ug'] = np.sqrt(df['e_umag']**2 + df['e_gmag']**2)
    df['e_color_gr'] = np.sqrt(df['e_gmag']**2 + df['e_rmag']**2)

if 'Jmag' in df.columns:
    df['color_JK'] = df['Jmag'] - df['Kmag']
    df['e_color_JK'] = np.sqrt(df['e_Jmag']**2 + df['e_Kmag']**2)

# Step 1: Cosmo-Rank Construction
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
if all(col in df.columns for col in morph_cols) and 'conf_prob' in df.columns and 'nsa_z' in df.columns:
    gz_df = df.copy()
    gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)
    gz_df['Num_w'] = gz_df['conf_prob']
    scaler_rank = MinMaxScaler()
    gz_df[['morph_sum_norm', 'Num_w_norm', 'nsa_z_norm']] = scaler_rank.fit_transform(
        gz_df[['morph_sum', 'Num_w', 'nsa_z']]
    )
    gz_df['cosmo_rank'] = (0.5 * gz_df['Num_w_norm'] + 0.3 * gz_df['morph_sum_norm'] + 0.2 * gz_df['nsa_z_norm'])
    df['cosmo_rank'] = gz_df['cosmo_rank']
else:
    print("Warning: Some morphology columns, conf_prob, or nsa_z missing. Skipping cosmo_rank.")

# Step 2: L_cosmo(s) Construction
alpha = -1.5
if 'logMass' in df.columns:
    df['log_Mass_gas'] = df['logMass']
    M_star = df['log_Mass_gas'].median()
    df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
    if 'kronRad' in df.columns:
        df['Re_kpc'] = df['kronRad']
        bins = pd.qcut(df['Re_kpc'], q=20, labels=False, duplicates='drop') + 1
        df['z_bin'] = bins
        n_bins = df['z_bin'].nunique()
        print(f"Number of unique bins after qcut: {n_bins}")
        print("Bin distribution for Re_kpc:")
        print(df['z_bin'].value_counts().sort_index())
        s_vals = [0.5, 1.0, 1.5, 2.0]
        for s in s_vals:
            col_name = f'L_cosmo_s_{s:.1f}'
            df[col_name] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)
        print("Columns after creating L_cosmo_s*:")
        print(df.columns.tolist())
    else:
        print("Warning: kronRad not found. Skipping L_cosmo_s* construction.")
else:
    print("Warning: logMass not found. Skipping L_cosmo_s* construction.")

# Adjust to 1–1.2M rows
target_min, target_max = 1000000, 1200000
print(f"Adjusting to {target_min}–{target_max} rows...")
if len(df) > target_max:
    df = df.sample(n=target_max, random_state=42)
elif len(df) < target_min:
    print(f"Warning: Only {len(df)} rows available, less than target {target_min}")
print(f"Final rows: {len(df)}")

# Verify NaN and infinities
nan_count = df.isna().sum().sum()
inf_count = np.isinf(df.select_dtypes(include=[np.number])).sum().sum()
print(f"Total NaN values: {nan_count}")
print(f"Total infinity values: {inf_count}")
print(f"Final columns: {len(df.columns)}")
print(f"Column names: {df.columns.tolist()}")

# Save final dataset
df.to_csv("merged_sdssdr16_dataset.csv", index=False)
print("Saved to merged_sdssdr16_dataset.csv")
# Fix plotting to use correct target
plt.scatter(df['L_cosmo_s_1.0'], df['log_SFR_Ha_raw'], alpha=0.5)
plt.xlabel("L_cosmo_s_1.0")
plt.ylabel("log_SFR_Ha_raw")
plt.title("L_cosmo_s_1.0 vs log_SFR_Ha_raw")
plt.savefig("L_cosmo_s1_vs_SFR.png")
plt.close()

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

# Step 3: Define features and target
target = "log_SFR_Ha"  # Adjust to "log_SFR_Ha_raw" if that’s your intended target
base_features = [
    "log_Mass_gas", "log_Mass", "Av_gas_Re", "Av_ssp_Re", 
    "OH_O3N2_cen", "OH_T04_cen", "OH_dop_cen", "Age_LW_Re_fit", 
    "ZH_LW_Re_fit", "Re_kpc", "vel_disp_Ha_cen", "Lambda_Re", 
    "Sigma_Mass_Re", "EW_Ha_cen", "Ha_Hb_cen"
]
# Assuming df is loaded earlier with 1,000,000 rows
print(f"Initial rows in df: {len(df)}")

# Global imputation before feature engineering
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].replace([np.inf, -np.inf], np.nan).fillna(df[numeric_cols].median(skipna=True))
print(f"Rows after global imputation: {len(df)}")

# Feature engineering
df["mass_metallicity"] = df["log_Mass"] * df["OH_O3N2_cen"]
df["dust_metallicity"] = df["Av_gas_Re"] * df["OH_T04_cen"]
df["disp_mass_ratio"] = df["vel_disp_Ha_cen"] / (df["Sigma_Mass_Re"] + 1e-5)
df["age_metallicity"] = df["Age_LW_Re_fit"] * df["ZH_LW_Re_fit"]
df["sqrt_Re_kpc"] = np.sqrt(df['Re_kpc'] + 1e-5)
df["log_mass"] = np.log(df["log_Mass_gas"] + 1e-5)
df["BSD_likelihood"] = (
    df["log_Mass_gas"] * df["OH_O3N2_cen"] /
    (df["Av_gas_Re"] + 1e-5 + df["Age_LW_Re_fit"])
)
df["cosmo_rank_mass"] = df["cosmo_rank"] * df["log_Mass"]
df["L_cosmo_s1_mass"] = df["L_cosmo_s_1.0"] * df["log_Mass"]
df["cosmo_rank_EW"] = df["cosmo_rank"] * df["EW_Ha_cen"]
df["L_cosmo_s1_EW"] = df["L_cosmo_s_1.0"] * df["EW_Ha_cen"]
df["cosmo_rank_scaled"] = df["cosmo_rank"] * 20
df["L_cosmo_s1_scaled"] = df["L_cosmo_s_1.0"] * 20
df["cosmo_rank_L_mass"] = df["cosmo_rank_L"] * df["log_Mass"]
df["L_cosmo_s1_metallicity"] = df["L_cosmo_s_1.0"] * df["OH_O3N2_cen"]
features = base_features + [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", 
    "age_metallicity", "sqrt_Re_kpc", "log_mass", "BSD_likelihood", 
    "cosmo_rank", "L_cosmo_s_0.5", "L_cosmo_s_1.5", "L_cosmo_s_2.0", 
    "cosmo_rank_L", "cosmo_rank_mass", "L_cosmo_s1_mass",
    "cosmo_rank_EW", "L_cosmo_s1_EW", "cosmo_rank_scaled", "L_cosmo_s1_scaled",
    "cosmo_rank_L_mass", "L_cosmo_s1_metallicity",
    "log_flux_Ha", "log_flux_Hb", "log_flux_OIII_5007", "log_flux_NII_6584", 
    "log_e_flux_Ha", "log_SFR_Ha_raw", "OH_O3N2_raw"
]
if 'color_ug' in df.columns:
    features.extend(["color_ug", "color_gr", "color_ri", "color_iz", "e_color_ug", "e_color_gr"])
if 'color_JK' in df.columns:
    features.extend(["color_JK", "e_color_JK"])

    # Select features and target
print(f"Features defined: {features}")
X = df[features]
y = df[target]
print(f"Rows after feature selection: {len(X)}")
print(f"NaN in y ({target}): {y.isna().sum()}")

# Filter to numeric columns only
numeric_features = [col for col in features if pd.api.types.is_numeric_dtype(X[col])]
X = X[numeric_features]
print(f"Numeric features selected: {numeric_features}")
print("Sample values:")
print(X.head())

# Clean X and y
X = X.replace([np.inf, -np.inf], np.nan)
print(f"Columns with NaN before imputation: {X.columns[X.isna().any()].tolist()}")
X = X.fillna(X.median())  # Impute NaN with column medians
print(f"Rows after X imputation: {len(X)}")
y = y.replace([np.inf, -np.inf], np.nan)
print(f"Rows before y.dropna(): {len(y)}")
y = y.dropna()
print(f"Rows after y.dropna(): {len(y)}")
mask = y.index.isin(X.index)
X = X.loc[mask]
y = y.loc[mask]
print(f"Rows after NaN/infinity cleaning: {len(X)}")

# Train/test split
if len(X) < 10:
    raise ValueError(f"Only {len(X)} rows after cleaning. Check data preprocessing.")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Verify inputs
print("NaN in X_train_scaled:", np.isnan(X_train_scaled).sum())
print("Inf in X_train_scaled:", np.isinf(X_train_scaled).sum())
print("NaN in y_train:", y_train.isna().sum())
print("Inf in y_train:", np.isinf(y_train).sum())

# Optuna optimization for HistGradientBoostingRegressor
def objective_hgb(trial):
    params = {
        'max_iter': trial.suggest_int('max_iter', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'l2_regularization': trial.suggest_float('l2_regularization', 0.1, 10.0),
        'max_leaf_nodes': trial.suggest_int('max_leaf_nodes', 20, 50),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 10, 30),
        'random_state': 42
    }
    model = HistGradientBoostingRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    mean_score = np.nanmean(scores)  # Handle NaN in scores
    if np.isnan(mean_score):
        print(f"HGB Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf

study_hgb = optuna.create_study(direction='maximize')
study_hgb.optimize(objective_hgb, n_trials=20)
best_params_hgb = study_hgb.best_params
print("Best HistGradientBoosting Parameters:", best_params_hgb)
print("Best HistGradientBoosting CV R²:", study_hgb.best_value)

# Train HistGradientBoostingRegressor
hgb = HistGradientBoostingRegressor(**best_params_hgb, random_state=42, n_jobs=2)
hgb.fit(X_train_scaled, y_train)
y_pred_hgb = hgb.predict(X_test_scaled)
r2_hgb = r2_score(y_test, y_pred_hgb)
cv_scores_hgb = cross_val_score(hgb, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"HistGradientBoosting 5-Fold CV R²: Mean = {cv_scores_hgb.mean():.4f}, Std = {cv_scores_hgb.std():.4f}")
print(f"R^2 Score (HistGradientBoosting, Test): {r2_hgb:.4f}")

# Optuna optimization for LightGBM
def objective_lgb(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'num_leaves': trial.suggest_int('num_leaves', 20, 50),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.1, 10.0),
        'random_state': 42,
        'verbose': -1
    }
    model = lgb.LGBMRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    mean_score = np.nanmean(scores)
    if np.isnan(mean_score):
        print(f"LGB Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf

study_lgb = optuna.create_study(direction='maximize')
study_lgb.optimize(objective_lgb, n_trials=20)
best_params_lgb = study_lgb.best_params
print("Best LightGBM Parameters:", best_params_lgb)
print("Best LightGBM CV R²:", study_lgb.best_value)

# Train LightGBM
lgb_model = lgb.LGBMRegressor(**best_params_lgb, random_state=42, verbose=-1)
lgb_model.fit(X_train_scaled, y_train)
y_pred_lgb = lgb_model.predict(X_test_scaled)
r2_lgb = r2_score(y_test, y_pred_lgb)
cv_scores_lgb = cross_val_score(lgb_model, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"LightGBM 5-Fold CV R²: Mean = {cv_scores_lgb.mean():.4f}, Std = {cv_scores_lgb.std():.4f}")
print(f"R^2 Score (LightGBM, Test): {r2_lgb:.4f}")

# XGBoost Optimization
def objective_xgb(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.1, 10.0),
        'random_state': 42
    }
    model = xgb.XGBRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    mean_score = np.nanmean(scores)
    if np.isnan(mean_score):
        print(f"XGB Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf

study_xgb = optuna.create_study(direction='maximize')
study_xgb.optimize(objective_xgb, n_trials=20)
best_params_xgb = study_xgb.best_params
print("Best XGBoost Parameters:", best_params_xgb)
print("Best XGBoost CV R²:", study_xgb.best_value)

# Train XGBoost
xgb_model = xgb.XGBRegressor(**best_params_xgb, random_state=42)
xgb_model.fit(X_train_scaled, y_train)
y_pred_xgb = xgb_model.predict(X_test_scaled)
r2_xgb = r2_score(y_test, y_pred_xgb)
cv_scores_xgb = cross_val_score(xgb_model, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"XGBoost 5-Fold CV R²: Mean = {cv_scores_xgb.mean():.4f}, Std = {cv_scores_xgb.std():.4f}")
print(f"R^2 Score (XGBoost, Test): {r2_xgb:.4f}")

# CatBoost Optimization
def objective_cat(trial):
    params = {
        'iterations': trial.suggest_int('iterations', 100, 500),
        'depth': trial.suggest_int('depth', 4, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10),
        'random_seed': 42,
        'verbose': 0
    }
    model = CatBoostRegressor(**params)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    mean_score = np.nanmean(scores)
    if np.isnan(mean_score):
        print(f"Cat Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf

study_cat = optuna.create_study(direction='maximize')
study_cat.optimize(objective_cat, n_trials=20)
best_params_cat = study_cat.best_params
print("Best CatBoost Parameters:", best_params_cat)
print("Best CatBoost CV R²:", study_cat.best_value)

# Train CatBoost
cat_model = CatBoostRegressor(**best_params_cat, random_seed=42, verbose=0)
cat_model.fit(X_train_scaled, y_train)
y_pred_cat = cat_model.predict(X_test_scaled)
r2_cat = r2_score(y_test, y_pred_cat)
cv_scores_cat = cross_val_score(cat_model, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"CatBoost 5-Fold CV R²: Mean = {cv_scores_cat.mean():.4f}, Std = {cv_scores_cat.std():.4f}")
print(f"R^2 Score (CatBoost, Test): {r2_cat:.4f}")

# SHAP for feature selection
explainer_hgb = shap.Explainer(hgb, X_train_scaled)
shap_values_hgb = explainer_hgb(X_test_scaled)
explainer_lgb = shap.Explainer(lgb_model, X_train_scaled)
shap_values_lgb = explainer_lgb(X_test_scaled)
explainer_xgb = shap.Explainer(xgb_model, X_train_scaled)
shap_values_xgb = explainer_xgb(X_test_scaled)
explainer_cat = shap.Explainer(cat_model, X_train_scaled)
shap_values_cat = explainer_cat(X_test_scaled)

# Compute SHAP values for all models
explainer_hgb = shap.Explainer(hgb, X_train_scaled)  # Define explainer first
shap_values_hgb = explainer_hgb(X_test_scaled)       # Then compute SHAP values

explainer_lgb = shap.Explainer(lgb_model, X_train_scaled)
shap_values_lgb = explainer_lgb(X_test_scaled)

explainer_xgb = shap.Explainer(xgb_model, X_train_scaled)
shap_values_xgb = explainer_xgb(X_test_scaled)

explainer_cat = shap.Explainer(cat_model, X_train_scaled)
shap_values_cat = explainer_cat(X_test_scaled)

# SHAP summary plots
shap.summary_plot(shap_values_hgb, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - HistGradientBoosting")
plt.tight_layout()
plt.savefig("shap_hgb_summary.png")
plt.clf()

shap.summary_plot(shap_values_lgb, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - LightGBM")
plt.tight_layout()
plt.savefig("shap_lgb_summary.png")
plt.clf()

shap.summary_plot(shap_values_xgb, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - XGBoost")
plt.tight_layout()
plt.savefig("shap_xgb_summary.png")
plt.clf()

shap.summary_plot(shap_values_cat, X_test_scaled, plot_type="bar", show=False)
plt.title("SHAP Summary - CatBoost")
plt.tight_layout()
plt.savefig("shap_cat_summary.png")
plt.clf()  # Fixed: Added closing parenthesis

