def evaluate_model(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)


    print(f"Test R²: {r2_score(y_test, y_pred):.4f}")
    print(f"Test RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")


    # SHAP
    explainer = shap.Explainer(model, X_train)
    shap_values = explainer(X_test)
    shap.summary_plot(shap_values, X_test, show=False)
    plt.savefig("shap_summary_testset.png", bbox_inches="tight")
