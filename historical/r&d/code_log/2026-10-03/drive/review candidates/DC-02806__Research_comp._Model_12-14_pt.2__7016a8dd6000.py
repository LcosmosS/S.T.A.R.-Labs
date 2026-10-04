# -------------------------------
# Step 10: Symbolic Regression with PySR
from pysr import PySRRegressor


# Optional: reduce dimensionality or add more engineered features
# You may already have symbolic candidate features (like u_g, g_r, etc.)


symbolic_model = PySRRegressor(
    model_selection="best",  # Select best model according to loss + complexity
    niterations=100,         # Increase for better results
    population_size=1000,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["sqrt", "log", "exp"],
    loss="loss(x, y) = (x - y)^2",
    maxsize=20,
    verbosity=1,
    random_state=42,
    temp_equation_file=True  # Save intermediate results
)


# Fit PySR on raw (unscaled) data for interpretability
symbolic_model.fit(X_train, y_train)


# Display the discovered symbolic equations
print("Best symbolic models:\n", symbolic_model)


# Predict and evaluate
y_pysr_pred = symbolic_model.predict(X_test)
r2_pysr = r2_score(y_test, y_pysr_pred)
print(f"PySR R² score: {r2_pysr:.4f}")


# Save model results
symbolic_model.save("pysr_model.pkl")
symbolic_model.equations_.to_csv("pysr_equations.csv", index=False)
