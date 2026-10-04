print(f"PySR R² score: {r2_score(y_test, y_pysr_pred):.4f}") \n \n
symbolic_model.save("pysr_model.pkl") \n
symbolic_model.equations_.to_csv("pysr_equations.csv", index=False) \n print("Top
