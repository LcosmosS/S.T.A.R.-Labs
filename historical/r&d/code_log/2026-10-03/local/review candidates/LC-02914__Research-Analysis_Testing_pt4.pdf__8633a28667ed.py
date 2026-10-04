        successful_curves += 1
attempts += 1

# Continue the loop from attempt 19
while successful_curves < max_successful_curves and attempts < max_total_attempts:
    force_failure = (attempts % 5 == 0 and attempts > 0 and len(set(y_data)) < 2)
    if attempts % 10 == 0 and len(X_data) >= 5:
        print("\nTraining logistic regression classifier...")
        if len(set(y_data)) < 2:
            print("Only one class in y_data, introducing synthetic failures...")
            for i in range(min(5, len(X_data))):
                synth_feat = [f + random.gauss(0, 0.5) for f in X_data[i]]
                X_data.append(synth_feat)
                y_data.append(0)
        classifier = LogisticRegression(max_iter=1000, class_weight={1: 50, 0: 1})
        rank3_features = [x for x, y in zip(X_data, y_data) if y and x[2] > 15]
        for feat in rank3_features:
            synth_feat = [f + random.gauss(0, 0.4) for f in feat]
            X_data.append(synth_feat)
            y_data.append(1)
        classifier.fit(np.array(X_data), np.array(y_data))
        print(f"Classifier trained. Coefficients: {classifier.coef_}")

    a, b = random_fibonacci_pair(n, classifier, fib_numbers, X_data, force_failure, seen_pairs)
    if seen_pairs.get((a, b), 0) >= 1:
        print(f"Duplicate pair a={a}, b={b}, skipping")
        with open("failed_curves.txt", "a") as f:
            f.write(f"a={a},b={b},conductor=N/A,reason=duplicate\n")
        # Remove the old entry from X_data and y_data
        old_entry = [a, b, math.log(abs(-16 * (4 * a**3 + 27 * b**2))), math.log(E.conductor()) if 'E' in locals()
