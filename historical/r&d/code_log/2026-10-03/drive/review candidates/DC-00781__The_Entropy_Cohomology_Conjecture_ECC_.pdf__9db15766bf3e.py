from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, max_depth=12)
model.fit(X_train, y_train)
preds = model.predict(X_test)
r2 = model.score(X_test, y_test)
