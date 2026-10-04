    # Train logistic regression classifier
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    print(f"Classifier trained. Coefficients: {clf.coef_}")

    # Save training data for future use
