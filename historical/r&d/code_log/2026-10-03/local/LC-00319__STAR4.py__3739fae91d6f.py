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

def clean_df(df, fill_method='median'):
    """Replace inf/-inf with NaN and fill NaNs with median or zero."""
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    if fill_method == 'median':
        df.fillna(df.median(numeric_only=True), inplace=True)
    elif fill_method == 'zero':
        df.fillna(0, inplace=True)
    nan_cols = df.columns[df.isna().any()].tolist()
    if nan_cols:
        print(f"Remaining NaN columns after cleaning: {nan_cols}")
    return df

def safe_log(x, min_val=1e-10):
    """Safe logarithm to prevent NaNs from zero or negative values."""
    return np.log10(np.clip(x, min_val, None))

# Load the original dataset and ensure RA/Dec are numeric
df = pd.read_csv("merged_data.csv")
df['objra_y'] = pd.to_numeric(df['objra_y'], errors='coerce')
df['objdec'] = pd.to_numeric(df['objdec'], errors='coerce')
df = clean_df(df)  # Initial cleaning
print(f"Initial df: objra_y dtype: {df['objra_y'].dtype}, objdec dtype: {df['objdec'].dtype}")
print(f"NaN in objra_y: {df['objra_y'].isna().sum()}, NaN in objdec: {df['objdec'].isna().sum()}")

