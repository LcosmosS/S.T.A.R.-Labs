from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(X_train, y_train)
* print("Linear Regression R²:", r2_score(y_test, lr.predict(X_test)))
