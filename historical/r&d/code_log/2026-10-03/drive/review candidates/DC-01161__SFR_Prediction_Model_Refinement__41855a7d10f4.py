X = df[features]
y = df[target]


# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Model
model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=4, random_state=42)
model.fit(X_train, y_train)


# Predictions and metrics
y_pred = model.predict(X_test)


print("\n--- Model Evaluation ---")
print(f"R² Score: {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred):.4f}")


# SHAP
explainer = shap.Explainer(model.predict, X_train)
shap_values = explainer(X_test)


shap.summary_plot(shap_values, X_test, show=False)
plt.tight_layout()
plt.savefig("shap_summary_plot.png")
print("\nSHAP summary plot saved as 'shap_summary_plot.png'")
