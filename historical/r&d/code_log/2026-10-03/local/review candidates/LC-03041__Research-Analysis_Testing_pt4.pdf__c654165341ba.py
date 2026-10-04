    else:

        a = fib_a

        sign = -1 if (attempt - 71) % 4 == 1 else 1

        b = sign * int(round(fib_b * (PHI ** phi_powers[phi_idx])))

        print(f"\nAttempt {attempt}: Testing Fibonacci curve with a={a} (raw), b={b} (φ^{phi_powers[phi_idx]} *
