from sklearn.ensemble import RandomForestRegressor


# Initialize the Random Forest Regressor
rf_model = RandomForestRegressor(random_state=42)


# Train the model on the training data
rf_model.fit(X_train, y_train)
