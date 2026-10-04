from sklearn.ensemble import GradientBoostingRegressor


* model = GradientBoostingRegressor(random_state=42)
* Hyperparameter Grid: Adjust the grid for hyperparameter tuning. For Random Forest:
* python
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None]
* }
* For Gradient Boosting:
* python
param_grid = {
    'n_estimators': [100, 200],
    'learning_rate': [0.01, 0.1],
    'max_depth': [3, 5]
* }
