np.array(X_data) 198 y_array = np.array(y_data) --> 199 classifier.fit(X_array, y_array) 200
print(f"Classifier trained. Coefficients: {classifier.coef_}") 202 a, b =
random_fibonacci_pair(n, classifier, fib_numbers, X_data)
