import xgboost as xgb

xgb_model = xgb.XGBRegressor(n_estimators=300, learning_rate=0.03, max_depth=7,
                             reg_alpha=0.2, reg_lambda=1.5)
xgb_model.fit(X_train, y_train)
