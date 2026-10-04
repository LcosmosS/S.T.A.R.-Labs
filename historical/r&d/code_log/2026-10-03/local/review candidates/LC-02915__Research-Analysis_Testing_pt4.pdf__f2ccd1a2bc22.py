        for i, x in enumerate(X_data):
            if x[0] == a and x[1] == b:
                X_data.pop(i)
                y_data.pop(i)
                break
        attempts += 1
        continue
    seen_pairs[(a, b)] = seen_pairs.get((a, b), 0) + 1
    print(f"\nAttempt {attempts + 1}: Testing Fibonacci curve with a={a}, b={b}")
    success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E = analyze_curve(
        a, b, require_3selmer=require_3selmer, conductor_limit=1e11
    )
    if features:
        # Remove any old entry for this (a, b) pair
        for i, x in enumerate(X_data):
            if x[0] == a and x[1] == b: