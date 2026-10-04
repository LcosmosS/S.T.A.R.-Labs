training_data = []
training_labels = []
target_3selmer_curves = 5  # Stop after finding 5 curves with 3-Selmer rank >= 3
max_attempts = 100  # Maximum additional attempts
attempt = 37  # Start from the next attempt after 36
current_fib_index = 26  # Start extending from index 26

# Existing high 3-Selmer rank curves
# From previous attempts: (2, 144, selmer3=3), (377, 987, selmer3=3), (34, 4181, selmer3=3)
existing_high_selmer = [(2, 144, 3), (377, 987, 3), (34, 4181, 3)]
for a, b, selmer3 in existing_high_selmer:
    E = EllipticCurve(QQ, [0, 0, 0, a, b])
    delta = E.discriminant()
    conductor = E.conductor()
    tors_order = E.torsion_subgroup().order()
    log_delta = math.log(abs(delta))
    log_cond = math.log(conductor)
    features = [a, b, log_delta, log_cond, tors_order]
    training_data.append(features)
    training_labels.append(selmer3)
    print(f"Added existing high 3-Selmer curve to training data: a={a}, b={b}, 3-Selmer rank={selmer3}")

print(f"Starting with {len(training_data)} high 3-Selmer rank curves: {training_data}")

# Continuous testing loop
while len(training_data) < target_3selmer_curves and attempt <= 36 + max_attempts:
    # Extend Fibonacci sequence if needed
    if current_fib_index >= len(fib_numbers):
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
        print(f"Extended Fibonacci numbers to index {current_fib_index}: {fib_numbers[-1]}")
    current_fib_index += 1

    # Select a and b from Fibonacci numbers (cycle through pairs)
    a_idx = (attempt - 37) % len(fib_numbers)
    b_idx = (attempt - 37 + 1) % len(fib_numbers)
    a = fib_numbers[a_idx]
    b = fib_numbers[b_idx]

    print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a}, b={b}")
    success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E,
selmer3_rank = analyze_curve(
        a, b, require_3selmer=False, conductor_limit=1e11, descent_limit=20
    )

    if success and rank is not None:
        # Add to interweb_data
        if omega is not None and reg is not None:
            interweb_data.append((a, b, rank, normalized_leading_coeff, omega, reg, tamagawa,
