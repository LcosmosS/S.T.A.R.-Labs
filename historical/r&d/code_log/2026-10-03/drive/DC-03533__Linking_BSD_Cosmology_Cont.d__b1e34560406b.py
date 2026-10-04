from sklearn.metrics import mean_squared_error
y_pred = best_rf.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"New MSE: {mse:.4f}")
