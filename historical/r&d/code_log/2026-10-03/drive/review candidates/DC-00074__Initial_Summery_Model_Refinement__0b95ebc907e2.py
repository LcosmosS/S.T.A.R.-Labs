symbolic_model.fit(X_train_scaled, y_train)
print("Best symbolic models:\n", symbolic_model)


y_pysr_pred = symbolic_model.predict(X_test_scaled)
print(f"PySR R² score: {r2_score(y_test, y_pysr_pred):.4f}")


symbolic_model.save("pysr_model.pkl")
symbolic_model.equations_.to_csv("pysr_equations.csv", index=False)
print("Top PySR Equations:\n", symbolic_model.equations_.head())
