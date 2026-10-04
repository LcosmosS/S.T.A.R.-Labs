with open("failed_curves.txt", "w") as f:
    f.write("a,b,conductor,reason\n")
with open("rank3_curves.txt", "w") as f:
    f.write("a,b,rank,selmer3,volume\n")
with open("unique_curves.txt", "w") as f:
    f.write("a,b,rank,omega,reg,volume,scaled_reg,leading_coeff,conductor,plot_file\n")

while successful_curves < max_successful_curves and attempts < max_total_attempts:
    force_failure = (attempts % 5 == 0 and attempts > 0 and len(set(y_data)) < 2)
    if attempts % 10 == 0 and len(X_data) >= 10 and len(set(y_data)) >= 2:
        print("\nTraining logistic regression classifier...")
        classifier = LogisticRegression(max_iter=1000)
        X_array = np.array(X_data)
        y_array = np.array(y_data)
        classifier.fit(X_array, y_array)
        print(f"Classifier trained. Coefficients: {classifier.coef_}")

    a, b = random_fibonacci_pair(n, classifier, fib_numbers, X_data, force_failure, seen_pairs)
    seen_pairs[(a, b)] = seen_pairs.get((a, b), 0) + 1
    print(f"\nAttempt {attempts + 1}: Testing Fibonacci curve with a={a}, b={b}")
    success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E = analyze_curve(
        a, b, require_3selmer=require_3selmer
    )
    if features:
        X_data.append(features)
        y_data.append(success)
        if success and rank is not None:
            cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
            comoving_volume = (omega * reg * cosmo_scale**3) / (8e13 if rank == 3 else 1e14)
            scaled_reg = reg * SQRT_KAPPA * (20 if rank == 3 else 10 if rank >= 2 else 20)
            interweb_data.append((a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
