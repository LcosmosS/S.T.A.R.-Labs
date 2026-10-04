math.log(3422384), math.log(1711192)),
    (2584, 233, 0, 3.1224725812826300697030396822 / 10, 0.52041209688043834495050661370, 1.0, 6,
True, math.log(1104248265904), math.log(39437438068)),
]

classifier = LogisticRegression(max_iter=1000, class_weight={1: 50, 0: 1})
classifier.fit(np.array(X_data), np.array(y_data))  # Retrain with updated data
print(f"Classifier retrained. Coefficients: {classifier.coef_}")

max_successful_curves = 30
max_total_attempts = 35
n = 25
require_3selmer = False
successful_curves = 12  # 10 from first set + 2 from attempts 11 and 14
attempts = 17  # Resume from attempt 18
fib_numbers = generate_fibonacci(n)
print(f"Fibonacci numbers up to index {n}: {fib_numbers}")

# Reinitialize output files to append new results
with open("interweb_nodes.txt", "w") as f:

f.write("a,b,rank,normalized_leading_coeff,omega,regulator,tamagawa,weak_bsd_holds,log_delta,log_co
