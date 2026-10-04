interweb_data = []  # Store node-edge data





# Main loop


max_successful_curves = 10


max_total_attempts = 100


n = 15  # Further reduced


require_3selmer = False  # Toggle for strict criteria


successful_curves = 0


attempts = 0


fib_numbers = generate_fibonacci(n)


print(f"Fibonacci numbers up to index {n}: {fib_numbers}")





while successful_curves < max_successful_curves and attempts < max_total_attempts:


    if attempts % 10 == 0 and len(X_data) >= 10 and len(set(y_data)) >= 2:


        print("\nTraining logistic regression classifier...")


        classifier = LogisticRegression(max_iter=1000)


        X_array = np.array(X_data)


        y_array = np.array(y_data)


        classifier.fit(X_array, y_array)