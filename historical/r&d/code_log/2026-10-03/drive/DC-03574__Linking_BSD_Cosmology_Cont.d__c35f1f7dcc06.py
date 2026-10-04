joblib.dump(gb_model, 'best_gb_model.pkl')
      * print("Best Gradient Boosting model saved to 'best_gb_model.pkl'")
      * Further Tuning: Tune Gradient Boosting’s hyperparameters (e.g., learning_rate, max_depth) to potentially lower the MSE further:
      * python
param_grid_gb = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7]
}
grid_search_gb = GridSearchCV(estimator=GradientBoostingRegressor(random_state=42),
                              param_grid=param_grid_gb, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_gb.fit(X_train, y_train)
      * print(f"Best Gradient Boosting hyperparameters: {grid_search_gb.best_params_}")
      2. Leverage Feature Importances
      * Observation: log_Mass_gas dominates with 75.25% importance, while other features contribute much less.
      * Action:
      * Focus on Gas Mass: Since log_Mass_gas is critical, ensure its data quality is high (e.g., check for measurement errors or missing values).
      * Add Related Features: Explore adding features related to gas properties (e.g., gas metallicity, gas density) if available, as they might complement log_Mass_gas and reduce reliance on a single predictor.
      * Feature Engineering: Create interaction terms involving log_Mass_gas (e.g., log_Mass_gas * log_Mass) to capture combined effects.
      3. Inspect Residual Plots
      * Action: Open the saved residual plots (residuals_histogram_rf.png, residuals_vs_predicted_rf.png) to check for patterns:
      * If residuals are randomly scattered around zero, the model fits well.
      * If you see patterns (e.g., a curve, funnel shape, or clustering), consider:
      * Adding nonlinear features (e.g., squared terms like log_Mass_gas^2).
      * Using a more complex model (e.g., a tuned Gradient Boosting or a neural network).
      * Optional: If you can’t view the plots due to the non-interactive environment, transfer the PNG files to a local machine for inspection.
      4. Improve XGBoost Performance
      * Observation: XGBoost underperformed (MSE: 0.2919, R²: 0.8103) compared to Random Forest and Gradient Boosting.
      * Action: Tune XGBoost’s hyperparameters to improve its performance:
      * python
param_grid_xgb = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7]
}
grid_search_xgb = GridSearchCV(estimator=xgb.XGBRegressor(random_state=42),
                               param_grid=param_grid_xgb, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_xgb.fit(X_train, y_train)
best_xgb_model = grid_search_xgb.best_estimator_
y_pred_xgb_tuned = best_xgb_model.predict(X_test)
mse_xgb_tuned = mean_squared_error(y_test, y_pred_xgb_tuned)
r2_xgb_tuned = r2_score(y_test, y_pred_xgb_tuned)
print(f"Tuned XGBoost MSE: {mse_xgb_tuned:.4f}")
      * print(f"Tuned XGBoost R-squared: {r2_xgb_tuned:.4f}")
      5. Address Plotting Warnings
