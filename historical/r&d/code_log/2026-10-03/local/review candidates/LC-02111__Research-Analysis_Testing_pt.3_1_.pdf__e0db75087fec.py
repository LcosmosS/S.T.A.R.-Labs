        print(f"Classifier trained. Coefficients: {classifier.coef_}")





    a, b = random_fibonacci_pair(n, classifier, fib_numbers, X_data)


    print(f"\nAttempt {attempts + 1}: Testing Fibonacci curve with a={a}, b={b}")


    success, features, rank = analyze_curve(a, b, require_3selmer=require_3selmer)


    if features:


        X_data.append(features)


        y_data.append(success)


        if success and rank is not None:


            interweb_data.append((a, b, rank, features[2], features[3]))  # Store a, b, rank, log_delta, log_cond


    if success and (rank is None or rank >= 2):  # Prioritize rank 2+


        successful_curves += 1


    attempts += 1





# Analyze original curve


print(f"\nAnalyzing original curve")


success, features, rank = analyze_curve(-1706, 6320, is_original=True,
require_3selmer=require_3selmer)


if features:


    X_data.append(features)