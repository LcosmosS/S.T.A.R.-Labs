import joblib


# Save the trained Gradient Boosting model and test data
joblib.dump(gb, "gb_model.pkl")
joblib.dump(X_test, "X_test.pkl")
