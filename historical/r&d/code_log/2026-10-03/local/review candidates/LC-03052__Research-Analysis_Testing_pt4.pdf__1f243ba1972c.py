except Exception as e:

    print(f"Failed to compute rank of twisted curve: {e}")



# Final training data update

print("\nFinal training data: {training_data}")

print(f"Final labels: {training_labels}")



# Final classifier training
scaler = StandardScaler()

X_train = scaler.fit_transform(training_data)

y_train = [1 if label >= 3 else 0 for label in training_labels]

clf = LogisticRegression(max_iter=1000)

clf.fit(X_train, y_train)

print(f"Final classifier trained. Coefficients: {clf.coef_}")

with open("final_selmer_training_data.txt", "w") as f:

    for features, label in zip(training_data, training_labels):

        f.write(f"{features},{label}\n")

print("Final training data saved to final_selmer_training_data.txt")
