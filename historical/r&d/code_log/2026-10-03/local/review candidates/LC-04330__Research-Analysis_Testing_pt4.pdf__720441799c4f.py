    print(f"Training data: {training_data}")

    print(f"Labels: {training_labels}")

    # Add negative examples and train anyway

    training_data.extend([

        [987, 610, 24.845, 19.353, 1],

        [1597, 4181, 26.316, 24.366, 1],

    ])

    training_labels.extend([0, 2])

    scaler = StandardScaler()

    X_train = scaler.fit_transform(training_data)
    y_train = [1 if label >= 3 else 0 for label in training_labels]

    clf = LogisticRegression(max_iter=1000)

    clf.fit(X_train, y_train)

    print(f"Classifier trained with available data. Coefficients: {clf.coef_}")

    with open("selmer_training_data.txt", "w") as f:
