import lightgbm as lgb

lgb_model = lgb.LGBMRegressor(num_leaves=64, learning_rate=0.03, n_estimators=300)
lgb_model.fit(X_train, y_train)
