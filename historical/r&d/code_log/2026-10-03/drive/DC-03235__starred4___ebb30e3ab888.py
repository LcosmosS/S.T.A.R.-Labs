# Train a linear model to optimize coefficients
model = LinearRegression()
model.fit(X_train, y_train)


# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mse_list.append(mse)
print(f"Fold {fold+1} MSE: {mse:.4f}")
