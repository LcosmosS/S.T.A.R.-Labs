import shap
import xgboost
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split


# Load data
X, y = load_boston(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# Train simple model
model = xgboost.XGBRegressor().fit(X_train, y_train)


# Create SHAP explainer and values
explainer = shap.Explainer(model)
shap_values = explainer(X_test)


# Plot summary
shap.plots.beeswarm(shap_values)
