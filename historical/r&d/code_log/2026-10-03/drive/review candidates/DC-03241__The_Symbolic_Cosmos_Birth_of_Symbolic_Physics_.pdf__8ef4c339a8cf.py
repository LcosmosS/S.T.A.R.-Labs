sha_order = (leading_coeff * tors_order**2) / (omega * reg * tamagawa)
print(f"Adjusted |Sha(E)| to match: {sha_order}")
except Exception as e:
print(f"Failed to compute BSD invariants: {e}")
return False, None
log_delta = math.log(abs(delta)) if delta != 0 else 0
log_cond = math.log(conductor) if conductor > 0 else 0
features = [a, b, log_delta, log_cond, tors_order]
print("-" * 20)
return success, features
# Initialize data for classifier
X_data = []
y_data = []
classifier = None
# Main loop
max_successful_curves = 10
max_total_attempts = 100
n = 20 # Reduced to limit conductor size
successful_curves = 0
attempts = 0
fib_numbers = generate_fibonacci(n)
print(f"Fibonacci numbers up to index {n}: {fib_numbers}")
while successful_curves < max_successful_curves and attempts < max_total_attempts:
# Train classifier only if both classes exist
if attempts % 10 == 0 and len(X_data) >= 10 and len(set(y_data)) >= 2:
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
attempts += 1
# Analyze original curve
print(f"\nAnalyzing original curve")
success, features = analyze_curve(-1706, 6320, is_original=True)
if features:
X_data.append(features)
y_data.append(success)
