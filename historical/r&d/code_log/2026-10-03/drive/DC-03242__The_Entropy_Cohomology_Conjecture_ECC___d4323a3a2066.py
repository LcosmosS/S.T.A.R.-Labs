from sklearn.ensemble import GradientBoostingRegressor

gb_model = GradientBoostingRegressor(
   n_estimators=300,
   learning_rate=0.03,
   max_depth=8,
   subsample=0.85,
   loss='ls'
)
gb_model.fit(X_train, y_train)
