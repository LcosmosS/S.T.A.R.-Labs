                print("Strong BSD fails: Leading coefficient does not match with |Sha(E)| = 1")
                sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)
                print(f"Adjusted |Sha(E)| to match: {sha_order}")
        except Exception as e:
            print(f"Failed to compute BSD invariants: {e}")
            return False, None

    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(conductor) if conductor > 0 else 0
    features = [a, b, log_delta, log_cond, tors_order]
    success = 1 if (rank_success and selmer2_success and selmer3_success) else 0

    print("-" * 20)
    return success, features

# Initialize data for classifier
X_data = []
y_data = []
classifier = None

# Main loop
max_successful_curves = 10
max_total_attempts = 100
n = 30
successful_curves = 0
attempts = 0
fib_numbers = generate_fibonacci(n)
print(f"Fibonacci numbers up to index {n}: {fib_numbers}")

while successful_curves < max_successful_curves and attempts < max_total_attempts:
    # Train classifier every 10 attempts if enough data
    if attempts % 10 == 0 and len(X_data) >= 10:
        print("\nTraining logistic regression classifier...")
        classifier = LogisticRegression(max_iter=1000)
        X_array = np.array(X_data)
        y_array = np.array(y_data)
        classifier.fit(X_array, y_array)
        print(f"Classifier trained. Coefficients: {classifier.coef_}")

    a, b = random_fibonacci_pair(n, classifier, fib_numbers, X_data)
    print(f"\nAttempt {attempts + 1}: Testing Fibonacci curve with a={a}, b={b}")
    success, features = analyze_curve(a, b)
    if features:
        X_data.append(features)
        y_data.append(success)
    if success:
        successful_curves += 1