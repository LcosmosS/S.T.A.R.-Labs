#===== Plot histogram for each feature ==================================================================================================================================================
        plt.figure(figsize=(8, 6))
        plt.hist(df[col].dropna(), bins=50, range=(df[col].quantile(0.01), df[col].quantile(0.99)), 
                 density=True, alpha=0.7)
        plt.xlabel(col)
        plt.ylabel("Density")
        plt.title(f"Distribution of {col}")
        plt.savefig(f"dist_{col}.png", dpi=150)
        plt.close()
    else:
        print(f"{col}: Missing from dataset")


# Define s_range and plot L_cosmo_s vs log_SFR_Ha_raw ====================================================================================================================================
s_vals = [0.5, 1.0, 1.5, 2.0]
for s in s_vals:
    col_name = f'L_cosmo_s_{s:.1f}'
    if col_name in df.columns:
        mask = df[col_name].notna() & df['log_SFR_Ha_raw'].notna() & np.isfinite(df[col_name]) & np.isfinite(df['log_SFR_Ha_raw'])
        if mask.sum() < 10:
            print(f"Warning: Insufficient valid data for {col_name} plotting/fitting ({mask.sum()} valid rows).")
            continue


# ===== Scatter plot =====================================================================================================================================================================
        plt.figure(figsize=(8, 6))
        plt.scatter(df.loc[mask, col_name], df.loc[mask, 'log_SFR_Ha_raw'], alpha=0.5, s=10)
        plt.xlabel(f"{col_name}")
        plt.ylabel("log_SFR_Ha_raw")
        plt.title(f"{col_name} vs log_SFR_Ha_raw")
        plt.savefig(f"L_cosmo_s{s:.1f}_vs_SFR.png", dpi=150)
        plt.close()


# ==== Polynomial fit plot ===============================================================================================================================================================
        try:
            poly_coeffs = Polynomial.fit(df.loc[mask, col_name], df.loc[mask, 'log_SFR_Ha_raw'], deg=2)
            x_fit = np.linspace(df.loc[mask, col_name].min(), df.loc[mask, col_name].max(), 100)
            y_fit = poly_coeffs(x_fit)
            y_pred = poly_coeffs(df.loc[mask, col_name])
            r2 = r2_score(df.loc[mask, 'log_SFR_Ha_raw'], y_pred)
            plt.figure(figsize=(8, 6))
            plt.scatter(df.loc[mask, col_name], df.loc[mask, 'log_SFR_Ha_raw'], alpha=0.5, s=10)
            plt.plot(x_fit, y_fit, 'r-', label=f'Quadratic Fit (R²={r2:.3f})')
            plt.xlabel(f"{col_name}")
            plt.ylabel("log_SFR_Ha_raw")
            plt.title(f"{col_name} vs log_SFR_Ha_raw with Polynomial Fit")
            plt.legend()
            plt.savefig(f"L_cosmo_s{s:.1f}_vs_SFR_fit.png", dpi=150)
            plt.close()
        except Exception as e:
            print(f"Warning: Polynomial fit failed for {col_name}: {e}")
    else:
        print(f"Warning: {col_name} not available for plotting.")


# Define features and target =============================================================================================================================================================
target = "log_SFR_Ha_raw"
features = [
    "logMass", "Re_kpc", "OH_O3N2_raw", "cosmo_rank",
    "mass_metallicity", "sqrt_Re_kpc", "cosmo_rank_mass", "L_cosmo_s1_mass",
    "log_flux_Ha", "log_flux_Hb", "log_flux_OIII_5007", "log_flux_NII_6584", 
    "log_e_flux_Ha", "L_cosmo_s_0.5", "L_cosmo_s_1.0", "L_cosmo_s_1.5", 
    "L_cosmo_s_2.0", "cluster_density"
]
if 'umag' in df.columns:
    features.extend(["color_ug", "color_gr", "color_ri", "color_iz", "e_color_ug", "e_color_gr"])
if 'Jmag' in df.columns:
    features.extend(["color_JK", "e_color_JK"])
if 'color_ug' in df.columns:
    features.extend(["color_ug", "color_gr", "color_ri", "color_iz", "e_color_ug", "e_color_gr"])
if 'color_JK' in df.columns:
    features.extend(["color_JK", "e_color_JK"])


# Global imputation before feature selection =============================================================================================================================================
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].replace([np.inf, -np.inf], np.nan).fillna(df[numeric_cols].median(skipna=True))


# Select features and target =============================================================================================================================================================
X = df[features]
y = df[target]
print(f"Rows after feature selection: {len(X)}")
print(f"NaN in y ({target}): {y.isna().sum()}")
missing_features = [f for f in features if f not in df.columns]
if missing_features:
    print(f"Warning: The following features are missing from the dataset: {missing_features}")
else:
    print("All features present in the dataset.")


