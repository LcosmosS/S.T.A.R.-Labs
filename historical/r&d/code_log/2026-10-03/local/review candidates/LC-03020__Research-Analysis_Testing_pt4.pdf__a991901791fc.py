        print(f"Extended Fibonacci numbers to index {current_fib_index}: {fib_numbers[-1]}")
    current_fib_index += 1

    # Select a and b indices, pairing smaller and larger Fibonacci numbers
    a_idx = (attempt - 71) % 20  # Use smaller Fibonacci numbers (indices 0 to 19)
    b_idx = (attempt - 71) % len(fib_numbers)  # Use larger Fibonacci numbers
    fib_a = fib_numbers[a_idx]
    fib_b = fib_numbers[b_idx]

    # Alternate golden ratio scaling and introduce negative coefficients
    phi_idx = (attempt - 71) % len(phi_powers)
    if (attempt - 71) % 2 == 0:
        # Scale a, keep b raw, possibly negative a
        sign = -1 if (attempt - 71) % 4 == 0 else 1  # Introduce negative coefficients every 4th attempt
        a = sign * int(round(fib_a * (PHI ** phi_powers[phi_idx])))
        b = fib_b
        print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a} (φ^{phi_powers[phi_idx]} * {fib_a} *
