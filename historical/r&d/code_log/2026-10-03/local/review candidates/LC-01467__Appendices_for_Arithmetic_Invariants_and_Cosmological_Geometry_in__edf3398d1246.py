y_train_y_num = df['y_num']

# Attempt to model numerators as a linear function of r and rho
model_x_num = LinearRegression().fit(X_train, y_train_x_num)
model_y_num = LinearRegression().fit(X_train, y_train_y_num)

print("\nNumerator Model Coefficients (Linear):")
print(f"  x_num = {model_x_num.coef_[0]:.2f}*r + {model_x_num.coef_[1]:.2f}*rho +