# Correlation heatmap of numeric features ================================================================================================================================================
plt.figure(figsize=(12, 10))
sns.heatmap(X.corr(), annot=False, cmap='coolwarm', vmin=-1, vmax=1)
plt.title("Correlation Heatmap of Features")
plt.savefig("feature_correlation_heatmap.png")
plt.close()


# Filter to numeric columns only =========================================================================================================================================================
numeric_features = [col for col in features if pd.api.types.is_numeric_dtype(X[col])]
X = X[numeric_features]
print(f"Numeric features selected: {numeric_features}")
print("Sample values:")
print(X.head())


# Clean X and y with global median imputation ============================================================================================================================================
X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median(skipna=True))
y = y.replace([np.inf, -np.inf], np.nan).fillna(y.median(skipna=True))
print(f"Rows after X and y imputation: {len(X)}")


# Train/test split =======================================================================================================================================================================
if len(X) < 10:
    raise ValueError(f"Only {len(X)} rows after cleaning. Check data preprocessing.")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Verify inputs ==========================================================================================================================================================================
print("NaN in X_train_scaled:", np.isnan(X_train_scaled).sum())
print("Inf in X_train_scaled:", np.isinf(X_train_scaled).sum())
print("NaN in y_train:", y_train.isna().sum())
print("Inf in y_train:", np.isinf(y_train).sum())
print("Feature selection and scaling complete. Initiating *S.T.A.R. training with Optuna...")


# Optuna Optimizations ===================================================================================================================================================================
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
    mean_score = np.nanmean(scores)
    if np.isnan(mean_score):
        print(f"HGB Trial {trial.number} failed: scores = {scores}")
    return mean_score if not np.isnan(mean_score) else -np.inf


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


# Define models and studies ==============================================================================================================================================================
hgb = HistGradientBoostingRegressor(random_state=42, n_jobs=2)
symbolic_reg = SymbolicRegressor(population_size=1000, generations=20, random_state=42, n_jobs=2)
lgb_model = lgb.LGBMRegressor(random_state=42, verbose=-1)
xgb_model = xgb.XGBRegressor(random_state=42)
cat_model = CatBoostRegressor(random_seed=42, verbose=0)


study_hgb = optuna.create_study(direction='maximize')
study_lgb = optuna.create_study(direction='maximize')
study_xgb = optuna.create_study(direction='maximize')
study_cat = optuna.create_study(direction='maximize')


print("Initiating *S.T.A.R. calculations...")
for model_name in tqdm(['HistGradientBoosting', 'Symbolic', 'LightGBM', 'XGBoost', 'CatBoost'], desc="Training Models"):
    print(f"Training {model_name}...")
    if model_name == 'HistGradientBoosting':
        study_hgb.optimize(objective_hgb, n_trials=20)
        print(f"Best HistGradientBoosting Parameters: {study_hgb.best_params}")
        print(f"Best HistGradientBoosting CV R²: {study_hgb.best_value:.4f}")
        hgb.set_params(**study_hgb.best_params)
        hgb.fit(X_train_scaled, y_train)
        y_pred_hgb = hgb.predict(X_test_scaled)
        r2_hgb = r2_score(y_test, y_pred_hgb)
        cv_scores_hgb = cross_val_score(hgb, X_train_scaled, y_train, cv=5, scoring='r2')
        print(f"HistGradientBoosting 5-Fold CV R²: Mean = {cv_scores_hgb.mean():.4f}, Std = {cv_scores_hgb.std():.4f}")
        print(f"R^2 Score (HistGradientBoosting, Test): {r2_hgb:.4f}")
    elif model_name == 'Symbolic':
        symbolic_reg.fit(X_train_scaled, y_train)
        y_pred_symbolic = symbolic_reg.predict(X_test_scaled)
        r2_symbolic = r2_score(y_test, y_pred_symbolic)
        print(f"R^2 Score (Symbolic Regression, Test): {r2_symbolic:.4f}")
        print(f"Symbolic Expression: {symbolic_reg._program}")
    elif model_name == 'LightGBM':
        study_lgb.optimize(objective_lgb, n_trials=20)
        print(f"Best LightGBM Parameters: {study_lgb.best_params}")
        print(f"Best LightGBM CV R²: {study_lgb.best_value:.4f}")
        lgb_model.set_params(**study_lgb.best_params)
        lgb_model.fit(X_train_scaled, y_train)
        y_pred_lgb = lgb_model.predict(X_test_scaled)
        r2_lgb = r2_score(y_test, y_pred_lgb)
        cv_scores_lgb = cross_val_score(lgb_model, X_train_scaled, y_train, cv=5, scoring='r2')
        print(f"LightGBM 5-Fold CV R²: Mean = {cv_scores_lgb.mean():.4f}, Std = {cv_scores_lgb.std():.4f}")
        print(f"R^2 Score (LightGBM, Test): {r2_lgb:.4f}")
    elif model_name == 'XGBoost':
        study_xgb.optimize(objective_xgb, n_trials=20)
        print(f"Best XGBoost Parameters: {study_xgb.best_params}")
        print(f"Best XGBoost CV R²: {study_xgb.best_value:.4f}")
        xgb_model.set_params(**study_xgb.best_params)
        xgb_model.fit(X_train_scaled, y_train)
        y_pred_xgb = xgb_model.predict(X_test_scaled)
        r2_xgb = r2_score(y_test, y_pred_xgb)
        cv_scores_xgb = cross_val_score(xgb_model, X_train_scaled, y_train, cv=5, scoring='r2')
        print(f"XGBoost 5-Fold CV R²: Mean = {cv_scores_xgb.mean():.4f}, Std = {cv_scores_xgb.std():.4f}")
        print(f"R^2 Score (XGBoost, Test): {r2_xgb:.4f}")
    elif model_name == 'CatBoost':
        study_cat.optimize(objective_cat, n_trials=20)
        print(f"Best CatBoost Parameters: {study_cat.best_params}")
        print(f"Best CatBoost CV R²: {study_cat.best_value:.4f}")
        cat_model.set_params(**study_cat.best_params)
        cat_model.fit(X_train_scaled, y_train)
        y_pred_cat = cat_model.predict(X_test_scaled)
        r2_cat = r2_score(y_test, y_pred_cat)
        cv_scores_cat = cross_val_score(cat_model, X_train_scaled, y_train, cv=5, scoring='r2')
        print(f"CatBoost 5-Fold CV R²: Mean = {cv_scores_cat.mean():.4f}, Std = {cv_scores_cat.std():.4f}")
        print(f"R^2 Score (CatBoost, Test): {r2_cat:.4f}")


