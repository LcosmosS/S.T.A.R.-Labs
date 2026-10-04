X = df[features]
y = df[target]


# --- Split Dataset ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# --- Gradient Boosting Model ---
gbr = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=4, random_state=42)
gbr.fit(X_train, y_train)
y_pred_gbr = gbr.predict(X_test)


# --- Random Forest Model ---
rf = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)


# --- Evaluation Metrics ---
def evaluate_model(name, y_true, y_pred):
    print(f"\n--- {name} ---")
    print(f"R² Score: {r2_score(y_true, y_pred):.4f}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_true, y_pred)):.4f}")
    print(f"MAE: {mean_absolute_error(y_true, y_pred):.4f}")


evaluate_model("Gradient Boosting", y_test, y_pred_gbr)
evaluate_model("Random Forest", y_test, y_pred_rf)


# --- SHAP Analysis ---
def shap_plot(model, X_sample, model_name):
    explainer = shap.Explainer(model.predict, X_sample)
    shap_values = explainer(X_sample)
    shap.summary_plot(shap_values, X_sample, show=False)
    plot_path = f"shap_summary_{model_name.lower().replace(' ', '_')}.png"
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.clf()
    print(f"SHAP summary plot saved for {model_name} as '{plot_path}'")


shap_plot(gbr, X_test, "Gradient Boosting")
shap_plot(rf, X_test, "Random Forest")
