from gplearn.genetic import SymbolicRegressor
print("Running gplearn...")
check_resources()
model = SymbolicRegressor(population_size=1000, generations=20, random_state=42, n_jobs=1)
model.fit(X_train, y_train)
y_pred_sym = model.predict(X_test)
r2_sym = r2_score(y_test, y_pred_sym)
print(f"gplearn - R²: {r2_sym:.4f}")
   * print("Best Equation:", model._program)
