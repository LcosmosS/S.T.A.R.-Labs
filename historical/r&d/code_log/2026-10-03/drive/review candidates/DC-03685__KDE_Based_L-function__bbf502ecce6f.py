print("X_train_scaled sample:")
print(pd.DataFrame(X_train_scaled).head())  # Wrap in DataFrame for easier view
print("X_train_scaled stats:")
print("Min:", np.min(X_train_scaled))
print("Max:", np.max(X_train_scaled))
print("Any NaNs?", np.isnan(X_train_scaled).any())


print("\ny_train sample:")
print(y_train.head())
print("y_train stats:")
print("Min:", y_train.min())
print("Max:", y_train.max())
print("Any NaNs?", y_train.isna().any())
