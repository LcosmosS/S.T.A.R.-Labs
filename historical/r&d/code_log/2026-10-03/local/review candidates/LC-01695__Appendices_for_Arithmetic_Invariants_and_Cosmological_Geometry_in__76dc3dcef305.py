    print("gudhi not installed. Run: pip install gudhi")
    gudhi = None

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')

# --- 3. Function Tracking ---
def log_function(func_name):
    print(f"Running {func_name}...")

# --- 4. Pre-Calculation NaN Handling ---
def impute_input_features(chunk, impute_cols=['ra', 'dec', 'z', 'metallicity'],
target_cols=['logmass', 'petrorad_r']):
    log_function("impute_input_features")
    chunk = chunk.copy()
    imputer = KNNImputer(n_neighbors=5, weights='distance')
    X = chunk[impute_cols + target_cols]
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=impute_cols +
target_cols, index=chunk.index)
    for target in target_cols:
        nan_idx = chunk[target].isna()
        if nan_idx.any():
            chunk.loc[nan_idx, target] = X_imputed.loc[nan_idx, target]
            print(f"impute_input_features: Imputed {target} for {nan_idx.sum()} rows")
    return chunk

# --- 5. Post-Calculation NaN Handling ---
def impute_derived_features(df, feature_cols):
    log_function("impute_derived_features")
    df = df.copy()
    imputer = KNNImputer(n_neighbors=5, weights='distance')
    X = df[feature_cols]
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=feature_cols,
index=df.index)
    for col in feature_cols:
        nan_idx = df[col].isna()