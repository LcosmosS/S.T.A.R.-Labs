import pandas as pd import numpy as np import matplotlib.pyplot as plt from sklearn.model_selection import KFold, cross_val_score, GridSearchCV, train_test_split from sklearn.ensemble import RandomForestRegressor from sklearn.metrics import mean_squared_error, r2_score import joblib
# Step 1: Load the dataset
df = pd.read_csv('Filtered_Pipe3D.csv') # Replace with your dataset file print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")
# Step 2: Define features (X) and target (y)
X = df.drop(columns=['log_SFR_Ha']) # Replace 'log_SFR_Ha' with your target column y = df['log_SFR_Ha']
# Step 3: Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")
# Step 4: Set up 5-fold cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
# Step 5: Initialize the model (Random Forest Regressor)
model = RandomForestRegressor(random_state=42)
# Step 6: Perform cross-validation and calculate MSE for each fold
mse_scores = cross_val_score(model, X_train, y_train, cv=kf, scoring='neg_mean_squared_error') mse_scores = -mse_scores # Convert to positive MSE print(f"MSE for each fold: {mse_scores}") print(f"Average MSE from cross-validation: {np.mean(mse_scores):.4f}")
# Step 7: Define a grid of hyperparameters for tuning
param_grid = { 'n_estimators': [100, 200, 300], 'max_depth': [10, 20, None], 'min_samples_split': [2, 5, 10] }
# Step 8: Perform hyperparameter tuning with GridSearchCV
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=42), param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1) grid_search.fit(X_train, y_train)
# Get the best hyperparameters and model
best_params = grid_search.best_params_ best_model = grid_search.best_estimator_ print(f"Best hyperparameters: {best_params}")
# Step 9: Train the best model on the full training set
best_model.fit(X_train, y_train)
# Step 10: Make predictions on the test set
y_pred = best_model.predict(X_test)
# Step 11: Evaluate the tuned model on the test set
mse = mean_squared_error(y_test, y_pred) r2 = r2_score(y_test, y_pred) print(f"Tuned Mean Squared Error (MSE): {mse:.4f}") print(f"Tuned R-squared: {r2:.4f}")
# Step 12: Save the best model
joblib.dump(best_model, 'best_rf_model.pkl') print("Best model saved to 'best_rf_model.pkl'")
# Step 13: Plot predicted vs. actual values
plt.figure(figsize=(8, 6)) plt.scatter(y_test, y_pred, alpha=0.5) plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--') # 45-degree line plt.xlabel('Actual SFR') plt.ylabel('Predicted SFR') plt.title('Predicted vs. Actual Star Formation Rates') plt.savefig('predicted_vs_actual.png') plt.show()
# Step 14: Plot a histogram of residuals
residuals = y_test - y_pred plt.figure(figsize=(8, 6)) plt.hist(residuals, bins=30, edgecolor='black') plt.xlabel('Residuals (Actual - Predicted)') plt.ylabel('Frequency') plt.title('Histogram of Residuals') plt.savefig('residuals_histogram.png') plt.show()