# Load and merge SDSS datasets
sdss_dr16 = pd.read_csv("V154sdss16.csv")
sdss_dr12 = pd.read_csv("V147sdss12.csv")
sdss_merged = pd.merge(
    sdss_dr16[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']],
    sdss_dr12[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']],
    on='objID', how='outer', suffixes=('_dr16', '_dr12')
)
sdss_merged['RA_ICRS'] = sdss_merged['RA_ICRS_dr16'].combine_first(sdss_merged['RA_ICRS_dr12'])
sdss_merged['DE_ICRS'] = sdss_merged['DE_ICRS_dr16'].combine_first(sdss_merged['DE_ICRS_dr12'])
sdss_merged['zsp'] = sdss_merged['zsp_dr16'].combine_first(sdss_merged['zsp_dr12'])
sdss_merged['umag'] = sdss_merged['umag_dr16'].combine_first(sdss_merged['umag_dr12'])
sdss_merged['gmag'] = sdss_merged['gmag_dr16'].combine_first(sdss_merged['gmag_dr12'])
sdss_merged['rmag'] = sdss_merged['rmag_dr16'].combine_first(sdss_merged['rmag_dr12'])
sdss_merged['imag'] = sdss_merged['imag_dr16'].combine_first(sdss_merged['imag_dr12'])
sdss_merged['zmag'] = sdss_merged['zmag_dr16'].combine_first(sdss_merged['zmag_dr12'])
sdss_merged['e_umag'] = sdss_merged['e_umag_dr16'].combine_first(sdss_merged['e_umag_dr12'])
sdss_merged['e_gmag'] = sdss_merged['e_gmag_dr16'].combine_first(sdss_merged['e_gmag_dr12'])
sdss_merged['e_rmag'] = sdss_merged['e_rmag_dr16'].combine_first(sdss_merged['e_rmag_dr12'])
sdss_merged['e_imag'] = sdss_merged['e_imag_dr16'].combine_first(sdss_merged['e_imag_dr12'])
sdss_merged['e_zmag'] = sdss_merged['e_zmag_dr16'].combine_first(sdss_merged['e_zmag_dr12'])
sdss_merged = sdss_merged[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']]
sdss_merged = clean_df(sdss_merged)
sdss_merged.to_csv("sdss_merged.csv", index=False)
print(f"Merged SDSS dataset created with {len(sdss_merged)} rows.")

# Cross-match functions
def clean_coordinates(df, ra_col, dec_col):
    initial_len = len(df)
    mask = (df[ra_col].notna() & df[dec_col].notna() & np.isfinite(df[ra_col]) & np.isfinite(df[dec_col]))
    df_cleaned = df[mask].copy()
    print(f"Removed {initial_len - len(df_cleaned)} rows due to NaN or inf in {ra_col} or {dec_col}")
    return df_cleaned

def deg_to_rad(df, ra_col, dec_col):
    df['ra_rad'] = np.radians(df[ra_col])
    df['dec_rad'] = np.radians(df[dec_col])
    return df

def cross_match(df1, df2, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec=10.0):
    df1_cleaned = clean_coordinates(df1, ra_col1, dec_col1)
    df2_cleaned = clean_coordinates(df2, ra_col2, dec_col2)
    if len(df1_cleaned) == 0 or len(df2_cleaned) == 0:
        print("One of the DataFrames is empty after cleaning. Cannot perform cross-match.")
        return df1_cleaned, pd.DataFrame()
    df1_cleaned = deg_to_rad(df1_cleaned, ra_col1, dec_col1)
    df2_cleaned = deg_to_rad(df2_cleaned, ra_col2, dec_col2)
    coords1 = np.array([df1_cleaned['ra_rad'], df1_cleaned['dec_rad']]).T
    coords2 = np.array([df2_cleaned['ra_rad'], df2_cleaned['dec_rad']]).T
    tree = cKDTree(coords2)
    max_dist = np.radians(max_dist_arcsec / 3600.0)
    dist, idx = tree.query(coords1, k=1, distance_upper_bound=max_dist)
    matched = dist < max_dist
    df1_matched = df1_cleaned[matched].copy()
    df2_matched = df2_cleaned.iloc[idx[matched]].copy()
    df1_matched = df1_matched.reset_index(drop=True)
    df2_matched = df2_matched.reset_index(drop=True)
    return df1_matched, df2_matched

def cross_match_in_chunks(df1, filepath, ra_col1, dec_col1, ra_col2, dec_col2, columns_to_keep, max_dist_arcsec=10.0, chunksize=100000):
    df1[ra_col1] = pd.to_numeric(df1[ra_col1], errors='coerce')
    df1[dec_col1] = pd.to_numeric(df1[dec_col1], errors='coerce')
    min_ra, max_ra = df1[ra_col1].min() - 0.1, df1[ra_col1].max() + 0.1
    min_dec, max_dec = df1[dec_col1].min() - 0.1, df1[dec_col1].max() + 0.1
    if pd.isna([min_ra, max_ra, min_dec, max_dec]).any():
        min_ra, max_ra, min_dec, max_dec = 0, 360, -90, 90
    matched_df2_list = []
    usecols = [ra_col2, dec_col2] + columns_to_keep
    chunk_reader = pd.read_csv(filepath, chunksize=chunksize, usecols=usecols, on_bad_lines='warn')
    for i, chunk in enumerate(chunk_reader):
        chunk = clean_df(chunk)
        chunk_filtered = chunk[
            (chunk[ra_col2] >= min_ra) & (chunk[ra_col2] <= max_ra) &
            (chunk[dec_col2] >= min_dec) & (chunk[dec_col2] <= max_dec)
        ]
        if len(chunk_filtered) == 0:
            continue
        _, matched_df2 = cross_match(df1, chunk_filtered, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec)
        if len(matched_df2) > 0:
            matched_df2_list.append(matched_df2[columns_to_keep])
    if len(matched_df2_list) == 0:
        return df1, pd.DataFrame()
    matched_df2 = pd.concat(matched_df2_list, ignore_index=True)
    return df1, matched_df2

# Cross-matching
df_original = df.copy()
df, sdss_matched = cross_match(df, sdss_merged, 'objra_y', 'objdec', 'RA_ICRS', 'DE_ICRS')
sdss_columns = ['zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']
if len(df) == 0:
    df = df_original.copy()
    df['zsp'] = df['nsa_z']
else:
    sdss_matched = clean_df(sdss_matched)
    df = pd.concat([df, sdss_matched[sdss_columns]], axis=1)

twomass_columns = ['Jmag', 'Hmag', 'Kmag', 'e_Jmag', 'e_Hmag', 'e_Kmag']
df, twomass_matched = cross_match_in_chunks(df, "2Mass.csv", 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000', twomass_columns)
if len(twomass_matched) > 0:
    twomass_matched = clean_df(twomass_matched)
    df = pd.concat([df, twomass_matched[twomass_columns]], axis=1)

gama_columns = ['UmAB', 'BmAB', 'VmAB']
df, gama_matched = cross_match_in_chunks(df, "II356xmmom41s.csv", 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000', gama_columns)
if len(gama_matched) > 0:
    gama_matched = clean_df(gama_matched)
    df = pd.concat([df, gama_matched[gama_columns]], axis=1)

# Flux calculations with safe_log
df['flux_Ha'] = df['F_Ha_cen']
df['e_flux_Ha'] = df['e_F_Ha_cen']
df['flux_Hb'] = df['flux_Hbeta4861.36_Re_fit']
df['flux_OIII_5007'] = df['flux_[OIII]5006.84_Re_fit']
df['flux_NII_6584'] = df['flux_[NII]6583.45_Re_fit']
flux_cols = ['flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584', 'e_flux_Ha']
for col in flux_cols:
    df[col] = df[col].fillna(df[col].median())

df['Ha_Hb_observed'] = df['flux_Ha'] / df['flux_Hb']
Ha_Hb_intrinsic = 2.86
k_Ha = 2.468
k_Hb = 3.634
df['A_Ha'] = 2.5 * safe_log(df['Ha_Hb_observed'] / Ha_Hb_intrinsic) * (k_Ha / (k_Hb - k_Ha))
df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * df['A_Ha'])
H0 = 70
c = 3e5
df['DL'] = (c * df['zsp'] / H0) * 3.0856e24
df['L_Ha'] = df['flux_Ha_corr'] * 4 * np.pi * df['DL']**2
df['log_SFR_Ha_raw'] = safe_log(df['L_Ha'] * 7.9e-42)
df['log_O3N2_raw'] = safe_log((df['flux_OIII_5007'] / df['flux_Hb']) / (df['flux_NII_6584'] / df['flux_Ha']))
df['OH_O3N2_raw'] = 8.533 - 0.214 * df['log_O3N2_raw']
df['log_flux_Ha'] = safe_log(df['flux_Ha'])
df['log_flux_Hb'] = safe_log(df['flux_Hb'])
df['log_flux_OIII_5007'] = safe_log(df['flux_OIII_5007'])
df['log_flux_NII_6584'] = safe_log(df['flux_NII_6584'])
df['log_e_flux_Ha'] = safe_log(df['e_flux_Ha'])

# Colors
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

# Final cleaning
df = df.dropna(subset=["log_SFR_Ha"])
df = df.dropna(axis=0, thresh=int(0.8 * df.shape[1]))
df = clean_df(df)

# Cosmo-Rank and L_cosmo(s)
gz_df = df.copy()
morph_cols = ['P(CD)', 'P(E)', 'P(S0)', 'P(Sa)', 'P(Sab)', 'P(Sb)', 'P(Sbc)', 'P(Sc)', 'P(Scd)', 'P(Sd)', 'P(Sdm)', 'P(Sm)', 'P(Irr)']
gz_df['morph_sum'] = gz_df[morph_cols].sum(axis=1)
gz_df['Num_w'] = gz_df['conf_prob']
scaler_rank = MinMaxScaler()
gz_df[['morph_sum_norm', 'Num_w_norm', 'nsa_z_norm']] = scaler_rank.fit_transform(gz_df[['morph_sum', 'Num_w', 'nsa_z']])
gz_df['cosmo_rank'] = (0.5 * gz_df['Num_w_norm'] + 0.3 * gz_df['morph_sum_norm'] + 0.2 * gz_df['nsa_z_norm'])
df['cosmo_rank'] = gz_df['cosmo_rank']

alpha = -1.5
M_star = df['log_Mass_gas'].median()
df['a_n'] = (10 ** df['log_Mass_gas'])**(1 + alpha) * np.exp(-10 ** df['log_Mass_gas'] / (10 ** M_star))
bins = pd.qcut(df['Re_kpc'], q=20, labels=False, duplicates='drop') + 1
df['z_bin'] = bins
s_vals = [0.5, 1.0, 1.5, 2.0]
for s in s_vals:
    df[f'L_cosmo_s_{s:.1f}'] = df.groupby('z_bin')['a_n'].transform('mean') / (df['z_bin'] ** s)
df['cosmo_rank_L'] = df['cosmo_rank'] * df['L_cosmo_s_1.0']
df['cosmo_rank_L'] = df['cosmo_rank_L'].replace([np.inf, -np.inf], np.nan).fillna(0)
df = clean_df(df)

# Feature engineering
target = "log_SFR_Ha"
base_features = [
    "log_Mass_gas", "log_Mass", "Av_gas_Re", "Av_ssp_Re", "OH_O3N2_cen", "OH_T04_cen", 
    "OH_dop_cen", "Age_LW_Re_fit", "ZH_LW_Re_fit", "Re_kpc", "vel_disp_Ha_cen", 
    "Lambda_Re", "Sigma_Mass_Re", "EW_Ha_cen", "Ha_Hb_cen"
]
df["mass_metallicity"] = df["log_Mass"] * df["OH_O3N2_cen"]
df["dust_metallicity"] = df["Av_gas_Re"] * df["OH_T04_cen"]
df["disp_mass_ratio"] = df["vel_disp_Ha_cen"] / (df["Sigma_Mass_Re"] + 1e-5)
df["age_metallicity"] = df["Age_LW_Re_fit"] * df["ZH_LW_Re_fit"]
df["sqrt_Re_kpc"] = np.sqrt(df['Re_kpc'] + 1e-5)
df["log_mass"] = safe_log(df["log_Mass_gas"])
df["BSD_likelihood"] = df["log_Mass_gas"] * df["OH_O3N2_cen"] / (df["Av_gas_Re"] + 1e-5 + df["Age_LW_Re_fit"])
df["cosmo_rank_mass"] = df["cosmo_rank"] * df["log_Mass"]
df["L_cosmo_s1_mass"] = df["L_cosmo_s_1.0"] * df["log_Mass"]
df["cosmo_rank_EW"] = df["cosmo_rank"] * df["EW_Ha_cen"]
df["L_cosmo_s1_EW"] = df["L_cosmo_s_1.0"] * df["EW_Ha_cen"]
df["cosmo_rank_scaled"] = df["cosmo_rank"] * 20
df["L_cosmo_s1_scaled"] = df["L_cosmo_s_1.0"] * 20
df["cosmo_rank_L_mass"] = df["cosmo_rank_L"] * df["log_Mass"]
df["L_cosmo_s1_metallicity"] = df["L_cosmo_s_1.0"] * df["OH_O3N2_cen"]
df = clean_df(df)

features = base_features + [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", "age_metallicity", "sqrt_Re_kpc", 
    "log_mass", "BSD_likelihood", "cosmo_rank", "L_cosmo_s_0.5", "L_cosmo_s_1.5", "L_cosmo_s_2.0", 
    "cosmo_rank_L", "cosmo_rank_mass", "L_cosmo_s1_mass", "cosmo_rank_EW", "L_cosmo_s1_EW", 
    "cosmo_rank_scaled", "L_cosmo_s1_scaled", "cosmo_rank_L_mass", "L_cosmo_s1_metallicity",
    "log_flux_Ha", "log_flux_Hb", "log_flux_OIII_5007", "log_flux_NII_6584", "log_e_flux_Ha", 
    "log_SFR_Ha_raw", "OH_O3N2_raw"
]
if 'color_ug' in df.columns:
    features.extend(["color_ug", "color_gr", "color_ri", "color_iz", "e_color_ug", "e_color_gr"])
if 'color_JK' in df.columns:
    features.extend(["color_JK", "e_color_JK"])

X = df[features]
y = df[target]

# Check NaNs before splitting
print("NaNs in X:", X.isna().sum().sum())
print("NaNs in y:", y.isna().sum())
X = clean_df(X)
y = y.fillna(y.median())

# Train/test split and scaling
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Check NaNs before optimization
print("NaNs in X_train_scaled:", np.isnan(X_train_scaled).sum())
print("NaNs in y_train:", y_train.isna().sum())
if np.isnan(X_train_scaled).any() or y_train.isna().any():
    X_train_scaled = np.nan_to_num(X_train_scaled, nan=np.nanmedian(X_train_scaled, axis=0))
    y_train = y_train.fillna(y_train.median())
    print("NaNs found and replaced with medians.")

# Optuna objectives
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
    if np.isnan(scores).any():
        print(f"HGB Trial {trial.number}: NaN in scores, returning -inf")
        return float('-inf')
    return scores.mean()

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
    if np.isnan(scores).any():
        print(f"LGB Trial {trial.number}: NaN in scores, returning -inf")
        return float('-inf')
    return scores.mean()

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
    if np.isnan(scores).any():
        print(f"XGB Trial {trial.number}: NaN in scores, returning -inf")
        return float('-inf')
    return scores.mean()

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
    if np.isnan(scores).any():
        print(f"CAT Trial {trial.number}: NaN in scores, returning -inf")
        return float('-inf')
    return scores.mean()

# Run Optuna optimizations
study_hgb = optuna.create_study(direction='maximize')
study_hgb.optimize(objective_hgb, n_trials=20)
best_params_hgb = study_hgb.best_params
print("Best HistGradientBoosting Parameters:", best_params_hgb)
print("Best HistGradientBoosting CV R²:", study_hgb.best_value)

study_lgb = optuna.create_study(direction='maximize')
study_lgb.optimize(objective_lgb, n_trials=20)
best_params_lgb = study_lgb.best_params
print("Best LightGBM Parameters:", best_params_lgb)
print("Best LightGBM CV R²:", study_lgb.best_value)

study_xgb = optuna.create_study(direction='maximize')
study_xgb.optimize(objective_xgb, n_trials=20)
best_params_xgb = study_xgb.best_params
print("Best XGBoost Parameters:", best_params_xgb)
print("Best XGBoost CV R²:", study_xgb.best_value)

study_cat = optuna.create_study(direction='maximize')
study_cat.optimize(objective_cat, n_trials=20)
best_params_cat = study_cat.best_params
print("Best CatBoost Parameters:", best_params_cat)
print("Best CatBoost CV R²:", study_cat.best_value)

# Train models
hgb = HistGradientBoostingRegressor(**best_params_hgb, random_state=42)
hgb.fit(X_train_scaled, y_train)
y_pred_hgb = hgb.predict(X_test_scaled)
r2_hgb = r2_score(y_test, y_pred_hgb)
cv_scores_hgb = cross_val_score(hgb, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"HistGradientBoosting 5-Fold CV R²: Mean = {cv_scores_hgb.mean():.4f}, Std = {cv_scores_hgb.std():.4f}")

lgb_model = lgb.LGBMRegressor(**best_params_lgb, random_state=42, verbose=-1)
lgb_model.fit(X_train_scaled, y_train)
y_pred_lgb = lgb_model.predict(X_test_scaled)
r2_lgb = r2_score(y_test, y_pred_lgb)
cv_scores_lgb = cross_val_score(lgb_model, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"LightGBM 5-Fold CV R²: Mean = {cv_scores_lgb.mean():.4f}, Std = {cv_scores_lgb.std():.4f}")

xgb_model = xgb.XGBRegressor(**best_params_xgb, random_state=42)
xgb_model.fit(X_train_scaled, y_train)
y_pred_xgb = xgb_model.predict(X_test_scaled)
r2_xgb = r2_score(y_test, y_pred_xgb)
cv_scores_xgb = cross_val_score(xgb_model, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"XGBoost 5-Fold CV R²: Mean = {cv_scores_xgb.mean():.4f}, Std = {cv_scores_xgb.std():.4f}")

cat_model = CatBoostRegressor(**best_params_cat, random_seed=42, verbose=0)
cat_model.fit(X_train_scaled, y_train)
y_pred_cat = cat_model.predict(X_test_scaled)
r2_cat = r2_score(y_test, y_pred_cat)
cv_scores_cat = cross_val_score(cat_model, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"CatBoost 5-Fold CV R²: Mean = {cv_scores_cat.mean():.4f}, Std = {cv_scores_cat.std():.4f}")

# SHAP analysis
explainer_hgb = shap.Explainer(hgb, X_train_scaled)
shap_values_hgb = explainer_hgb(X_test_scaled)
explainer_lgb = shap.Explainer(lgb_model, X_train_scaled)
shap_values_lgb = explainer_lgb(X_test_scaled)
explainer_xgb = shap.Explainer(xgb_model, X_train_scaled)
shap_values_xgb = explainer_xgb(X_test_scaled)
explainer_cat = shap.Explainer(cat_model, X_train_scaled)
shap_values_cat = explainer_cat(X_test_scaled)

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
plt.clf()

# SHAP feature importance
shap_values_hgb_mean = np.abs(shap_values_hgb.values).mean(axis=0)
shap_values_lgb_mean = np.abs(shap_values_lgb.values).mean(axis=0)
shap_values_xgb_mean = np.abs(shap_values_xgb.values).mean(axis=0)
shap_values_cat_mean = np.abs(shap_values_cat.values).mean(axis=0)
shap_values_combined = (shap_values_hgb_mean + shap_values_lgb_mean + shap_values_xgb_mean + shap_values_cat_mean) / 4

feature_importance = pd.DataFrame({"feature": features, "importance": shap_values_combined})
feature_importance = feature_importance.sort_values("importance", ascending=False)
top_features = feature_importance["feature"].head(10).tolist()

bsd_features = ["cosmo_rank", "L_cosmo_s_1.0", "cosmo_rank_L", "cosmo_rank_scaled", "L_cosmo_s1_scaled", "cosmo_rank_L_mass", "L_cosmo_s1_metallicity"]
for bsd_feature in bsd_features:
    if bsd_feature not in top_features:
        top_features.append(bsd_feature)

X_selected = df[top_features]
X_train_selected, X_test_selected, _, _ = train_test_split(X_selected, y, test_size=0.2, random_state=42)
X_train_selected_scaled = scaler.fit_transform(X_train_selected)
X_test_selected_scaled = scaler.transform(X_test_selected)

print("Top features selected based on combined SHAP values:", top_features)

# Symbolic Regression
symbolic_model = SymbolicRegressor(
    population_size=3000, generations=150, stopping_criteria=0.01, p_crossover=0.7,
    p_subtree_mutation=0.1, p_hoist_mutation=0.05, p_point_mutation=0.1, max_samples=0.9,
    verbose=1, parsimony_coefficient=0.0001, random_state=42,
    function_set=('add', 'sub', 'mul', 'div', 'sqrt', 'log', 'sin', 'cos')
)
symbolic_model.fit(X_train_selected_scaled, y_train)
y_pred_sym = symbolic_model.predict(X_test_selected_scaled)
r2_sym = r2_score(y_test, y_pred_sym)
print(f"gplearn R²: {r2_sym:.4f}")
print("Symbolic Expression:", symbolic_model._program)

cv_scores_sym = cross_val_score(symbolic_model, X_train_selected_scaled, y_train, cv=5, scoring='r2')
print(f"Symbolic Regression 5-Fold CV R²: Mean = {cv_scores_sym.mean():.4f}, Std = {cv_scores_sym.std():.4f}")

# Polynomial fit
x = np.linspace(min(y_test), max(y_test), 500)
y_expr = symbolic_model.predict(scaler.transform(np.tile(X_test_selected.mean().values, (500,1))))
p = Polynomial.fit(y_test, y_pred_sym, deg=3)
coeffs = p.coef
print("Polynomial Fit Equation (degree 3):")
print(f"y = {coeffs[0]:.4f} + {coeffs[1]:.4f}*x + {coeffs[2]:.4f}*x^2 + {coeffs[3]:.4f}*x^3")
plt.plot(*p.linspace(), label="Polynomial Fit")
plt.scatter(y_test, y_pred_sym, s=10, alpha=0.5, label="Symbolic Predictions")
plt.xlabel("True log_SFR_Ha")
plt.ylabel("Predicted log_SFR_Ha")
plt.title("Symbolic Regression Fit with Polynomial")
plt.legend()
plt.tight_layout()
plt.savefig("gplearn_expression_plot.png")
plt.clf()

# Predictions vs true
plt.scatter(y_test, y_pred_hgb, alpha=0.5, label="HistGradientBoosting", marker="o")
plt.scatter(y_test, y_pred_lgb, alpha=0.5, label="LightGBM", marker="o")
plt.scatter(y_test, y_pred_xgb, alpha=0.5, label="XGBoost", marker="s")
plt.scatter(y_test, y_pred_cat, alpha=0.5, label="CatBoost", marker="^")
plt.scatter(y_test, y_pred_sym, alpha=0.5, label="Symbolic", marker="x")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--")
plt.xlabel("True log_SFR_Ha")
plt.ylabel("Predicted")
plt.title("Model Predictions vs True Values")
plt.legend()
plt.tight_layout()
plt.savefig("model_comparison.png")
plt.clf()

# Residuals
residuals = pd.DataFrame({
    "True": y_test,
    "HistGradientBoosting": y_pred_hgb - y_test,
    "LightGBM": y_pred_lgb - y_test,
    "XGBoost": y_pred_xgb - y_test,
    "CatBoost": y_pred_cat - y_test,
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
print(residuals[["HistGradientBoosting", "LightGBM", "Symbolic", "cosmo_rank", "L_cosmo_s1"]].corr()[["HistGradientBoosting", "LightGBM", "Symbolic"]])