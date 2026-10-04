    # Alternate golden ratio scaling: scale a, keep b raw, or vice versa
    phi_idx = (attempt - 71) % len(phi_powers)
    if (attempt - 71) % 2 == 0:
        # Scale a, keep b raw
        a = int(round(fib_a * (PHI ** phi_powers[phi_idx])))
        b = fib_b
        print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a} (φ^{phi_powers[phi_idx]} * {fib_a}),
b={b} (raw)")
    else:
        # Keep a raw, scale b
        a = fib_a
        b = int(round(fib_b * (PHI ** phi_powers[phi_idx])))
        print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a} (raw), b={b} (φ^{phi_powers[phi_idx]} *
