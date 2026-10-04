from pysr import PySRRegressor


# Symbolic Regression with PySR
symbolic_model = PySRRegressor(
    model_selection="best",
    niterations=30,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["exp", "log", "sqrt"],
    extra_sympy_mappings={"log": lambda x: np.log(np.abs(x) + 1e-5)},
    loss="loss(x, y) = (x - y)^2",
    maxsize=20,
    verbosity=1,
    random_state=42,
    procs=1
)
symbolic_model.fit(X_train_scaled, y_train)
y_pred_sym = symbolic_model.predict(X_test_scaled)
r2_sym = r2_score(y_test, y_pred_sym)
print(f"PySR R²: {r2_sym:.4f}")
   * print("Top PySR Equations:\n", symbolic_model.equations_.head())
