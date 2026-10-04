math.log(3422384), math.log(1711192)),
    (2584, 233, 0, 3.1224725812826300697030396822 / 10, 0.52041209688043834495050661370, 1.0, 6,
True, math.log(1104248265904), math.log(39437438068)),
    (377, 2, 1, 19.086494537074770450070509606 / 10, 0.84161318212549367925981332813,
11.3392321689115, 2, True, math.log(3429290240), math.log(5792720)),
    (-1706, 6320, 1, 5.7161472701821916623395660050 / 10, 0.42236269178325809849360427108,
3.38343524498343, 4, True, math.log(300517927424), math.log(150258963712)),
]

classifier = LogisticRegression(max_iter=1000, class_weight={1: 50, 0: 1})
classifier.fit(np.array(X_data), np.array(y_data))
print(f"Classifier retrained. Coefficients: {classifier.coef_}")

max_successful_curves = 30
max_total_attempts = 50
n = 25
require_3selmer = False
successful_curves = 13  # 10 from first set + 2 from attempts 11 and 14 + 1 from attempt 34
attempts = 17  # Resume from attempt 18
fib_numbers = generate_fibonacci(n)
print(f"Fibonacci numbers up to index {n}: {fib_numbers}")

# Reinitialize output files to append new results
with open("interweb_nodes.txt", "w") as f:

f.write("a,b,rank,normalized_leading_coeff,omega,regulator,tamagawa,weak_bsd_holds,log_delta,log_co
