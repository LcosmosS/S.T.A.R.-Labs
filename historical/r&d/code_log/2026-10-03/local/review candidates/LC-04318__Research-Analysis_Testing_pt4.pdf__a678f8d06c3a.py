    # Train logistic regression classifier
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    print(f"Classifier trained. Coefficients: {clf.coef_}")

    # Save training data for future use
    with open("selmer_training_data.txt", "w") as f:
        for features, label in zip(training_data, training_labels):