# Blend symbolic regression with HistGradientBoosting ====================================================================================================================================
y_pred_blend = (y_pred_hgb + y_pred_symbolic) / 2
r2_blend = r2_score(y_test, y_pred_blend)
print(f"R^2 Score (Blended HGB + Symbolic, Test): {r2_blend:.4f}")
y_pred_all = (hgb.predict(X_train_scaled) + symbolic_reg.predict(X_train_scaled)) / 2
percentiles = np.percentile(y_pred_all - y_train, [5, 95])
print(f"Blended Model 90% Prediction Interval: [{percentiles[0]:.4f}, {percentiles[1]:.4f}]")


# Plot blended predictions vs actual =====================================================================================================================================================
plt.scatter(y_test, y_pred_blend, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel("Actual log_SFR_Ha_raw")
plt.ylabel("Predicted log_SFR_Ha_raw (Blended HGB + Symbolic)")
plt.title("Blended Model: Actual vs Predicted")
plt.savefig("blended_actual_vs_pred.png", dpi=150)
plt.close()


# SHAP Analysis ==========================================================================================================================================================================
sample_idx = np.random.choice(X_test_scaled.shape[0], min(1000, X_test_scaled.shape[0]), replace=False)
X_test_scaled_sample = X_test_scaled[sample_idx]


explainer_hgb = shap.Explainer(hgb, X_train_scaled)
shap_values_hgb = explainer_hgb(X_test_scaled_sample)
shap.summary_plot(shap_values_hgb, X_test.iloc[sample_idx], feature_names=X.columns, plot_type="bar")
plt.title("SHAP Summary - HistGradientBoosting")
plt.tight_layout()
plt.savefig("shap_hgb_summary.png", dpi=150)
plt.close()


explainer_lgb = shap.Explainer(lgb_model, X_train_scaled)
shap_values_lgb = explainer_lgb(X_test_scaled_sample)
shap.summary_plot(shap_values_lgb, X_test.iloc[sample_idx], feature_names=X.columns, plot_type="bar")
plt.title("SHAP Summary - LightGBM")
plt.tight_layout()
plt.savefig("shap_lgb_summary.png", dpi=150)
plt.close()


explainer_xgb = shap.Explainer(xgb_model, X_train_scaled)
shap_values_xgb = explainer_xgb(X_test_scaled_sample)
shap.summary_plot(shap_values_xgb, X_test.iloc[sample_idx], feature_names=X.columns, plot_type="bar")
plt.title("SHAP Summary - XGBoost")
plt.tight_layout()
plt.savefig("shap_xgb_summary.png", dpi=150)
plt.close()


explainer_cat = shap.Explainer(cat_model, X_train_scaled)
shap_values_cat = explainer_cat(X_test_scaled_sample)
shap.summary_plot(shap_values_cat, X_test.iloc[sample_idx], feature_names=X.columns, plot_type="bar")
plt.title("SHAP Summary - CatBoost")
plt.tight_layout()
plt.savefig("shap_cat_summary.png", dpi=150)
plt.close()
print("*S.T.A.R. training and analysis complete. All outputs saved.")