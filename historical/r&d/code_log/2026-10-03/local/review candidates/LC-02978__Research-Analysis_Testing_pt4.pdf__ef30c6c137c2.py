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

# Continuous testing loop with golden ratio
phi_powers = [0, 1, 2]  # Test scaling by φ^0, φ^1, φ^2
while len(training_data) < target_3selmer_curves and attempt <= 53 + max_attempts:
    # Extend Fibonacci sequence if needed
    if current_fib_index >= len(fib_numbers):
        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])
        print(f"Extended Fibonacci numbers to index {current_fib_index}: {fib_numbers[-1]}")
    current_fib_index += 1

    # Select a and b indices
    a_idx = (attempt - 54) % len(fib_numbers)
    b_idx = (attempt - 54 + 1) % len(fib_numbers)
    fib_a = fib_numbers[a_idx]
    fib_b = fib_numbers[b_idx]

    # Use golden ratio to scale coefficients
    phi_idx_a = (attempt - 54) % len(phi_powers)
    phi_idx_b = (attempt - 54 + 1) % len(phi_powers)
    a = int(round(fib_a * (PHI ** phi_powers[phi_idx_a])))
    b = int(round(fib_b * (PHI ** phi_powers[phi_idx_b])))

    print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a} (φ^{phi_powers[phi_idx_a]} * {fib_a}),
b={b} (φ^{phi_powers[phi_idx_b]} * {fib_b})")
    result = analyze_curve(a, b, require_3selmer=False, conductor_limit=1e12, descent_limit=20)

    # Handle the return value safely
    if len(result) == 10:
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E,
selmer3_rank = result
    else:
        print("Curve analysis failed, skipping...")
        attempt += 1
        continue

    if success and rank is not None: