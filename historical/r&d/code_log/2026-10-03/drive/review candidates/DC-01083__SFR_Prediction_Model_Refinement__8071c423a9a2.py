from sklearn.ensemble import GradientBoostingRegressor


# Train a fresh model
gb = GradientBoostingRegressor()
gb.fit(X_train, y_train)
