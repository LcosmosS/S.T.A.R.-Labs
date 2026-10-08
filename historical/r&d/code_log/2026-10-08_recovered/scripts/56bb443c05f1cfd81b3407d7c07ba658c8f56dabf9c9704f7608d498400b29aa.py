from sklearn.model_selection import GridSearchCV

# Define parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

# Perform grid search within cross-validation
model = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X, y)  # Fit on the full dataset initially
best_model = grid_search.best_estimator_
print(f"Best parameters: {grid_search.best_params_}")

# Use best_model for cross-validation
for fold, (train_idx, test_idx) in enumerate(kf.split(X)):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mse_list.append(mse)
    print(f"Fold {fold+1} MSE: {mse:.4f}")

import joblib

# After training the final model
joblib.dump(model, 'bsd_model.pkl')

# Load and test on new data
new_df = pd.read_csv('new_dataset.csv')
for col in required_columns + optional_columns:
    if col in new_df.columns:
        new_df[col] = new_df[col].fillna(new_df[col].mean())
    else:
        new_df[col] = 0
if 'ra' in new_df.columns and 'dec' in new_df.columns:
    new_df['environment'] = new_df.groupby(['ra', 'dec'])['ra'].transform('size')
else:
    new_df['environment'] = 0

X_new = np.array([predict_sfr_features(row, l_1, order) for _, row in new_df.iterrows()])
y_new = new_df['sfr'].values
loaded_model = joblib.load('bsd_model.pkl')
y_new_pred = loaded_model.predict(X_new)
new_mse = mean_squared_error(y_new, y_new_pred)
print(f"MSE on new dataset: {new_mse:.4f}")