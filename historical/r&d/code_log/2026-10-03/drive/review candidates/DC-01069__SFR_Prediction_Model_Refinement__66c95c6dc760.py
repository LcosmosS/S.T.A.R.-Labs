from pysr import PySRRegressor
model = PySRRegressor(
    model_selection="best",
    niterations=100,
    unary_operators=["exp", "log", "sqrt"],
    binary_operators=["+", "-", "*", "/"],
    loss="loss(x, y) = (x - y)^2",
)
model.fit(X_train, y_train)
