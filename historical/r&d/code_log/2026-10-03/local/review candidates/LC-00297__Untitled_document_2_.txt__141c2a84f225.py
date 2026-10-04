mse = mean_squared_error(y_test, y_pred) r2 = r2_score(y_test, y_pred)
print(f"Initial MSE: {mse:.4f}") print(f"Initial R-squared: {r2:.4f}")
from sklearn.model_selection import GridSearchCV
