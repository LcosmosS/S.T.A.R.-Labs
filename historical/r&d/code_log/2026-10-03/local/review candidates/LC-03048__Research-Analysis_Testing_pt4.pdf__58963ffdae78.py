    training_labels.extend([0, 2])

    scaler = StandardScaler()

    X_train = scaler.fit_transform(training_data)

    y_train = [1 if label >= 3 else 0 for label in training_labels]

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)

    print(f"Classifier trained. Coefficients: {clf.coef_}")



    with open("selmer_training_data.txt", "w") as f:

        for features, label in zip(training_data, training_labels):

            f.write(f"{features},{label}\n")

    print("Training data saved to selmer_training_data.txt")

else:

    print(f"\nReached maximum attempts ({attempt-1}) without finding enough 3-Selmer rank >= 3 curves.
