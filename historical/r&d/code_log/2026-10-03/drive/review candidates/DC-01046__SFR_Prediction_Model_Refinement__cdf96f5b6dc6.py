# --- SHAP: Explain Gradient Boosting Model ---
import shap


print("\nRunning SHAP for Gradient Boosting...")
explainer = shap.Explainer(gb, X_train)
shap_values = explainer(X_test)


# Summary Plot
shap.summary_plot(shap_values, X_test, plot_type="bar")


# Full detailed plot (optional but insightful)
shap.summary_plot(shap_values, X_test)


# --- Symbolic Regression with PySR ---
from pysr import PySRRegressor


print("\nRunning symbolic regression with PySR...")
symbolic_model = PySRRegressor(
    model_selection="best",  # Use best validation loss
    niterations=100,
    binary_operators=["+", "-", "*", "/"],
    unary_operators=["cos", "sin", "exp", "log", "sqrt"],
    loss="loss(x, y) = (x - y)^2",
    maxsize=20,
    verbosity=1,
)


symbolic_model.fit(X_train.values, y_train.values)


# Print best symbolic expression
print("\nBest symbolic equation:")
print(symbolic_model)


# Optionally plot loss vs complexity
symbolic_model.plot()
