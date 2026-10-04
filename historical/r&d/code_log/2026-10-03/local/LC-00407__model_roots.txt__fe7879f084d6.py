from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


# Basic model (you may have done this already)
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Baseline MSE: {mse:.4f}")
