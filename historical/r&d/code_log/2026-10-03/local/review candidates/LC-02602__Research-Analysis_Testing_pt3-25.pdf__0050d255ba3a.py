        X_array = np.array(X_data)
        y_array = np.array(y_data)
        classifier.fit(X_array, y_array)
        print(f"Classifier trained. Coefficients: {classifier.coef_}")

    a, b = random_fibonacci_pair(n, classifier, fib_numbers, X_data, force_failure, seen_pairs)
    seen_pairs[(a, b)] = seen_pairs.get((a, b), 0) + 1
    print(f"\nAttempt {attempts + 1}: Testing Fibonacci curve with a={a}, b={b}")
    success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds = analyze_curve(
        a, b, require_3selmer=require_3selmer
    )
    if features:
        X_data.append(features)
        y_data.append(success)
        if success and rank is not None:
            cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
            comoving_volume = (omega * reg * cosmo_scale**3) / 1e14
            interweb_data.append((a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
