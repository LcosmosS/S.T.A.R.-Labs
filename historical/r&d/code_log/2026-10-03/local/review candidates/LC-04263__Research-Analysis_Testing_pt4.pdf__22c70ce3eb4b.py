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
