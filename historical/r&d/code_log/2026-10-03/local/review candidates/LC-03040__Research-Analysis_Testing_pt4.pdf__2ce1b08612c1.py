    if current_fib_index >= len(fib_numbers):

        fib_numbers.append(fib_numbers[-1] + fib_numbers[-2])

        print(f"Extended Fibonacci numbers to index {current_fib_index}: {fib_numbers[-1]}")

    current_fib_index += 1



    # Select a and b indices

    a_idx = (attempt - 71) % 20

    b_idx = (attempt - 71) % len(fib_numbers)
    fib_a = fib_numbers[a_idx]

    fib_b = fib_numbers[b_idx]



    # Alternate golden ratio scaling and introduce negative coefficients

    phi_idx = (attempt - 71) % len(phi_powers)

    if (attempt - 71) % 2 == 0:

        sign = -1 if (attempt - 71) % 4 == 0 else 1

        a = sign * int(round(fib_a * (PHI ** phi_powers[phi_idx])))

        b = fib_b

        print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a} (φ^{phi_powers[phi_idx]} * {fib_a} *
