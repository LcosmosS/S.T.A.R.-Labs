models = {
   "RandomForest": RandomForestRegressor(n_estimators=200, max_depth=10),
   "GradientBoosting": GradientBoostingRegressor(n_estimators=300, learning_rate=0.03, max_depth=8),
   "CatBoost": CatBoostRegressor(iterations=300, learning_rate=0.05, depth=7, verbose=False),
   "LightGBM": lgb.LGBMRegressor(n_estimators=300, learning_rate=0.03, num_leaves=64),
   "XGBoost": XGBRegressor(n_estimators=300, learning_rate=0.03, max_depth=7, reg_alpha=0.2, reg_lambda=1.0),
   "GPlearn": SymbolicRegressor(population_size=2000, generations=30,
                                function_set=['add', 'sub', 'mul', 'div', 'log', 'sqrt'],
                                metric='mean absolute error', parsimony_coefficient=0.01, random_state=42)
}

results = {}
for name, model in models.items():
   model.fit(X_train, y_train)
   preds = model.predict(X_test)
   results[name] = {
       "R2": r2_score(y_test, preds),
       "MAE": mean_absolute_error(y_test, preds)
   }
