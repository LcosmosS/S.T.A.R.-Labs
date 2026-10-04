from sklearn.metrics import r2_score, mean_squared_error
import numpy as np


y_pred = model.predict(X_test)


r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))


print(f"Test R²: {r2:.4f}")
print(f"Test RMSE: {rmse:.4f}")
