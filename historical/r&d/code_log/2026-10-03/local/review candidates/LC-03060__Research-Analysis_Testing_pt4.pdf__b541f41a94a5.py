    fib_a = fib_numbers[a_idx]
    fib_b = fib_numbers[b_idx]

    phi_idx = (attempt - 71) % len(phi_powers)
    if (attempt - 71) % 2 == 0:
        sign = -1 if (attempt - 71) % 4 == 0 else 1
        a = sign * int(round(fib_a * (PHI ** phi_powers[phi_idx])))
        b = fib_b
        print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a} (φ^{phi_powers[phi_idx]} *
