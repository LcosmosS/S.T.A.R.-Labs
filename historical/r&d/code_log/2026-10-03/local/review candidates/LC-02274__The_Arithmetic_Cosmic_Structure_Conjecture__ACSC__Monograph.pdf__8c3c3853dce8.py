from pysr import PySRRegressor
model = PySRRegressor(
    niterations=1000,
    binary_operators=["+", "-", "*", "/", "log"],
    unary_operators=["exp", "sqrt"],
    model_selection="best",
    maxsize=20,
)
model.fit(X_train, y_train)
print(model)
