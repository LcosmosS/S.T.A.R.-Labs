numeric_features = [col for col in features if pd.api.types.is_numeric_dtype(X[col])]
X = X[numeric_features]
print(f"Numeric features selected: {numeric_features}")
print("Sample values:")
print(X.head())

# Clean X and y with global median imputation
========================================================================
====================================================================
X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median(skipna=True))
y = y.replace([np.inf, -np.inf], np.nan).fillna(y.median(skipna=True))
print(f"Rows after X and y imputation: {len(X)}")

# Train/test split
========================================================================
========================================================================
=======================
if len(X) < 10:
    raise ValueError(f"Only {len(X)} rows after cleaning. Check data preprocessing.")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Verify inputs
========================================================================
========================================================================
==========================
print("NaN in X_train_scaled:", np.isnan(X_train_scaled).sum())
print("Inf in X_train_scaled:", np.isinf(X_train_scaled).sum())
print("NaN in y_train:", y_train.isna().sum())
print("Inf in y_train:", np.isinf(y_train).sum())
print("Feature selection and scaling complete. Initiating *S.T.A.R. training with Optuna...")

# Optuna Optimizations
========================================================================
========================================================================
===================
def objective_hgb(trial):
    params = {