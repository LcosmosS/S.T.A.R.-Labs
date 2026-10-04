# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set: {X_train.shape[0]} rows, Testing set: {X_test.shape[0]} rows")


# Subset outliers for the test set
outliers_test = outliers.loc[y_test.index]


# ... (model training, hyperparameter tuning)


# Evaluate models
rf_results = evaluate_model(best_rf, X_test, y_test, outliers_test, ~outliers_test)
gb_results = evaluate_model(best_gb, X_test, y_test, outliers_test, ~outliers_test)
