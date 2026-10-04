from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=500, max_depth=8, random_state=42)
rf.fit(X_train, y_train)
rf_r2 = rf.score(X_test, y_test)
