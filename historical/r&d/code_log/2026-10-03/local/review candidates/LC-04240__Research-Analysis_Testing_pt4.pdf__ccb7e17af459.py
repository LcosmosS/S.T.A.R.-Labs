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
