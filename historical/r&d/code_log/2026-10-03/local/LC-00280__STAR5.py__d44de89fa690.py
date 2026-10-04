import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingRegressor
import optuna
from scipy.spatial import cKDTree

# Load data
df = pd.read_csv("merged_data.csv")
df['objra_y'] = pd.to_numeric(df['objra_y'], errors='coerce')
df['objdec'] = pd.to_numeric(df['objdec'], errors='coerce')
print(f"Initial rows in df: {len(df)}")  # Expect 100,000
print(f"NaN in objra_y: {df['objra_y'].isna().sum()}, NaN in objdec: {df['objdec'].isna().sum()}")

# SDSS merging
sdss_dr16 = pd.read_csv("V154sdss16.csv")
sdss_dr12 = pd.read_csv("V147sdss12.csv")
sdss_merged = pd.merge(
    sdss_dr16[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']],
    sdss_dr12[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']],
    on='objID', how='outer', suffixes=('_dr16', '_dr12')
)
sdss_merged['RA_ICRS'] = sdss_merged['RA_ICRS_dr16'].combine_first(sdss_merged['RA_ICRS_dr12'])
# ... (combine other columns as in your code)
sdss_merged = sdss_merged[['objID', 'RA_ICRS', 'DE_ICRS', 'zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']]
print(f"Merged SDSS rows: {len(sdss_merged)}")

# Cross-match function (unchanged)
def clean_coordinates(df, ra_col, dec_col):
    initial_len = len(df)
    mask = df[ra_col].notna() & df[dec_col].notna() & np.isfinite(df[ra_col]) & np.isfinite(df[dec_col])
    df_cleaned = df[mask].copy()
    print(f"Removed {initial_len - len(df_cleaned)} rows due to NaN/inf in {ra_col}/{dec_col}")
    return df_cleaned

def deg_to_rad(df, ra_col, dec_col):
    df['ra_rad'] = np.radians(df[ra_col])
    df['dec_rad'] = np.radians(df[dec_col])
    return df

def cross_match(df1, df2, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec=30.0):
    df1_cleaned = clean_coordinates(df1, ra_col1, dec_col1)
    df2_cleaned = clean_coordinates(df2, ra_col2, dec_col2)
    if len(df1_cleaned) == 0 or len(df2_cleaned) == 0:
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
    print(f"Matches found: {len(df2_matched)}")
    return df1_matched, df2_matched

def cross_match_in_chunks(df1, filepath, ra_col1, dec_col1, ra_col2, dec_col2, columns_to_keep, max_dist_arcsec=30.0, chunksize=100000):
    df1[ra_col1] = pd.to_numeric(df1[ra_col1], errors='coerce')
    df1[dec_col1] = pd.to_numeric(df1[dec_col1], errors='coerce')
    min_ra, max_ra = df1[ra_col1].min() - 0.1, df1[ra_col1].max() + 0.1
    min_dec, max_dec = df1[dec_col1].min() - 0.1, df1[dec_col1].max() + 0.1
    matched_df2_list = []
    usecols = [ra_col2, dec_col2] + columns_to_keep
    chunk_reader = pd.read_csv(filepath, chunksize=chunksize, usecols=usecols, on_bad_lines='warn')
    for i, chunk in enumerate(chunk_reader):
        chunk[ra_col2] = pd.to_numeric(chunk[ra_col2], errors='coerce')
        chunk[dec_col2] = pd.to_numeric(chunk[dec_col2], errors='coerce')
        chunk = chunk.dropna(subset=[ra_col2, dec_col2])
        chunk_filtered = chunk[
            (chunk[ra_col2] >= min_ra) & (chunk[ra_col2] <= max_ra) &
            (chunk[dec_col2] >= min_dec) & (chunk[dec_col2] <= max_dec)
        ]
        if len(chunk_filtered) == 0:
            continue
        _, matched_df2 = cross_match(df1, chunk_filtered, ra_col1, dec_col1, ra_col2, dec_col2, max_dist_arcsec)
        if len(matched_df2) > 0:
            matched_df2_list.append(matched_df2[columns_to_keep])
    matched_df2 = pd.concat(matched_df2_list, ignore_index=True) if matched_df2_list else pd.DataFrame()
    print(f"Total matches from chunks: {len(matched_df2)}")
    return df1, matched_df2

# Cross-matching with preservation
df_original = df.copy()
df_matched, sdss_matched = cross_match(df, sdss_merged, 'objra_y', 'objdec', 'RA_ICRS', 'DE_ICRS', max_dist_arcsec=30.0)
sdss_columns = ['zsp', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'e_umag', 'e_gmag', 'e_rmag', 'e_imag', 'e_zmag']
if len(sdss_matched) < 10000:  # 10% threshold
    print("Few SDSS matches. Retaining original df.")
    df = df_original.copy()
    df['zsp'] = df['nsa_z']
else:
    sdss_matched[sdss_columns] = sdss_matched[sdss_columns].fillna(sdss_matched[sdss_columns].median())
    df = df_original.merge(sdss_matched[sdss_columns], left_index=True, right_index=True, how='left')
print(f"Rows after SDSS processing: {len(df)}")

twomass_columns = ['Jmag', 'Hmag', 'Kmag', 'e_Jmag', 'e_Hmag', 'e_Kmag']
df, twomass_matched = cross_match_in_chunks(
    df, "2Mass.csv", 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000',
    twomass_columns, max_dist_arcsec=30.0, chunksize=100000
)
if len(twomass_matched) > 0:
    twomass_matched[twomass_columns] = twomass_matched[twomass_columns].fillna(twomass_matched[twomass_columns].median())
    df = df.merge(twomass_matched[twomass_columns], left_index=True, right_index=True, how='left')
print(f"Rows after 2MASS processing: {len(df)}")

gama_columns = ['UmAB', 'BmAB', 'VmAB']
df, gama_matched = cross_match_in_chunks(
    df, "II356xmmom41s.csv", 'objra_y', 'objdec', 'RAJ2000', 'DEJ2000',
    gama_columns, max_dist_arcsec=30.0, chunksize=100000
)
if len(gama_matched) > 0:
    gama_matched[gama_columns] = gama_matched[gama_columns].fillna(gama_matched[gama_columns].median())
    df = df.merge(gama_matched[gama_columns], left_index=True, right_index=True, how='left')
print(f"Rows after GAMA processing: {len(df)}")

# Flux calculations
flux_cols = ['flux_Ha', 'e_flux_Ha', 'flux_Hb', 'flux_OIII_5007', 'flux_NII_6584']
df[flux_cols] = df[['F_Ha_cen', 'e_F_Ha_cen', 'flux_Hbeta4861.36_Re_fit', 'flux_[OIII]5006.84_Re_fit', 'flux_[NII]6583.45_Re_fit']]
for col in flux_cols:
    nan_count = df[col].isna().sum()
    print(f"NaN in {col}: {nan_count}")
    df[col] = df[col].fillna(df[col].median())
df['Ha_Hb_observed'] = df['flux_Ha'] / df['flux_Hb']
df['A_Ha'] = 2.5 * np.log10(df['Ha_Hb_observed'] / 2.86) * (2.468 / (3.634 - 2.468))
df['flux_Ha_corr'] = df['flux_Ha'] * 10**(0.4 * df['A_Ha'])
df['DL'] = (3e5 * df['zsp'].fillna(df['nsa_z']) / 70) * 3.0856e24
df['L_Ha'] = df['flux_Ha_corr'] * 4 * np.pi * df['DL']**2
df['log_SFR_Ha_raw'] = np.log10(df['L_Ha'] * 7.9e-42)
print(f"NaN in log_SFR_Ha_raw after calc: {df['log_SFR_Ha_raw'].isna().sum()}")

# Pre-cleaning
df = df.dropna(subset=["log_SFR_Ha_raw"])
df = df.dropna(axis=0, thresh=int(0.5 * df.shape[1]))
df.fillna(df.median(numeric_only=True), inplace=True)
print(f"Rows after pre-cleaning: {len(df)}")

# Feature engineering
target = "log_SFR_Ha_raw"
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
df["sqrt_Re_kpc"] = np.sqrt(df['Re_kpc'] + 1e-5)
df["log_mass"] = np.log(df["log_Mass_gas"] + 1e-5)
df["BSD_likelihood"] = (
    df["log_Mass_gas"] * df["OH_O3N2_cen"] /
    (df["Av_gas_Re"] + 1e-5 + df["Age_LW_Re_fit"])
)
# Add cosmo features (simplified for brevity; include your full list)
df["cosmo_rank_mass"] = df.get("cosmo_rank", 0) * df["log_Mass"]
features = base_features + [
    "mass_metallicity", "dust_metallicity", "disp_mass_ratio", 
    "age_metallicity", "sqrt_Re_kpc", "log_mass", "BSD_likelihood", 
    "cosmo_rank_mass", "log_flux_Ha", "log_flux_Hb", "log_flux_OIII_5007", 
    "log_flux_NII_6584", "log_e_flux_Ha", "log_SFR_Ha_raw"
]
if 'umag' in df.columns:
    df['color_ug'] = df['umag'] - df['gmag']
    features.extend(["color_ug"])
if 'Jmag' in df.columns:
    df['color_JK'] = df['Jmag'] - df['Kmag']
    features.extend(["color_JK"])

X = df[features]
y = df[target]
print(f"Rows after feature selection: {len(X)}")
print(f"NaN in y ({target}): {y.isna().sum()}")

# Cleaning
numeric_features = [col for col in features if pd.api.types.is_numeric_dtype(X[col])]
X = X[numeric_features]
print(f"Numeric features selected: {len(numeric_features)}")
print(X.head())
X = X.replace([np.inf, -np.inf], np.nan)
print(f"Columns with NaN before imputation: {X.columns[X.isna().any()].tolist()}")
X = X.fillna(X.median())
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
if len(X) < 100:
    raise ValueError(f"Only {len(X)} rows after cleaning. Check data preprocessing.")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize
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
hgb = HistGradientBoostingRegressor(**best_params_hgb, random_state=42)
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