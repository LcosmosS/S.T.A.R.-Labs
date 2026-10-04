from sklearn.ensemble import GradientBoostingRegressor
# Initialize the model
model = GradientBoostingRegressor(random_state=42)
# Define a new param_grid
param_grid = { 'n_estimators': [100, 200], 'learning_rate': [0.01, 0.1], 'max_depth': [3, 5, 7] }
