import shap
import xgboost
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# Load California housing data
X, y = fetch_california_housing(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Train XGBoost model
model = xgboost.XGBRegressor().fit(X_train, y_train)


# SHAP explainer
explainer = shap.Explainer(model)
shap_values = explainer(X_test)


# Plot summary
shap.plots.beeswarm(shap_values)
plt.show()
