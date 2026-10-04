from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_test[["BSD_likelihood"]], y_test)
r2 = model.score(X_test[["BSD_likelihood"]], y_test)
print("R² with only BSD_likelihood:", r2)
